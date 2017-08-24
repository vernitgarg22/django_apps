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
    # test_labels = ["tests"]
    # failures = test_runner.run_tests(["tests"])
    # test_labels = ["tests.test_cod_utils"]
    # test_labels = ["tests.test_assessments"]
    # test_labels = ["tests.test_blight_tickets"]
    # test_labels = ["tests.test_commands"]
    # test_labels = ["tests.test_photo_survey"]
    # test_labels = ["tests.test_photo_survey.BridgingNeighborhoodsTests"]
    # test_labels = ["tests.test_waste_schedule"]
    # test_labels = ["tests.test_waste_schedule.WasteScheduleTests.test_get_schedule_details_citywide_reschedule"]
    # test_labels = ["tests.test_waste_notifier"]
    # test_labels = ["tests.test_waste_wizard"]
    # test_labels = ["tests.test_waste_notifier.WasteNotifierTests.test_confirm_invalid_phone_number"]
    test_labels = ["tests.test_blight_tickets", "tests.test_assessments", "tests.test_cod_utils", "tests.test_commands", "tests.test_photo_survey", "tests.test_waste_schedule", "tests.test_waste_notifier", "tests.test_waste_wizard", "tests.test_weather_info"]
    failures = test_runner.run_tests(test_labels)
    sys.exit(bool(failures))
