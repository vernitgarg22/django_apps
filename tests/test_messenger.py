import datetime
from datetime import date, timedelta
import requests

from django.test import Client, TestCase
import mock
from unittest.mock import MagicMock, patch
from django.core.management import call_command
from django.utils.six import StringIO
from django.core.management.base import CommandError

from rest_framework.exceptions import NotFound, PermissionDenied

from tests import test_util

from messenger import views
from messenger.views import get_existing_object
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

GEO_LAYER_URL="https://services2.arcgis.com/qvkbeam7Wirps6zC/arcgis/rest/services/Elections_2019/FeatureServer/0/query?where=&objectIds=&time=&geometry={lng}%2C+{lat}&geometryType=esriGeometryPoint&inSR=4326&spatialRel=esriSpatialRelWithin&resultType=none&distance=0.0&units=esriSRUnit_Meter&returnGeodetic=false&outFields=*&returnGeometry=false&returnCentroid=false&multipatchOption=xyFootprint&maxAllowableOffset=&geometryPrecision=&outSR=4326&datumTransformation=&applyVCSProjection=false&returnIdsOnly=false&returnUniqueIdsOnly=false&returnCountOnly=false&returnExtentOnly=false&returnDistinctValues=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&having=&resultOffset=&resultRecordCount=&returnZ=false&returnM=false&returnExceededLimitFeatures=true&quantizationParameters=&sqlFormat=none&f=pjson"


def setup_messenger():

    # url="https://services2.arcgis.com/qvkbeam7Wirps6zC/arcgis/rest/services/Elections_2019/FeatureServer/0/query?where=1%3D1&objectIds=&time=&geogeometry={lng}%2C+{lat}&geometryType=esriGeometryPoint&inSR=4326&spatialRel=esriSpatialRelIntersects&resultType=none&distance=0.0&units=esriSRUnit_Meter&returnGeodetic=false&outFields=*&returnGeometry=false&returnCentroid=false&featureEncoding=esriDefault&multipatchOption=xyFootprint&maxAllowableOffset=&geometryPrecision=&outSR=&datumTransformation=&applyVCSProjection=false&returnIdsOnly=false&returnUniqueIdsOnly=false&returnCountOnly=false&returnExtentOnly=false&returnQueryGeometry=false&returnDistinctValues=false&cacheHint=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&having=&resultOffset=&resultRecordCount=&returnZ=false&returnM=false&returnExceededLimitFeatures=true&quantizationParameters=&sqlFormat=none&f=pjson&token="

    client = MessengerClient(name='Elections', description='Elections Messenger', confirmation_message="You will receive elections reminders for the address {street_address}")
    client.save()
    phone_number = MessengerPhoneNumber(messenger_client=client, phone_number='5005550006', description='Test phone number')
    phone_number.save()

    for location in [ 48214 ]:
        MessengerLocation(location_type="ZIP Code", prefix="zipcode", value=location).save()

    notification = MessengerNotification(messenger_client=client, day=datetime.date(year=2019, month=11, day=5),
      geo_layer_url=GEO_LAYER_URL, formatter='ElectionFormatter')
    notification.save()
    notification.locations.add(MessengerLocation.objects.first())
    message = MessengerMessage(messenger_notification=notification,
      message='Reminder: today is election day.  Your polling location is {name}, located at {location} - open in maps: https://www.google.com/maps/search/?api=1&query={lat},{lng}')
    message.save()

