import csv

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError

from photo_survey.models import ParcelMetadata, SurveyType, Survey
from assessments.models import ParcelMaster


def get_user_name(user):
    """
    Return properly-formatted user name.
    """

    return user.first_name + user.last_name


class Command(BaseCommand):
    help = """
        Use this to export bridging neighborhoods data, e.g.,
        python manage.py export_bn_data"""

    def add_arguments(self, parser):
        parser.add_argument('output_file', type=str, help="Output file")

    field_names = [ 'Email', 'Full Name', 'Address', 'Date Selected', 'Ranking' ]

    def handle(self, *args, **options):

        filename = options['output_file']

        ignored_users = [ 44, 46, 47, 1047, 1048, 1049, 1051, 1052, 1054 ]

        survey_type = SurveyType.objects.get(survey_template_id = 'bridging_neighborhoods')

        surveys = survey_type.survey_set.all().order_by('-created_at', 'user_id')

        existing_surveys = {}
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
                    elif existing_surveys.get(parcel.parcel_id) or survey.status == 'deleted':
                        continue
                    elif not missing_emails:

                        existing_surveys[parcel.parcel_id] = True
                        data = {
                            'Email': user.email,
                            'Full Name': get_user_name(user),
                            'Address': parcel_master.propstreetcombined,
                            'Date Selected': survey.created_at.strftime("%b %d, %Y"),
                            'Ranking': int(ranking.answer) + 1,
                        }

                        writer.writerow(data)

            if missing_emails:
                raise CommandError("User ids {} need email added".format(list(missing_emails.keys())))
