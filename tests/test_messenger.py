import datetime
from datetime import date

from django.test import Client, TestCase
import mock
from unittest.mock import MagicMock, patch
from django.core.management import call_command
from django.utils.six import StringIO
from django.core.management.base import CommandError

from rest_framework.exceptions import PermissionDenied

from tests import test_util

from messenger import views
from messenger.models import *
from messenger.util import NotificationException, send_messages

from cod_utils import messaging

from twilio.request_validator import RequestValidator


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


class MessengerBaseTests(TestCase):

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


class MessengerTests(MessengerBaseTests):

    # Test actual API endpoints
    def test_subscribe(self):

        with patch.object(messaging.MsgHandler, 'send_text') as mock_method, patch.object(RequestValidator, 'validate') as mock_validate:
            mock_validate.return_value = True

            c = Client()
            response = c.post('/messenger/subscribe/', TEXT_DATA)

        mock_method.assert_called_once_with(phone_number='5005550006', text='You will receive elections reminders for the address 7840 VAN DYKE PL')

        expected = {'received': {'phone_number': '5005550006', 'address': '7840 VAN DYKE PL'}, 'message': 'New elections subscriber created'}
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, expected, "Subscription signup returns correct message")

    def test_subscribe_msg_missing_fone(self):

        with patch.object(RequestValidator, 'validate') as mock_validate:
            mock_validate.return_value = True

            c = Client()
            response = c.post('/messenger/subscribe/', { "address": "1104 Military St" } )

        expected = {'error': 'Address and phone_number are required'}
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, expected, "Subscription signup returns correct message")

    def test_subscribe_msg_missing_address(self):

        with patch.object(RequestValidator, 'validate') as mock_validate:
            mock_validate.return_value = True

            c = Client()
            response = c.post('/messenger/subscribe/', { "phone_number": "5005550006" } )

        expected = {'error': 'Address and phone_number are required'}
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, expected, "Subscription signup returns correct message")

    def test_subscribe_msg_missing_destination_fone_number(self):

        phone_number = MessengerPhoneNumber.objects.first()
        phone_number.phone_number = '1234567890'
        phone_number.save()

        with patch.object(RequestValidator, 'validate') as mock_validate:
            mock_validate.return_value = True

            c = Client()
            response = c.post('/messenger/subscribe/', TEXT_DATA)

        expected = {'error': 'phone_number 5005550006 not found'}
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, expected, "Subscription signup returns correct message")

    def test_subscribe_msg_invalid_address(self):

        text_data = TEXT_DATA.copy()
        text_data['Body'][0] = 'invalid address'

        with patch.object(RequestValidator, 'validate') as mock_validate:
            mock_validate.return_value = True

            c = Client()
            response = c.post('/messenger/subscribe/', text_data)

        expected = {'error': "Street address 'INVALID ADDRESS' not found"}
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, expected, "Subscription signup returns correct message")

    def test_subscribe_no_authentication(self):

        c = Client()
        response = c.post('/messenger/subscribe/', TEXT_DATA)
        self.assertEqual(response.status_code, 403, "MsgHandler.validate() catches invalid requests")

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

    def test_send_message_subscriber_outside_geo(self):
        "Test sending messages when subscriber is outside notification's polygon"

        subscriber = MessengerSubscriber(messenger_client=MessengerClient.objects.first(), phone_number='+15005550006', status='active',
            address='132 Dikeman Street Ann Arbor, MI', latitude='42.201225', longitude='-83.150925')
        super(MessengerSubscriber, subscriber).save()

        messages_meta = send_messages(client_name='elections', day=date(2019, 11, 5))
        self.assertEqual('\nclient: elections\nday:    2019-11-05\n\nnotifications:  (No notifications sent)', messages_meta.describe(), "No messages can be sent")

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