def setup_subscriber(**kwargs):

    phone_number = kwargs.get("phone_number", "+15005550006")
    status = kwargs.get("status", "active")
    address = kwargs.get("address", "7840 Van Dyke Pl")
    lang = kwargs.get("lang", "en")

    subscriber = MessengerSubscriber(phone_number=phone_number, status=status, address=address, lang=lang)
    subscriber.save()

    client = MessengerClient.objects.first()
    if client:
        subscriber.messenger_clients.add(client)

    return subscriber


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

        expected = {'received': {'phone_number': '5005550006', 'address': '7840 VAN DYKE PL'}, 'message': 'New Elections subscriber created'}
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

    # Test subscribing from web page
    def test_subscribe_web(self):
        "Test subscribing from webpage"

        with patch.object(messaging.MsgHandler, 'send_text') as mock_method:

            c = Client()
            response = c.post('/messenger/clients/1/subscribe/', { "phone_number": "5005550006", "address": "7840 Van Dyke Pl" })

        mock_method.assert_called_once_with(phone_number='5005550006', text="Please reply with 'add me' to confirm you would like to receive alerts from Elections")

        expected = {'received': {'phone_number': '5005550006', 'address': '7840 VAN DYKE PL'}, 'message': 'New Elections subscriber created'}
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, expected, "Subscription signup returns correct message")
        self.assertEqual(MessengerSubscriber.objects.first().status, "inactive", "Subscriber needs to confirm")

    # Test subscribing from web page with address missing
    def test_subscribe_web_missing_address(self):
        "Test subscribing from webpage with address missing"

        c = Client()
        response = c.post('/messenger/clients/1/subscribe/', { "phone_number": "5005550006" })

        expected = {'error': 'Address and phone number are required'}
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, expected, "Subscription signup returns correct message")

    # Test confirming subscription
    def test_confirm_subscription(self):
        "Test confirming subscription"

        setup_subscriber()

        with patch.object(messaging.MsgHandler, 'send_text') as mock_method, patch.object(RequestValidator, 'validate') as mock_validate:
            mock_validate.return_value = True

            c = Client()
            response = c.post('/messenger/clients/1/confirm/', TEXT_DATA)

        mock_method.assert_called_once_with(phone_number='5005550006', text='Your Elections alerts have been activated')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(MessengerSubscriber.objects.first().status, "active", "Subscriber got activated")

    def test_confirm_subscription_invalid_user(self):
        "Test confirming subscription with invalid user"

        with patch.object(messaging.MsgHandler, 'send_text') as mock_method, patch.object(RequestValidator, 'validate') as mock_validate:
            mock_validate.return_value = True

            c = Client()
            response = c.post('/messenger/clients/1/confirm/', TEXT_DATA)

        self.assertEqual(response.status_code, 404)

    def test_confirm_subscription_missing_message(self):
        "Test confirming subscription with user message missing"

        setup_subscriber()

        with patch.object(messaging.MsgHandler, 'send_text') as mock_method, patch.object(RequestValidator, 'validate') as mock_validate:
            mock_validate.return_value = True

            c = Client()
            response = c.post('/messenger/clients/1/confirm/', {"From": "15005550006"})

        mock_method.assert_not_called()
        self.assertEqual(response.status_code, 400)

    def test_send_messages(self):
        "Test sending a basic formatted message"

        setup_subscriber()

        out = StringIO()

        with patch.object(messaging.MsgHandler, 'send_text') as mock_method:

            call_command('send_messages', 'Elections', '--today=20191105', stdout=out)

        message = 'Reminder: today is election day.  Your polling location is MAR. GARVEY ACADEMY, located at 2301 VAN DYKE ST. - open in maps: https://www.google.com/maps/search/?api=1&query=42.35972900000,-83.00074500000'
        mock_method.assert_called_once_with(phone_number='5005550006', text=message)

    def test_send_messages_citywide(self):
        "Test sending a message to subscribers citywide"

        location = MessengerLocation.objects.first()
        location.prefix = 'citywide'
        location.location_type = 'Citywide'
        location.save()

        notification = MessengerNotification.objects.first()
        notification.geo_layer_url = None
        notification.save()

        message = MessengerMessage.objects.first()
        message.message = "Don't forget to vote today!"
        message.save()

        setup_subscriber()

        out = StringIO()

        with patch.object(messaging.MsgHandler, 'send_text') as mock_method:

            call_command('send_messages', 'Elections', '--today=20191105', stdout=out)

        mock_method.assert_called_once_with(phone_number='5005550006', text="Don't forget to vote today!")

    def test_send_messages_multi_lang(self):
        "Test sending a basic formatted message with multi-language support"

        message = MessengerMessage(messenger_notification=MessengerNotification.objects.first(), lang='es',
            message='Recordatorio: hoy es el día de las elecciones. Su lugar de votación es {name}, situado en {location} - abrir en mapas: https://www.google.com/maps/search/?api=1&query={lat},{lng}')
        message.save()

        setup_subscriber(lang="es")

        out = StringIO()

        with patch.object(messaging.MsgHandler, 'send_text') as mock_method:

            call_command('send_messages', 'Elections', '--today=20191105', stdout=out)

        message = 'Recordatorio: hoy es el día de las elecciones. Su lugar de votación es MAR. GARVEY ACADEMY, situado en 2301 VAN DYKE ST. - abrir en mapas: https://www.google.com/maps/search/?api=1&query=42.35972900000,-83.00074500000'
        mock_method.assert_called_once_with(phone_number='5005550006', text=message)

    def test_send_messages_simple(self):
        "Test sending a message with no geo layer (just the message itself"

        notification = MessengerNotification.objects.first()
        notification.geo_layer_url = None
        notification.save()

        messenger_message = notification.messengermessage_set.first()
        messenger_message.message = "Don't forget to vote today!"
        messenger_message.save()

        setup_subscriber()

        out = StringIO()

        with patch.object(messaging.MsgHandler, 'send_text') as mock_method:

            call_command('send_messages', 'Elections', '--today=20191105', stdout=out)

        message = "Don't forget to vote today!"
        mock_method.assert_called_once_with(phone_number='5005550006', text=message)

    def test_send_messages_dhsem(self):
        "Test sending a message for DHSEM"

        client = MessengerClient.objects.first()
        client.name = 'DHSEM'
        client.save()

        notification = MessengerNotification.objects.first()
        notification.geo_layer_url = None
        notification.formatter = 'DHSEMFormatter'
        notification.save()

        messenger_message = notification.messengermessage_set.first()
        messenger_message.message = "Please wear sunscreen and seek shelter during the heatwave"
        messenger_message.save()

        setup_subscriber()

        out = StringIO()

        with patch.object(messaging.MsgHandler, 'send_text') as mock_method:

            call_command('send_messages', 'DHSEM', '--today=20191105', stdout=out)

        message = "Please wear sunscreen and seek shelter during the heatwave"
        mock_method.assert_called_once_with(phone_number='5005550006', text=message)

    def test_send_message_subscriber_outside_geo(self):
        "Test sending messages when subscriber is outside notification's polygon"

        subscriber = MessengerSubscriber(phone_number='+15005550006', status='active',
            address='132 Dikeman Street Ann Arbor, MI', latitude='42.201225', longitude='-83.150925')
        super(MessengerSubscriber, subscriber).save()

        subscriber.messenger_clients.add(MessengerClient.objects.first())

        messages_meta = send_messages(client_name='Elections', day=date(2019, 11, 5))
        self.assertEqual('\nclient: Elections\nday:    2019-11-05\n\nnotifications:  (No notifications sent)', messages_meta.describe(), "No messages can be sent")

    def test_send_messages_no_notifications(self):

        test_util.cleanup_model(MessengerMessage)
        test_util.cleanup_model(MessengerNotification)

        setup_subscriber()

        messages_meta = send_messages(client_name='Elections', day=date(2019, 11, 5))
        self.assertEqual('\nclient: Elections\nday:    2019-11-05\n\nnotifications:  (No notifications sent)', messages_meta.describe(), "No messages can be sent")

    def test_send_messages_no_message(self):
        "Test sending a message with no message set in database"

        test_util.cleanup_model(MessengerMessage)

        setup_subscriber()

        out = StringIO()
        with self.assertRaises(NotificationException):

            call_command('send_messages', 'Elections', '--today=20191105', stdout=out)

    def test_send_messages_no_formatter(self):

        notification = MessengerNotification.objects.first()
        notification.formatter = None
        notification.save()

        setup_subscriber()

        out = StringIO()
        with self.assertRaises(NotificationException):

            call_command('send_messages', 'Elections', '--today=20191105', stdout=out)

    def test_send_messages_invalid_formatter(self):

        notification = MessengerNotification.objects.first()
        notification.formatter = "invalid"
        notification.save()

        setup_subscriber()

        out = StringIO()
        with self.assertRaises(NotificationException):

            call_command('send_messages', 'Elections', '--today=20191105', stdout=out)

    def test_send_messages_invalid_client_name(self):

        out = StringIO()
        with self.assertRaises(CommandError):

            call_command('send_messages', 'invalid', '--today=20191105', stdout=out)

    def test_send_messages_invalid_geo_layer_url(self):

        setup_subscriber()

        class MockedResponse():

            def __init__(self):
                self.ok = False

        with patch.object(requests, 'get') as mocked_requests_get, self.assertRaises(NotificationException):
            mocked_requests_get.return_value = MockedResponse()

            out = StringIO()
            call_command('send_messages', 'Elections', '--today=20191105', stdout=out)

    def test_send_messages_invalid_dryrun_param(self):

        out = StringIO()
        with self.assertRaises(CommandError):

            call_command('send_messages', 'Elections', '--today=20191105', '--dry_run=maybe', stdout=out)

    def test_send_messages_invalid_date_param(self):

        out = StringIO()
        with self.assertRaises(CommandError):

            call_command('send_messages', 'Elections', '--today=201911050', stdout=out)

    def test_get_object_null_id(self):

        with self.assertRaises(NotFound):

            get_existing_object(cl_type=MessengerClient, obj_id=None, cl_name="Client", required=True)

    def test_get_object_invalid_id(self):

        with self.assertRaises(NotFound):

            get_existing_object(cl_type=MessengerClient, obj_id="invalid", cl_name="Client")


