import csv
from datetime import datetime

from django.core.management.base import BaseCommand, CommandError

from photo_survey.models import Survey, SurveyAnswer, SurveyQuestion
from assessments.models import ParcelMaster


class Command(BaseCommand):
    help = """
        Use this to export survey answers to csv, e.g.,
        python manage.py export_survey_answers survey_template_id """

    def add_arguments(self, parser):
        parser.add_argument('survey_template_id', type=str, help='Identifies the survey type')
        parser.add_argument('--pretty_print', default='y', help='Pretty print values')
        parser.add_argument('--add_data', default='ownership', help='Comma-delimited set of types of data to add')

    def init_metadata(self, options):
        """
        Initializes internal data to do the export.
        """

        # First parse out command-line options
        self.pretty_print = options['pretty_print'] == 'y'
        tmp = options.get('add_data', '')
        self.data_types = { data_type: True for data_type in tmp.split(',') }
        self.survey_template_id = options['survey_template_id']

        # Now finish initializing everything
        self.using_db='photo_survey'
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

    def cache_data(self):
        """
        Pre-fetch data, wherever helpful.
        """

        survey_ids = { survey.parcel_id for survey in self.surveys }
        parcels_tmp = ParcelMaster.objects.filter(pnum__in=list(survey_ids))
        self.parcels = { parcel.pnum: parcel for parcel in parcels_tmp }

    def get_fieldnames(self):
        """
        Returns correct header row column names.
        """

        field_names = [ 'parcel', 'surveyor', 'common_name', 'note', 'status', 'created_at' ] + [ question.question_id for question in self.questions ]
        if self.data_types.get('ownership', False):
            field_names.extend( [ 'owner name', 'owner address', 'owner city', 'owner state', 'owner zip' ] )

        return field_names

    def get_answerdata(self, survey):
        """
        Returns answer data for a given survey.
        """

        curr_answers = [ answer for answer in self.answers if answer.survey_id == survey.id ]
        if not curr_answers:
            return None

        # Get basic information about the survey itself
        answer_data = { 'parcel': survey.parcel_id, 'surveyor': survey.user.username, 'common_name': survey.common_name, 'note': survey.note, 'status': survey.status, 'created_at': survey.created_at }

        # Get the answers
        answer_data_tmp = { answer.question_id: answer.answer for answer in curr_answers }

        # TODO pretty print the answers?
        # if self.pretty_print:

        answer_data.update(answer_data_tmp)

        # Get the ownership data?
        if self.data_types.get('ownership', False):
            parcel = self.parcels.get(survey.parcel_id, None)
            if parcel:
                owner_name = parcel.ownername1
                if parcel.ownername2:
                    owner_name = owner_name + ' - ' + parcel.ownername2
                answer_data['owner name'] = owner_name
                answer_data['owner address'] = parcel.ownerstreetaddr
                answer_data['owner city'] = parcel.ownercity
                answer_data['owner state'] = parcel.ownerstate
                answer_data['owner zip'] = parcel.ownerzip

        return answer_data

    def export_data(self):
        """
        Export the actual data
        """

        with open(self.out_file, 'w', newline='') as csvfile:

            fieldnames = self.get_fieldnames()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for survey in self.surveys:
                answer_data = self.get_answerdata(survey)
                if answer_data:
                    writer.writerow(answer_data)
                    self.num_exported = self.num_exported + 1

                    if self.num_exported % 100 == 0:
                        self.stdout.write("{} rows exported ...".format(self.num_exported))
                        self.stdout.flush()

    def handle(self, *args, **options):

        self.init_metadata(options)

        self.get_data()

        self.cache_data()

        self.export_data()

        return "Exported answers for {} surveys to {}".format(self.num_exported, self.out_file)
