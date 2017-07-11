import csv
from datetime import datetime

from django.core.management.base import BaseCommand, CommandError

from photo_survey.models import Survey, SurveyAnswer, SurveyQuestion


class Command(BaseCommand):
    help = """
        Use this to export survey answers to csv, e.g.,
        python manage.py export_survey_answers survey_template_id """

    def add_arguments(self, parser):
        parser.add_argument('survey_template_id', type=str)

    def init_metadata(self, options):
        """
        Initializes internal data to do the export.
        """

        self.using_db='photo_survey'
        self.survey_template_id = options['survey_template_id']
        self.questions = SurveyQuestion.objects.using(self.using_db).filter(survey_template_id=self.survey_template_id).order_by('question_number')
        now = datetime.now()
        self.out_file = now.strftime("%Y%m%d_%H%M%S.csv")
        self.num_exported = 0

    def get_data(self):
        """
        Retrieve all the survey answers.
        """

        self.surveys = Survey.objects.using(self.using_db).filter(survey_template_id=self.survey_template_id).order_by('parcel_id')
        self.answers = SurveyAnswer.objects.using(self.using_db).all()

    def export_data(self):
        """
        Export the actual data
        """

        with open(self.out_file, 'w', newline='') as csvfile:

            fieldnames = [ 'parcel', 'surveyor', 'common_name', 'note', 'status', 'created_at' ] + [ question.question_id for question in self.questions ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for survey in self.surveys:
                id = survey.id
                curr_answers = [ answer for answer in self.answers if answer.survey_id == id ]
                if curr_answers:
                    answer_data = { 'parcel': survey.parcel_id, 'surveyor': survey.user.username, 'common_name': survey.common_name, 'note': survey.note, 'status': survey.status, 'created_at': survey.created_at }
                    answer_data.update( { answer.question_id: answer.answer for answer in curr_answers } )
                    writer.writerow(answer_data)

                    self.num_exported = self.num_exported + len(curr_answers)

    def handle(self, *args, **options):

        self.init_metadata(options)

        self.get_data()

        self.export_data()

        return "Exported {} rows to {}".format(self.num_exported, self.out_file)