class MessengerSubscriberValidationTests(TestCase):

    def setUp(self):
        """
        Set up each unit test, including making sure database is properly cleaned up before each test
        """

        test_util.cleanup_model(MessengerSubscriber)

    def test_validate_address(self):

        with self.assertRaises(ValidationError):

            MessengerSubscriber(address="100 Invalid Street").save()

    def test_validate_phone_number(self):

        subscriber = setup_subscriber()
        subscriber.phone_number = "48214"

        with self.assertRaises(ValidationError):
            subscriber.validate()

    def test_validate_status(self):

        subscriber = setup_subscriber()
        subscriber.status = "invalid"

        with self.assertRaises(ValidationError):
            subscriber.validate()

    def test_validate_address2(self):

        subscriber = setup_subscriber()
        subscriber.address = "48226"

        with self.assertRaises(ValidationError):
            subscriber.validate()

    def test_validate_lat_long(self):

        subscriber = setup_subscriber()
        subscriber.latitude = ''
        subscriber.longitude = ''

        with self.assertRaises(ValidationError):
            subscriber.validate()

    def test_validate_lang(self):

        subscriber = setup_subscriber()
        subscriber.lang = "foobar"

        with self.assertRaises(ValidationError):
            subscriber.validate()

    def test_validate_timestamps(self):

        subscriber = setup_subscriber()
        subscriber.last_status_update = subscriber.created_at - timedelta(days=1)

        with self.assertRaises(ValidationError):
            subscriber.validate()


