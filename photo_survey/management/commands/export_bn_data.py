import csv

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError

from photo_survey.models import ParcelMetadata, SurveyType, Survey
from assessments.models import ParcelMaster


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

        with open(filename, 'w', newline='') as csvfile:

            writer = csv.DictWriter(csvfile, fieldnames=self.field_names)
            writer.writeheader()

            for survey in surveys:

                if int(survey.user_id) not in ignored_users:

                    user = survey.user
                    parcel = survey.parcel
                    parcel_master = ParcelMaster.objects.filter(pnum = parcel.parcel_id).first()
                    ranking = survey.survey_answers[2]

                    if not user.email:
                        raise CommandError("User id {} needs email added".format(user.id))

                    if existing_surveys.get(parcel.parcel_id) or survey.status == 'deleted':
                        continue

                    existing_surveys[parcel.parcel_id] = True

                    data = { 
                        'Email': user.email,
                        'Full Name': user.first_name + ' ' + user.last_name,
                        'Address': parcel_master.propstreetcombined,
                        'Date Selected': survey.created_at.strftime("%b %d, %Y"),
                        'Ranking': int(ranking.answer) + 1,
                    }

                    writer.writerow(data)
