import datetime
from datetime import date

from django.test import Client, TestCase
import mock
from unittest.mock import MagicMock, patch
from django.core.management import call_command
from django.utils.six import StringIO
from django.core.management.base import CommandError

from tests import test_util

from messenger import views
from messenger.models import MessengerClient, MessengerPhoneNumber, MessengerMessage, MessengerNotification, MessengerSubscriber
from messenger.util import NotificationException, send_messages

from cod_utils import messaging
from cod_utils.util import geocode_address


TEXT_DATA = {
  'FromState': [
    'MI'
  ],
  'From': [
    '+15005550006'
  ],
  'ToState': [
    'MI'
  ],
  'ToZip': [
    ''
  ],
  'SmsStatus': [
    'received'
  ],
  'FromCountry': [
    'US'
  ],
  'FromCity': [
    'DETROIT'
  ],
  'SmsMessageSid': [
    'ABC'
  ],
  'AccountSid': [
    'XYZ'
  ],
  'NumSegments': [
    '1'
  ],
  'MessageSid': [
    'DUMMY'
  ],
  'ToCity': [
    ''
  ],
  'Body': [
    '7840 van dyke pl'
  ],
  'ToCountry': [
    'US'
  ],
  'SmsSid': [
    'DUMMY'
  ],
  'FromZip': [
    '10010'
  ],
  'NumMedia': [
    '0'
  ],
  'To': [
    '+15005550006'
  ]
}


def setup_messenger():

    url="https://services2.arcgis.com/qvkbeam7Wirps6zC/arcgis/rest/services/Elections_2019/FeatureServer/0/query?where=1%3D1&objectIds=&time=&geometry={lng}%2C+{lat}&geometryType=esriGeometryPoint&inSR=4326&spatialRel=esriSpatialRelIntersects&resultType=none&distance=0.0&units=esriSRUnit_Meter&returnGeodetic=false&outFields=*&returnGeometry=false&returnCentroid=false&featureEncoding=esriDefault&multipatchOption=xyFootprint&maxAllowableOffset=&geometryPrecision=&outSR=&datumTransformation=&applyVCSProjection=false&returnIdsOnly=false&returnUniqueIdsOnly=false&returnCountOnly=false&returnExtentOnly=false&returnQueryGeometry=false&returnDistinctValues=false&cacheHint=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&having=&resultOffset=&resultRecordCount=&returnZ=false&returnM=false&returnExceededLimitFeatures=true&quantizationParameters=&sqlFormat=none&f=pjson&token="

    client = MessengerClient(name='elections', description='Elections Messenger', confirmation_message="You will receive elections reminders for the address {street_address}")
    client.save()
    phone_number = MessengerPhoneNumber(messenger_client=client, phone_number='5005550006', description='Test phone number')
    phone_number.save()
    notification = MessengerNotification(messenger_client=client, day=datetime.date(year=2019, month=11, day=5),
      geo_layer_url=url, formatter='ElectionFormatter')
    notification.save()
    message = MessengerMessage(messenger_notification=notification,
      message='Reminder: today is election day.  Your polling location is {name}, located at {location} - open in maps: https://www.google.com/maps/search/?api=1&query={lat},{lng}')
    message.save()


