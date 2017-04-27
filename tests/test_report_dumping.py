from django.test import Client
from django.test import TestCase

import report_dumping.views


# class ReportDumpingTests(TestCase):

#     def test_report(self):
#         """
#         Test reporting illegal duming
#         """

#         c = Client()
#         response = c.post('/report_dumping/')

#         self.assertTrue(response.status_code == 200)
#         expected = {}
#         self.assertDictEqual(expected, response.data, "Dumping should have been reported")
