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
    # failures = test_runner.run_tests(["tests"])
    # failures = test_runner.run_tests(["tests.cod_utils_tests"])
    # failures = test_runner.run_tests(["tests.test_waste_schedule"])
    # failures = test_runner.run_tests(["tests.test_waste_schedule.WasteScheduleTests.test_get_schedule_details_citywide_reschedule"])
    # failures = test_runner.run_tests(["tests.test_waste_notifier"])
    # failures = test_runner.run_tests(["tests.test_waste_wizard"])
    # failures = test_runner.run_tests(["tests.test_waste_notifier.WasteNotifierTests.test_confirm_invalid_phone_number"])
    failures = test_runner.run_tests(["tests.cod_utils_tests", "tests.test_waste_schedule", "tests.test_waste_notifier", "tests.test_waste_wizard", "tests.test_weather_info"])
    sys.exit(bool(failures))
