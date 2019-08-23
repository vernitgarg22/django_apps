import csv

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from photo_survey.models import PublicPropertyData, Survey, SurveyType, SurveyAnswer, SurveyQuestion, SurveyQuestionAvailAnswer, ImageMetadata
from assessments.models import ParcelMaster

from cod_utils.util import split_csv


class Command(BaseCommand):
    help = """
        Use this to export survey answers to csv, e.g.,
        python manage.py export_survey_answers survey_template_id """


    def add_arguments(self, parser):
        parser.add_argument('survey_template_id', type=str, help='Identifies the survey type')
        parser.add_argument('--pretty_print', default='y', help='Pretty print values?')
        parser.add_argument('--remove_dupes', default='y', help='Only return most-recent survey for each parcel?')
        parser.add_argument('--add_data', default='ownership,address_info', help='Comma-delimited set of types of data to add')
        parser.add_argument('--calc_score', default='y', help='Calculate a score for each survey?')
        parser.add_argument('--add_streetview_link', default='y', help='Add a link to mapillary streetview?')

    def init_metadata(self, options):
        """
        Initializes internal data to do the export.
        """

        # First parse out command-line options
        self.pretty_print = options['pretty_print'] == 'y'
        self.remove_dupes = options['remove_dupes'] == 'y'
        self.calc_score = options['calc_score'] == 'y'
        self.add_streetview_link = options['add_streetview_link'] == 'y'
        tmp = options.get('add_data', '')
        self.data_types = { data_type: True for data_type in tmp.split(',') }
        self.survey_template_id = options['survey_template_id']

        # Now finish initializing everything
        self.questions = SurveyQuestion.objects.filter(survey_type__survey_template_id=self.survey_template_id).order_by('question_number')
        now = timezone.now()
        self.out_file = now.strftime("%Y%m%d_%H%M%S.csv")
        self.num_exported = 0

        if self.pretty_print:

            avail_answers_tmp = SurveyQuestionAvailAnswer.objects.filter(survey_question__survey_type__survey_template_id=self.survey_template_id)

            self.avail_answers = { avail_answer.survey_question.question_id: {} for avail_answer in avail_answers_tmp }
            for avail_answer in avail_answers_tmp:
                self.avail_answers[avail_answer.survey_question.question_id][avail_answer.value] = avail_answer.text

    def get_data(self):
        """
        Retrieve all the survey answers.
        """

        self.surveys = Survey.objects.filter(survey_type__survey_template_id=self.survey_template_id).order_by('id')
        if self.remove_dupes:
            survey_map = { survey.parcel.parcel_id: survey for survey in self.surveys }
            self.surveys = survey_map.values()

        self.answers = SurveyAnswer.objects.all()

        if self.data_types.get('ownership', False) or self.data_types.get('address_info', False):
            survey_parcel_ids = { survey.parcel.parcel_id for survey in self.surveys }
            parcels_tmp = ParcelMaster.objects.filter(pnum__in=list(survey_parcel_ids))
            self.parcels = { parcel.pnum: parcel for parcel in parcels_tmp }

            public_property_tmp = PublicPropertyData.objects.all()
            self.public_property = { public_property.parcelno: public_property for public_property in public_property_tmp }

    def get_fieldnames(self):
        """
        Returns correct header row column names.
        """

        field_names = [ 'parcel', 'surveyor', 'common_name', 'note', 'status', 'created_at' ] + [ question.question_id for question in self.questions ]
        if self.data_types.get('ownership', False):
            field_names.extend( [ 'owner name', 'owner address', 'owner city', 'owner state', 'owner zip', 'publicly owned' ] )
        if self.data_types.get('address_info', False):
            field_names.extend( [ 'street address' ] )
        if self.calc_score:
            field_names.extend( [ 'score' ] )
        if self.add_streetview_link:
            field_names.extend( [ 'streetview' ] )
        return field_names

    def prettify_answers(self, answer_data):
        """
        Replace answer values with human-readable text.
        """

        for question_id in answer_data.keys():
            pretty_answer = ''
            for answer_value in split_csv(answer_data[question_id]):
                if pretty_answer:
                    pretty_answer = pretty_answer + ', '
                pretty_answer = pretty_answer + self.avail_answers[question_id][answer_value]

            answer_data[question_id] = pretty_answer

    @staticmethod
    def get_curr_answers(question, answers):
        """
        Return survey answers for current question.
        """

        curr_answers = [ answer.answer for answer in answers[question.question_id] ]
        if len(curr_answers) == 1 and ',' in curr_answers[0]:
            return split_csv(curr_answers[0])
        else:
            return curr_answers

    @staticmethod
    def calculate_survey_score(survey):
        """
        Calculate a score for this survey.
        """

        MAX_SCORE = 5

        questions = survey.survey_questions
        answers_tmp = SurveyAnswer.objects.filter(survey_id=survey.id)

        question_answers = { question.question_id: [ answer for answer in answers_tmp if answer.question_id == question.question_id ] for question in questions }

        score = 0

        for question in questions:

            curr_answers = Command.get_curr_answers(question, question_answers)

            answer_weights = [ avail_answer.weight for avail_answer in question.surveyquestionavailanswer_set.all() if avail_answer.value in curr_answers ]

            if len(curr_answers) != len(answer_weights):
                raise Exception('# of answers and # of answer weights should be equal')    # pragma: no cover (should never get here)

            if not answer_weights:
                curr_score = 0
            elif question.scoring_type == 'sum':
                curr_score = min(sum(answer_weights), MAX_SCORE)
            else:
                curr_score = max(answer_weights)

            if curr_score > score:
                score = curr_score

        return score

    @staticmethod
    def get_streetview_link(survey):
        """
        Returns a link to one of the mapillary 'streetview' images that was used to create the survey.
        """

        img_meta = ImageMetadata.objects.filter(parcel__parcel_id=survey.parcel.parcel_id).first()
        if not img_meta:
            return None     # pragma: no cover - should never get here

        # TODO might be smart to make this a method on the survey object... except we may need to optimize this
        # by retrieving all the image_metadata objects when we first retrieve all the surveys?

        return "https://www.mapillary.com/app/?lat={0}&lng={1}&z=17&pKey={2}&focus=photo".format(img_meta.latitude, img_meta.longitude, survey.image_url)

    def get_answerdata(self, survey):
        """
        Returns answer data for a given survey.
        """

        curr_answers = [ answer for answer in self.answers if answer.survey_id == survey.id ]
        if not curr_answers:
            return None     # pragma: no cover - should never get here

        # Get basic information about the survey itself
        answer_data = { 'parcel': survey.parcel.parcel_id, 'surveyor': survey.user.username, 'common_name': survey.common_name, 'note': survey.note, 'status': survey.status, 'created_at': survey.created_at }

        # Get the answers
        answer_data_tmp = { answer.question_id: answer.answer for answer in curr_answers }

        # Pretty print the answers?
        if self.pretty_print:
            self.prettify_answers(answer_data_tmp)

        answer_data.update(answer_data_tmp)

        # Get the ownership data?
        if self.data_types.get('ownership', False):
            parcel = self.parcels.get(survey.parcel.parcel_id, None)
            if parcel:
                if self.data_types.get('ownership', False):
                    owner_name = parcel.ownername1
                    if parcel.ownername2:
                        owner_name = owner_name + ' - ' + parcel.ownername2
                    answer_data['owner name'] = owner_name
                    answer_data['owner address'] = parcel.ownerstreetaddr
                    answer_data['owner city'] = parcel.ownercity
                    answer_data['owner state'] = parcel.ownerstate
                    answer_data['owner zip'] = parcel.ownerzip
                    answer_data['publicly owned'] = 'y' if self.public_property.get(survey.parcel.parcel_id) else 'n'
                if self.data_types.get('address_info', False):
                    answer_data['street address'] = parcel.propstreetcombined

        # Calculate a score for each survey?
        if self.calc_score:
            answer_data['score'] = self.calculate_survey_score(survey)

        # Add a streetview link for each survey?
        if self.add_streetview_link:
            link = self.get_streetview_link(survey)
            if link:
                answer_data['streetview'] = link

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

                    if self.num_exported % 100 == 0:    # pragma: no cover
                        self.stdout.write("{} rows exported ...".format(self.num_exported))
                        self.stdout.flush()

    def handle(self, *args, **options):

        self.init_metadata(options)

        self.get_data()

        self.export_data()

        return "Exported answers for {} surveys to {}".format(self.num_exported, self.out_file)