class MessengerDashboardTests(MessengerBaseTests):

    def test_add_notification(self):
        "Test adding a notification"

        c = Client()
        response = c.post('/messenger/clients/1/notifications/', {
            "day": "2019/11/05",
            "geo_layer_url": GEO_LAYER_URL,
            "formatter": "ElectionFormatter"
            })

        expected = {
            'id': 2,
            'day': '2019-11-05T00:00:00.000Z',
            'geo_layer_url': GEO_LAYER_URL,
            'formatter': 'ElectionFormatter',
            'locations': {},
            'messages': []
        }

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, expected, "Notification gets added")

    def test_get_all_locations(self):
        "Test returning all locations"

        for location in [ 1, 2 ]:
            MessengerLocation(location_type="DHSEM Evacuation Zone", prefix='dhsem_evac_zone', value=location).save()

        c = Client()
        response = c.get('/messenger/locations/')

        expected = {
            'dhsem_evac_zone': {
                'description': 'DHSEM Evacuation Zone',
                'values': ['1', '2']
            },
            'zipcode': {
                    'description': 'ZIP Code',
                    'values': ['48214']
            }
        }

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected, "Locations get returned")

    def test_get_location_notifications(self):
        "Test returning notifications for a given location"

        c = Client()
        response = c.get('/messenger/clients/1/locations/zipcode/48214/notifications/')

        expected = {
            'location': {
                'location_type': 'ZIP Code',
                'prefix': 'zipcode',
                'value': '48214'
            },
            'notifications': [
                {
                    'id': 1,
                    'day': '2019-11-05T00:00:00.000Z',
                    'geo_layer_url': GEO_LAYER_URL,
                    'formatter': 'ElectionFormatter',
                    'messages': [
                        {
                            'id': 1,
                            'lang': 'en',
                            'message': 'Reminder: today is election day.  Your polling location is {name}, located at {location} - open in maps: https://www.google.com/maps/search/?api=1&query={lat},{lng}'
                        }
                    ],
                    'locations': {'zipcode': {'description': 'ZIP Code', 'values': ['48214']}}
                }
            ]
        }

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected, "Locations get returned")

    def test_get_location_notifications_invalid_location(self):
        "Test returning notifications for an invalid location"

        c = Client()
        response = c.get('/messenger/clients/1/locations/zipcode/99/notifications/')

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, { "error": "zipcode 99 not found"})

    def test_add_notification_location(self):
        "Test adding a notification with a location"

        for location in [ 48226 ]:
            MessengerLocation(location_type="ZIP Code", prefix='zipcode', value=location).save()

        cl = Client()
        response = cl.post('/messenger/clients/1/notifications/', {
            "day": "2019/11/05",
            "geo_layer_url": GEO_LAYER_URL,
            "formatter": "ElectionFormatter",
            "location_prefix": "zipcode",
            "locations": [ 48214, 48226 ]
            })

        expected = {
            'id': 2,
            'day': '2019-11-05T00:00:00.000Z',
            'geo_layer_url': GEO_LAYER_URL,
            'formatter': 'ElectionFormatter',
            'locations': {'zipcode': {'description': 'ZIP Code', 'values': ['48214', '48226']}},
            'messages': []
        }

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, expected, "Notification gets added")

    def test_add_invalid_notification_location(self):
        "Test adding a notification with an invalid location"

        cl = Client()
        response = cl.post('/messenger/clients/1/notifications/', {
            "day": "2019/11/05",
            "geo_layer_url": GEO_LAYER_URL,
            "formatter": "ElectionFormatter",
            "location_prefix": "zipcode",
            "locations": [ 10001 ]
            })

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {'error': 'zipcode with value 10001 is invalid '}, "Invalid locations are rejected")

    def test_add_notification_invalid_client(self):
        "Test adding a notification with invalid client id"

        c = Client()
        response = c.post('/messenger/clients/99/notifications/', {
            "day": "2019/11/05"
            })

        self.assertEqual(response.status_code, 404)
        self.assertEqual({'error': 'Client 99 not found'}, response.json())

    def test_add_notification_invalid_day(self):
        "Test adding a notification with invalid day format"

        c = Client()
        response = c.post('/messenger/clients/1/notifications/', {
            "day": "2019/11/5"
            })

        self.assertEqual(response.status_code, 400)

    def test_add_notification_missing_day(self):
        "Test adding a notification with invalid day format"

        c = Client()
        response = c.post('/messenger/clients/1/notifications/', {})

        self.assertEqual(response.status_code, 400)

    def test_update_notification(self):
        "Test updating a notification"

        c = Client()
        response = c.post('/messenger/clients/1/notifications/1/', {
            "day": "2019/11/05",
            "geo_layer_url": GEO_LAYER_URL,
            "formatter": "ElectionFormatter"
            })

        expected = {
            'id': 1,
            'day': '2019-11-05T00:00:00.000Z',
            'geo_layer_url': GEO_LAYER_URL,
            'formatter': 'ElectionFormatter',
            'locations': {'zipcode': {'description': 'ZIP Code', 'values': ['48214']}},
            'messages': [{'id': 1, 'lang': 'en', 'message': 'Reminder: today is election day.  Your polling location is {name}, located at {location} - open in maps: https://www.google.com/maps/search/?api=1&query={lat},{lng}'}]
        }

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, expected, "Notification gets added")

    def test_update_notification_geo_only(self):
        "Test updating a notification"

        c = Client()
        response = c.post('/messenger/clients/1/notifications/1/', {
            "geo_layer_url": "https://gis.detroitmi.gov",
            })

        expected = {
            'id': 1,
            'day': '2019-11-05T00:00:00.000Z',
            'geo_layer_url': 'https://gis.detroitmi.gov',
            'formatter': 'ElectionFormatter',
            'locations': {'zipcode': {'description': 'ZIP Code', 'values': ['48214']}},
            'messages': [{'id': 1, 'lang': 'en', 'message': 'Reminder: today is election day.  Your polling location is {name}, located at {location} - open in maps: https://www.google.com/maps/search/?api=1&query={lat},{lng}'}]
        }

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, expected, "Notification gets added")

    def test_update_notification_invalid_notification(self):
        "Test adding a notification with invalid notification id"

        c = Client()
        response = c.post('/messenger/clients/1/notifications/99/', {
            "day": "2019/11/05"
            })

        self.assertEqual(response.status_code, 404)
        self.assertEqual({'error': 'Notification 99 not found'}, response.json())

    def test_get_clients(self):
        "Test returning all notifications for all clients"

        c = Client()
        response = c.get('/messenger/clients/')

        expected = [{
                'id': 1,
                'name': 'Elections',
                'description': 'Elections Messenger',
                'confirmation_message': 'You will receive elections reminders for the address {street_address}'
            }]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected, "Notifications get returned")

    def test_get_notifications(self):
        "Test returning all notifications for a client"

        for location in [ 48214, 48226 ]:
            MessengerLocation(location_type="ZIP Code", prefix='zipcode', value=location).save()

        c = Client()
        response = c.get('/messenger/clients/1/')

        expected = {
            'client': {
                'id': 1,
                'name': 'Elections',
                'description': 'Elections Messenger',
                'confirmation_message': 'You will receive elections reminders for the address {street_address}'
            },
            'notifications': [
                {
                    'id': 1,
                    'day': '2019-11-05T00:00:00.000Z',
                    'geo_layer_url': GEO_LAYER_URL,
                    'formatter': 'ElectionFormatter',
                    'locations': {'zipcode': {'description': 'ZIP Code', 'values': ['48214']}},
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