class MessengerTests(TestCase):

    def cleanup_db(self):
        
        for model in [ MessengerSubscriber, MessengerMessage, MessengerNotification, MessengerPhoneNumber, MessengerClient ]:
            test_util.cleanup_model(model)

    def setUp(self):
        """
        Set up each unit test, including making sure database is properly cleaned up before each test
        """
        self.cleanup_db()
        self.maxDiff = None

        setup_messenger()

    # Test actual API endpoints
    def test_subscribe(self):

        with patch.object(messaging.MsgHandler, 'send_text') as mock_method:

          c = Client()
          response = c.post('/messenger/subscribe/', TEXT_DATA)

        mock_method.assert_called_once_with(phone_number='5005550006', text='You will receive elections reminders for the address 7840 VAN DYKE PL')

        expected = {'received': {'phone_number': '5005550006', 'address': '7840 VAN DYKE PL'}, 'message': 'New elections subscriber created'}
        self.assertEqual(response.status_code, 201)
        self.assertDictEqual(response.data, expected, "Subscription signup returns correct message")

    def test_subscribe_msg_missing_fone(self):

        c = Client()
        response = c.post('/messenger/subscribe/', { "address": "1104 Military St" } )

        expected = {'error': 'Address and phone_number are required'}
        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(response.data, expected, "Subscription signup returns correct message")

    def test_subscribe_msg_missing_address(self):

        c = Client()
        response = c.post('/messenger/subscribe/', { "phone_number": "5005550006" } )

        expected = {'error': 'Address and phone_number are required'}
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, expected, "Subscription signup returns correct message")

    def test_subscribe_msg_missing_destination_fone_number(self):

        phone_number = MessengerPhoneNumber.objects.first()
        phone_number.phone_number = '1234567890'
        phone_number.save()

        c = Client()
        response = c.post('/messenger/subscribe/', TEXT_DATA)

        expected = {'error': 'phone_number 5005550006 not found'}
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, expected, "Subscription signup returns correct message")

    def test_subscribe_msg_invalid_address(self):

        text_data = TEXT_DATA.copy()
        text_data['Body'][0] = 'invalid address'

        c = Client()
        response = c.post('/messenger/subscribe/', text_data)

        expected = {'error': "Street address 'INVALID ADDRESS' not found"}
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, expected, "Subscription signup returns correct message")

    def test_send_messages(self):
        "Test sending a basic formatted message"

        subscriber = MessengerSubscriber(messenger_client=MessengerClient.objects.first(), phone_number='+15005550006', status='active', address='7840 Van Dyke Pl')
        subscriber.save()

        out = StringIO()

        with patch.object(messaging.MsgHandler, 'send_text') as mock_method:

            call_command('send_messages', 'elections', '--today=20191105', stdout=out)

        message = 'Reminder: today is election day.  Your polling location is MAR. GARVEY ACADEMY, located at 2301 VAN DYKE ST. - open in maps: https://www.google.com/maps/search/?api=1&query=42.35972900000,-83.00074500000'
        mock_method.assert_called_once_with(phone_number='+15005550006', text=message)

    def test_send_messages_multi_lang(self):
        "Test sending a basic formatted message with multi-language support"

        message = MessengerMessage(messenger_notification=MessengerNotification.objects.first(), lang='es',
            message='Recordatorio: hoy es el día de las elecciones. Su lugar de votación es {name}, situado en {location} - abrir en mapas: https://www.google.com/maps/search/?api=1&query={lat},{lng}')
        message.save()

        subscriber = MessengerSubscriber(messenger_client=MessengerClient.objects.first(), phone_number='+15005550006', status='active', address='7840 Van Dyke Pl', lang='es')
        subscriber.save()

        out = StringIO()

        with patch.object(messaging.MsgHandler, 'send_text') as mock_method:

            call_command('send_messages', 'elections', '--today=20191105', stdout=out)

        message = 'Recordatorio: hoy es el día de las elecciones. Su lugar de votación es MAR. GARVEY ACADEMY, situado en 2301 VAN DYKE ST. - abrir en mapas: https://www.google.com/maps/search/?api=1&query=42.35972900000,-83.00074500000'
        mock_method.assert_called_once_with(phone_number='+15005550006', text=message)

    def test_send_messages_simple(self):
        "Test sending a message with no geo layer (just the message itself"

        notification = MessengerNotification.objects.first()
        notification.geo_layer_url = None
        notification.message = "Don't forget to vote today!"
        notification.save()

        messenger_message = notification.messengermessage_set.first()
        messenger_message.message = "Don't forget to vote today!"
        messenger_message.save()

        subscriber = MessengerSubscriber(messenger_client=MessengerClient.objects.first(), phone_number='+15005550006', status='active', address='7840 Van Dyke Pl')
        subscriber.save()

        out = StringIO()

        with patch.object(messaging.MsgHandler, 'send_text') as mock_method:

            call_command('send_messages', 'elections', '--today=20191105', stdout=out)

        message = "Don't forget to vote today!"
        mock_method.assert_called_once_with(phone_number='+15005550006', text=message)

    def test_send_messages_no_notifications(self):

        test_util.cleanup_model(MessengerMessage)
        test_util.cleanup_model(MessengerNotification)

        subscriber = MessengerSubscriber(messenger_client=MessengerClient.objects.first(), phone_number='+15005550006', status='active', address='7840 Van Dyke Pl')
        subscriber.save()

        messages_meta = send_messages(client_name='elections', day=date(2019, 11, 5))
        self.assertEqual('\nclient: elections\nday:    2019-11-05\n\nnotifications:  (No notifications sent)', messages_meta.describe(), "No messages can be sent")

    def test_send_messages_no_message(self):
        "Test sending a message with no message set in database"

        test_util.cleanup_model(MessengerMessage)

        subscriber = MessengerSubscriber(messenger_client=MessengerClient.objects.first(), phone_number='+15005550006', status='active', address='7840 Van Dyke Pl')
        subscriber.save()

        out = StringIO()
        with self.assertRaises(NotificationException):

            call_command('send_messages', 'elections', '--today=20191105', stdout=out)

    def test_send_messages_no_formatter(self):

        notification = MessengerNotification.objects.first()
        notification.formatter = None
        notification.save()

        subscriber = MessengerSubscriber(messenger_client=MessengerClient.objects.first(), phone_number='+15005550006', status='active', address='7840 Van Dyke Pl')
        subscriber.save()

        out = StringIO()
        with self.assertRaises(NotificationException):

            call_command('send_messages', 'elections', '--today=20191105', stdout=out)

    def test_send_messages_invalid_formatter(self):

        notification = MessengerNotification.objects.first()
        notification.formatter = "invalid"
        notification.save()

        subscriber = MessengerSubscriber(messenger_client=MessengerClient.objects.first(), phone_number='+15005550006', status='active', address='7840 Van Dyke Pl')
        subscriber.save()

        out = StringIO()
        with self.assertRaises(NotificationException):

            call_command('send_messages', 'elections', '--today=20191105', stdout=out)

    def test_send_messages_invalid_client_name(self):

        out = StringIO()
        with self.assertRaises(CommandError):

            call_command('send_messages', 'invalid', '--today=20191105', stdout=out)

    @mock.patch('requests.get')
    def test_send_messages_invalid_geo_layer_url(self, mocked_requests_get):

        class MockedResponse():

            def __init__(self):
                self.ok = False

        subscriber = MessengerSubscriber(messenger_client=MessengerClient.objects.first(), phone_number='+15005550006', status='active', address='7840 Van Dyke Pl')
        subscriber.save()

        out = StringIO()
        with self.assertRaises(NotificationException):

            mocked_requests_get.return_value = MockedResponse()
            call_command('send_messages', 'elections', '--today=20191105', stdout=out)

    def test_send_messages_invalid_dryrun_param(self):

        out = StringIO()
        with self.assertRaises(CommandError):

            call_command('send_messages', 'elections', '--today=20191105', '--dry_run=maybe', stdout=out)

    def test_send_messages_invalid_date_param(self):

        out = StringIO()
        with self.assertRaises(CommandError):

            call_command('send_messages', 'elections', '--today=201911050', stdout=out)
