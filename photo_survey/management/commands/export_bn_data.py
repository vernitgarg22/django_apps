import csv
import requests
from requests.auth import HTTPBasicAuth

from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError

from photo_survey.models import ParcelMetadata, SurveyType, Survey
from assessments.models import ParcelMaster

from cod_utils.messaging import MsgHandler


def get_user_name(user):
    """
    Return properly-formatted user name.
    """

    name = user.first_name if user.first_name else ''
    if user.last_name:
        if name:
            name = name + ' '
        name = name + user.last_name
    return name


def init_user_name(user):
    """
    Try to init user info.
    """

    auth_values = tuple(settings.CREDENTIALS['BRIDGING_NEIGHBORHOODS'].values())

    url = "https://bridgingneighborhoods.org/user/{}?_format=json".format(user.username)
    response = requests.get(url, auth=HTTPBasicAuth(*auth_values))
    if response.status_code != 200:
        return False

    data = response.json()
    names = data['field_full_name'][0]['value'].split(' ')
    if not names:
        return False

    if len(names) < 2:
        user.last_name = names[0]
    else:
        user.first_name = names[0]
        user.last_name = names[1]

    user.save()
    return True


class ParcelFavoriteMap():

    def __init__(self):
        self.map = {}

    def add(self, user, parcel):

        if not self.map.get(user.id):
            self.map[user.id] = {}
        self.map[user.id][parcel.parcel_id] = True

    def exists(self, user, parcel):

        if self.map.get(user.id):
            return self.map[user.id].get(parcel.parcel_id)
        return False


class Command(BaseCommand):
    help = """
        Use this to export bridging neighborhoods data, e.g.,
        python manage.py export_bn_data"""

    def add_arguments(self, parser):
        parser.add_argument('output_file', type=str, help="Output file")
        parser.add_argument('--export_username', type=str, help="Output username [y|n]", default='n')
        parser.add_argument('--export_survey_id', type=str, help="Output survey id [y|n]", default='n')

    field_names = [ 'Email', 'Full Name', 'Address', 'Date Selected', 'Ranking', 'Confirmed' ]

    def handle(self, *args, **options):

        filename = options['output_file']
        export_username = options['export_username'] == 'y'
        export_survey_id = options['export_survey_id'] == 'y'

        if settings.DEBUG:
            export_username = True
            export_survey_id = True

        ignored_users = [ 0, 81, 86, 91, 92, 96, 101, 126, 131, 216, 9999 ]

        ignored_addresses = {
            "2007 OAKDALE": None,
            "2408 RIEDEN": None,
            "4111 BUCKINGHAM": None,
            "6711 ASHTON": None,
            "13517 OHIO": None,
        }

        if export_username:
            self.field_names.append('Username')
        if export_survey_id:
            self.field_names.append('Survey id')

        survey_type = SurveyType.objects.get(survey_template_id = 'bridging_neighborhoods')

        surveys = survey_type.survey_set.exclude(status='deleted').order_by('-created_at', 'user_id')

        parcel_map = ParcelFavoriteMap()
        missing_emails = {}

        with open(filename, 'w', newline='') as csvfile:

            writer = csv.DictWriter(csvfile, fieldnames=self.field_names)
            writer.writeheader()

            for survey in surveys:

                user = survey.user

                if int(user.username) not in ignored_users:

                    # First check if we need to try to init user name.
                    if not get_user_name(user) and not init_user_name(user):
                        continue

                    if len(survey.survey_answers) < 3:
                        continue

                    ranking = survey.survey_answers[2]

                    confirmed = None
                    if len(survey.survey_answers) == 4 and survey.survey_answers[3].answer != 'Please Confirm Your Selections.':
                        confirmed = survey.survey_answers[3]

                    parcel = survey.parcel
                    parcel_master = ParcelMaster.objects.get(pnum = parcel.parcel_id)

                    # Now try to output our information.
                    if not get_user_name(user) and not user.email:
                        missing_emails[int(user.username)] = True
                    elif (parcel_map.exists(user, parcel) or survey.status == 'deleted') and not confirmed:
                        continue
                    elif parcel_master.propstreetcombined in ignored_addresses:
                        print("ignoring address " + parcel_master.propstreetcombined)
                        ignored_addresses[parcel_master.propstreetcombined] = parcel.parcel_id
                    elif not missing_emails:

                        parcel_map.add(user, parcel)
                        data = {
                            'Email': user.email,
                            'Full Name': get_user_name(user),
                            'Address': parcel_master.propstreetcombined,
                            'Date Selected': survey.created_at.strftime("%b %d, %Y"),
                            'Ranking': int(ranking.answer) + 1,
                            'Confirmed': confirmed.answer if confirmed else 'No',
                        }

                        if export_username:
                            data['Username'] = user.username

                        if export_survey_id:
                            data['Survey id'] = survey.id

                        writer.writerow(data)

            for address, parcel_id in ignored_addresses.items():
                if not parcel_id:
                    print("Address " + address + " did not get ignored properly")
                else:
                    print("parcel_id: " + parcel_id)

            if missing_emails:
                msg = "User ids {} need email added".format(list(missing_emails.keys()))
                MsgHandler().send_admin_alert(text=msg)
                raise CommandError(msg)
