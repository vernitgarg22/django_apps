import csv

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError

from photo_survey.models import ParcelMetadata, SurveyType, Survey
from assessments.models import ParcelMaster


def get_user_name(user):
    """
    Return properly-formatted user name.
    """

    return user.first_name + " " + user.last_name


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

    field_names = [ 'Email', 'Full Name', 'Address', 'Date Selected', 'Ranking' ]

    def handle(self, *args, **options):

        filename = options['output_file']
        export_username = options['export_username'] == 'y'

        ignored_users = [ 44, 46, 47, 1047, 1048, 1049, 1051, 1052, 1054, 1067 ]

        if export_username:
            self.field_names.append('Username')

        survey_type = SurveyType.objects.get(survey_template_id = 'bridging_neighborhoods')

        surveys = survey_type.survey_set.all().order_by('-created_at', 'user_id')

        parcel_map = ParcelFavoriteMap()
        missing_emails = {}

        with open(filename, 'w', newline='') as csvfile:

            writer = csv.DictWriter(csvfile, fieldnames=self.field_names)
            writer.writeheader()

            for survey in surveys:

                if int(survey.user_id) not in ignored_users:

                    user = survey.user
                    parcel = survey.parcel
                    parcel_master = ParcelMaster.objects.filter(pnum = parcel.parcel_id).first()
                    ranking = survey.survey_answers[2]

                    if not get_user_name(user) and not user.email:
                        missing_emails[int(user.username)] = True
                    elif parcel_map.exists(user, parcel) or survey.status == 'deleted':
                        continue
                    elif not missing_emails:

                        parcel_map.add(user, parcel)
                        data = {
                            'Email': user.email,
                            'Full Name': get_user_name(user),
                            'Address': parcel_master.propstreetcombined,
                            'Date Selected': survey.created_at.strftime("%b %d, %Y"),
                            'Ranking': int(ranking.answer) + 1,
                        }

                        if export_username:
                            data['Username'] = user.username

                        writer.writerow(data)

            if missing_emails:
                raise CommandError("User ids {} need email added".format(list(missing_emails.keys())))
