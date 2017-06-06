from django.core.management import call_command
from django.test import TestCase
from django.utils.six import StringIO


class ClosepollTest(TestCase):
    def test_command_output(self):
        out = StringIO()
        call_command('send_message', '5005550006', 'test message', stdout=out)
        self.assertIn("Sent message 'test message' to phone_number 5005550006", out.getvalue())