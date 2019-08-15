import datetime

from django.test import Client, TestCase
from unittest.mock import MagicMock, patch
from django.core.management import call_command
from django.utils.six import StringIO

from tests import test_util

from messenger import views
from messenger.models import MessengerClient, MessengerPhoneNumber, MessengerNotification, MessengerSubscriber

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
    notification = MessengerNotification(messenger_client=client, day=datetime.date(year=2019, month=11, day=5), message="Reminder: today is election day.  Your polling location is {name}, located at {location}", geo_layer_url=url, formatter='ElectionFormatter')
    notification.save()


class MessengerTests(TestCase):

    def cleanup_db(self):
        
        for model in [ MessengerSubscriber, MessengerNotification, MessengerPhoneNumber, MessengerClient ]:
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

        street_address = '7840 Van Dyke Pl'
        location, address = geocode_address(street_address=street_address)

        subscriber = MessengerSubscriber(messenger_client=MessengerClient.objects.first(), phone_number='+15005550006', status='active',
            address=street_address, latitude=location['location']['y'], longitude=location['location']['x']
        )
        subscriber.save()

        out = StringIO()

        with patch.object(messaging.MsgHandler, 'send_text') as mock_method:

            call_command('send_messages', 'elections', '--today=20191105', stdout=out)

        mock_method.assert_called_once_with(phone_number='+15005550006', text='Reminder: today is election day.  Your polling location is MAR. GARVEY ACADEMY, located at 2301 VAN DYKE ST.')
