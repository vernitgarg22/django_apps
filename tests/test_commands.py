from django.contrib.auth.models import User
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.test import TestCase
from django.utils.six import StringIO

from tests.test_photo_survey import PhotoSurveyTests


class SendMessageTest(TestCase):
    def test_command_output(self):
        out = StringIO()
        call_command('send_message', '5005550006', 'test message', stdout=out)
        self.assertIn("Sent message 'test message' to phone_number 5005550006", out.getvalue())


class AddUserTest(TestCase):

    def setUp(self):
        User.objects.using('photo_survey').all().delete()

    def test_command(self):

        out = StringIO()
        call_command('add_user', 'bob', 'smith', 'bob.smith@test.com', 'password', stdout=out)
        self.assertEqual(User.objects.using('photo_survey').first().email, 'bob.smith@test.com', 'add_user adds a photo_survey user')

    def test_uniqueness_enforcement(self):
        out = StringIO()
        call_command('add_user', 'bob', 'smith', 'bob.smith@test.com', 'password', stdout=out)

        with self.assertRaises(CommandError, msg="add_user should not let duplicate user be added") as error:
            call_command('add_user', 'bob', 'smith', 'bob.smith@test.com', 'password', stdout=out)


class ExportSurveyAnswersTest(TestCase):

    def test_output(self):

        out = StringIO()

        # Run a different test just to get a survey submitted
        PhotoSurveyTests().test_post_survey_combined()

        call_command('export_survey_answers', 'default_combined', stdout=out)