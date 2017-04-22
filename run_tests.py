#!/usr/bin/env python
import os
import sys

import django
from django.conf import settings
from django.test.utils import get_runner

if __name__ == "__main__":
    os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.test_settings'
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests(["tests"])
    # failures = test_runner.run_tests(["tests.test_report_dumping.ReportDumpingTests.test_report"])
    # failures = test_runner.run_tests(["tests.test_waste_notifier.WasteNotifierTests.test_send_today_query_param"])
    sys.exit(bool(failures))