class MessengerDashboardTests(MessengerBaseTests):

    def test_add_notification(self):
        "Test adding a notification"

        c = Client()
        response = c.post('/messenger/clients/1/notifications/', {
            "client_id": 1,
            "day": "2019/11/05",
            "geo_layer_url": "https://services2.arcgis.com/qvkbeam7Wirps6zC/arcgis/rest/services/Elections_2019/FeatureServer/0/query?where=1%3D1&objectIds=&time=&geometry={lng}%2C+{lat}&geometryType=esriGeometryPoint&inSR=4326&spatialRel=esriSpatialRelIntersects&resultType=none&distance=0.0&units=esriSRUnit_Meter&returnGeodetic=false&outFields=*&returnGeometry=false&returnCentroid=false&featureEncoding=esriDefault&multipatchOption=xyFootprint&maxAllowableOffset=&geometryPrecision=&outSR=&datumTransformation=&applyVCSProjection=false&returnIdsOnly=false&returnUniqueIdsOnly=false&returnCountOnly=false&returnExtentOnly=false&returnQueryGeometry=false&returnDistinctValues=false&cacheHint=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&having=&resultOffset=&resultRecordCount=&returnZ=false&returnM=false&returnExceededLimitFeatures=true&quantizationParameters=&sqlFormat=none&f=pjson&token=",
            "formatter": "ElectionFormatter"
            })

        expected = {
            'id': 2,
            'day': '2019-11-05T00:00:00.000Z',
            'geo_layer_url': 'https://services2.arcgis.com/qvkbeam7Wirps6zC/arcgis/rest/services/Elections_2019/FeatureServer/0/query?where=1%3D1&objectIds=&time=&geometry={lng}%2C+{lat}&geometryType=esriGeometryPoint&inSR=4326&spatialRel=esriSpatialRelIntersects&resultType=none&distance=0.0&units=esriSRUnit_Meter&returnGeodetic=false&outFields=*&returnGeometry=false&returnCentroid=false&featureEncoding=esriDefault&multipatchOption=xyFootprint&maxAllowableOffset=&geometryPrecision=&outSR=&datumTransformation=&applyVCSProjection=false&returnIdsOnly=false&returnUniqueIdsOnly=false&returnCountOnly=false&returnExtentOnly=false&returnQueryGeometry=false&returnDistinctValues=false&cacheHint=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&having=&resultOffset=&resultRecordCount=&returnZ=false&returnM=false&returnExceededLimitFeatures=true&quantizationParameters=&sqlFormat=none&f=pjson&token=',
            'formatter': 'ElectionFormatter',
            'locations': {},
            'messages': []
        }

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, expected, "Notification gets added")

    def test_get_all_locations(self):
        "Test returning all locations"

        for location in [ 48214, 48226 ]:
            MessengerLocation(location_type="ZIP Code", value=location).save()

        for location in [ 1, 2 ]:
            MessengerLocation(location_type="DHSEM Evacuation Zone", value=location).save()

        c = Client()
        response = c.get('/messenger/locations/')

        expected = {'DHSEM Evacuation Zone': ['1', '2'], 'ZIP Code': ['48214', '48226']}

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected, "Locations get returned")

    def test_add_notification_location(self):
        "Test adding a notification with a location"


        for location in [ 48214, 48226 ]:
            MessengerLocation(location_type="ZIP Code", value=location).save()

        cl = Client()
        response = cl.post('/messenger/clients/1/notifications/', {
            "client_id": 1,
            "day": "2019/11/05",
            "geo_layer_url": "https://services2.arcgis.com/qvkbeam7Wirps6zC/arcgis/rest/services/Elections_2019/FeatureServer/0/query?where=1%3D1&objectIds=&time=&geometry={lng}%2C+{lat}&geometryType=esriGeometryPoint&inSR=4326&spatialRel=esriSpatialRelIntersects&resultType=none&distance=0.0&units=esriSRUnit_Meter&returnGeodetic=false&outFields=*&returnGeometry=false&returnCentroid=false&featureEncoding=esriDefault&multipatchOption=xyFootprint&maxAllowableOffset=&geometryPrecision=&outSR=&datumTransformation=&applyVCSProjection=false&returnIdsOnly=false&returnUniqueIdsOnly=false&returnCountOnly=false&returnExtentOnly=false&returnQueryGeometry=false&returnDistinctValues=false&cacheHint=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&having=&resultOffset=&resultRecordCount=&returnZ=false&returnM=false&returnExceededLimitFeatures=true&quantizationParameters=&sqlFormat=none&f=pjson&token=",
            "formatter": "ElectionFormatter",
            "location_type": "ZIP Code",
            "locations": [ 48214, 48226 ]
            })

        expected = {
            'id': 2,
            'day': '2019-11-05T00:00:00.000Z',
            'geo_layer_url': 'https://services2.arcgis.com/qvkbeam7Wirps6zC/arcgis/rest/services/Elections_2019/FeatureServer/0/query?where=1%3D1&objectIds=&time=&geometry={lng}%2C+{lat}&geometryType=esriGeometryPoint&inSR=4326&spatialRel=esriSpatialRelIntersects&resultType=none&distance=0.0&units=esriSRUnit_Meter&returnGeodetic=false&outFields=*&returnGeometry=false&returnCentroid=false&featureEncoding=esriDefault&multipatchOption=xyFootprint&maxAllowableOffset=&geometryPrecision=&outSR=&datumTransformation=&applyVCSProjection=false&returnIdsOnly=false&returnUniqueIdsOnly=false&returnCountOnly=false&returnExtentOnly=false&returnQueryGeometry=false&returnDistinctValues=false&cacheHint=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&having=&resultOffset=&resultRecordCount=&returnZ=false&returnM=false&returnExceededLimitFeatures=true&quantizationParameters=&sqlFormat=none&f=pjson&token=',
            'formatter': 'ElectionFormatter',
            'locations': {'ZIP Code': ['48214', '48226']},
            'messages': []
        }

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, expected, "Notification gets added")

    def test_add_invalid_notification_location(self):
        "Test adding a notification with an invalid location"

        cl = Client()
        response = cl.post('/messenger/clients/1/notifications/', {
            "client_id": 1,
            "day": "2019/11/05",
            "geo_layer_url": "https://services2.arcgis.com/qvkbeam7Wirps6zC/arcgis/rest/services/Elections_2019/FeatureServer/0/query?where=1%3D1&objectIds=&time=&geometry={lng}%2C+{lat}&geometryType=esriGeometryPoint&inSR=4326&spatialRel=esriSpatialRelIntersects&resultType=none&distance=0.0&units=esriSRUnit_Meter&returnGeodetic=false&outFields=*&returnGeometry=false&returnCentroid=false&featureEncoding=esriDefault&multipatchOption=xyFootprint&maxAllowableOffset=&geometryPrecision=&outSR=&datumTransformation=&applyVCSProjection=false&returnIdsOnly=false&returnUniqueIdsOnly=false&returnCountOnly=false&returnExtentOnly=false&returnQueryGeometry=false&returnDistinctValues=false&cacheHint=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&having=&resultOffset=&resultRecordCount=&returnZ=false&returnM=false&returnExceededLimitFeatures=true&quantizationParameters=&sqlFormat=none&f=pjson&token=",
            "formatter": "ElectionFormatter",
            "location_type": "ZIP Code",
            "locations": [ 10001 ]
            })

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {'error': 'ZIP Code with value 10001 is invalid '}, "Invalid locations are rejected")

    def test_add_notification_invalid_client(self):
        "Test adding a notification with invalid client id"

        c = Client()
        response = c.post('/messenger/clients/1/notifications/', {
            "client_id": "invalid",
            "day": "2019/11/05"
            })

        self.assertEqual(response.status_code, 404)
        self.assertEqual({'error': 'Client invalid not found'}, response.json())

    def test_add_notification_invalid_day(self):
        "Test adding a notification with invalid day format"

        c = Client()
        response = c.post('/messenger/clients/1/notifications/', {
            "client_id": 1,
            "day": "2019/11/5"
            })

        self.assertEqual(response.status_code, 400)

    def test_add_notification_missing_day(self):
        "Test adding a notification with invalid day format"

        c = Client()
        response = c.post('/messenger/clients/1/notifications/', { "client_id": 1 })

        self.assertEqual(response.status_code, 400)

    def test_update_notification(self):
        "Test updating a notification"

        c = Client()
        response = c.post('/messenger/clients/1/notifications/1/', {
            "client_id": 1,
            "day": "2019/11/05",
            "geo_layer_url": "https://services2.arcgis.com/qvkbeam7Wirps6zC/arcgis/rest/services/Elections_2019/FeatureServer/0/query?where=1%3D1&objectIds=&time=&geometry={lng}%2C+{lat}&geometryType=esriGeometryPoint&inSR=4326&spatialRel=esriSpatialRelIntersects&resultType=none&distance=0.0&units=esriSRUnit_Meter&returnGeodetic=false&outFields=*&returnGeometry=false&returnCentroid=false&featureEncoding=esriDefault&multipatchOption=xyFootprint&maxAllowableOffset=&geometryPrecision=&outSR=&datumTransformation=&applyVCSProjection=false&returnIdsOnly=false&returnUniqueIdsOnly=false&returnCountOnly=false&returnExtentOnly=false&returnQueryGeometry=false&returnDistinctValues=false&cacheHint=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&having=&resultOffset=&resultRecordCount=&returnZ=false&returnM=false&returnExceededLimitFeatures=true&quantizationParameters=&sqlFormat=none&f=pjson&token=",
            "formatter": "ElectionFormatter"
            })

        expected = {
            'id': 1,
            'day': '2019-11-05T00:00:00.000Z',
            'geo_layer_url': 'https://services2.arcgis.com/qvkbeam7Wirps6zC/arcgis/rest/services/Elections_2019/FeatureServer/0/query?where=1%3D1&objectIds=&time=&geometry={lng}%2C+{lat}&geometryType=esriGeometryPoint&inSR=4326&spatialRel=esriSpatialRelIntersects&resultType=none&distance=0.0&units=esriSRUnit_Meter&returnGeodetic=false&outFields=*&returnGeometry=false&returnCentroid=false&featureEncoding=esriDefault&multipatchOption=xyFootprint&maxAllowableOffset=&geometryPrecision=&outSR=&datumTransformation=&applyVCSProjection=false&returnIdsOnly=false&returnUniqueIdsOnly=false&returnCountOnly=false&returnExtentOnly=false&returnQueryGeometry=false&returnDistinctValues=false&cacheHint=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&having=&resultOffset=&resultRecordCount=&returnZ=false&returnM=false&returnExceededLimitFeatures=true&quantizationParameters=&sqlFormat=none&f=pjson&token=',
            'formatter': 'ElectionFormatter',
            'locations': {},
            'messages': [{'id': 1, 'lang': 'en', 'message': 'Reminder: today is election day.  Your polling location is {name}, located at {location} - open in maps: https://www.google.com/maps/search/?api=1&query={lat},{lng}'}]
        }

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, expected, "Notification gets added")

    def test_update_notification_geo_only(self):
        "Test updating a notification"

        c = Client()
        response = c.post('/messenger/clients/1/notifications/1/', {
            "client_id": 1,
            "geo_layer_url": "https://gis.detroitmi.gov",
            })

        expected = {
            'id': 1,
            'day': '2019-11-05T00:00:00.000Z',
            'geo_layer_url': 'https://gis.detroitmi.gov',
            'formatter': 'ElectionFormatter',
            'locations': {},
            'messages': [{'id': 1, 'lang': 'en', 'message': 'Reminder: today is election day.  Your polling location is {name}, located at {location} - open in maps: https://www.google.com/maps/search/?api=1&query={lat},{lng}'}]
        }

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, expected, "Notification gets added")

    def test_update_notification_invalid_notification(self):
        "Test adding a notification with invalid notification id"

        c = Client()
        response = c.post('/messenger/clients/1/notifications/99/', {
            "client_id": "invalid",
            "day": "2019/11/05"
            })

        self.assertEqual(response.status_code, 404)
        self.assertEqual({'error': 'Client invalid not found'}, response.json())

    def test_get_clients(self):
        "Test returning all notifications for all clients"

        c = Client()
        response = c.get('/messenger/clients/')

        expected = [{
                'id': 1,
                'name': 'elections',
                'description': 'Elections Messenger',
                'confirmation_message': 'You will receive elections reminders for the address {street_address}'
            }]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected, "Notifications get returned")

    def test_get_notifications(self):
        "Test returning all notifications for a client"

        c = Client()
        response = c.get('/messenger/clients/1/')

        expected = {
            'client': {
                'id': 1,
                'name': 'elections',
                'description': 'Elections Messenger',
                'confirmation_message': 'You will receive elections reminders for the address {street_address}'
            },
            'notifications': [
                {
                    'id': 1,
                    'day': '2019-11-05T00:00:00.000Z',
                    'geo_layer_url': 'https://services2.arcgis.com/qvkbeam7Wirps6zC/arcgis/rest/services/Elections_2019/FeatureServer/0/query?where=1%3D1&objectIds=&time=&geometry={lng}%2C+{lat}&geometryType=esriGeometryPoint&inSR=4326&spatialRel=esriSpatialRelIntersects&resultType=none&distance=0.0&units=esriSRUnit_Meter&returnGeodetic=false&outFields=*&returnGeometry=false&returnCentroid=false&featureEncoding=esriDefault&multipatchOption=xyFootprint&maxAllowableOffset=&geometryPrecision=&outSR=&datumTransformation=&applyVCSProjection=false&returnIdsOnly=false&returnUniqueIdsOnly=false&returnCountOnly=false&returnExtentOnly=false&returnQueryGeometry=false&returnDistinctValues=false&cacheHint=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&having=&resultOffset=&resultRecordCount=&returnZ=false&returnM=false&returnExceededLimitFeatures=true&quantizationParameters=&sqlFormat=none&f=pjson&token=',
                    'formatter': 'ElectionFormatter',
                    'locations': {},
                    'messages': [
                        {
                            'id': 1,
                            'lang': 'en',
                            'message': 'Reminder: today is election day.  Your polling location is {name}, located at {location} - open in maps: https://www.google.com/maps/search/?api=1&query={lat},{lng}'
                        }
                    ]
                }
            ]
        }

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected, "Notifications get returned")

    def test_get_notifications_invalid_client(self):
        "Test returning all notifications for a client with invalid client id"

        c = Client()
        response = c.get('/messenger/notifications/99/')
        self.assertEqual(response.status_code, 404)

    def test_add_message(self):
        "Test adding a message"

        c = Client()
        response = c.post('/messenger/notifications/1/messages/', { "lang": "en", "message": "Get out the vote!" })

        expected = { 'id': 2, 'lang': 'en', 'message': 'Get out the vote!' }
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, expected, "Notifications get returned")

    def test_add_message_invalid_notification(self):
        "Test adding a message with invalid notification"

        c = Client()
        response = c.post('/messenger/notifications/99/messages/', { "lang": "en", "message": "Get out the vote!" })
        self.assertEqual(response.status_code, 404)

    def test_add_message_missing_msg(self):
        "Test adding a message with missing msg"

        c = Client()
        response = c.post('/messenger/notifications/1/messages/', { "lang": "en" })
        self.assertEqual(response.status_code, 400)

    def test_update_message(self):
        "Test updating a message"

        c = Client()
        response = c.post('/messenger/notifications/1/messages/1/', { "lang": "en", "message": "Get out the vote!" })

        expected = { 'id': 1, 'lang': 'en', 'message': 'Get out the vote!' }
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, expected, "Notifications get returned")
