#!/usr/bin/env python
import os
import sys

import django
from django.conf import settings
from django.test.utils import get_runner


if __name__ == "__main__":
    os.environ['DJANGO_SETTINGS_MODULE'] = 'django_apps.settings'
    os.environ['RUNNING_UNITTESTS'] = 'yes'
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    # test_labels = ["tests"]
    # failures = test_runner.run_tests(["tests"])
    # test_labels = ["tests.test_cod_utils"]
    # test_labels = ["tests.test_assessments"]
    # test_labels = ["tests.test_blight_tickets"]
    # test_labels = ["tests.test_commands"]
    # test_labels = ["tests.test_commands.ExportDataCSVTest.test_output_foreign_key"]
    # test_labels = ["tests.test_data_cache"]
    # test_labels = ["tests.test_data_cache.DataCacheTests.test_data_cache_invalid_source"]
    # test_labels = ["tests.test_photo_survey"]
    # test_labels = ["tests.test_photo_survey.BridgingNeighborhoodsTests"]
    # test_labels = ["tests.test_waste_schedule"]
    # test_labels = ["tests.test_waste_notifier.WasteNotifierTests.test_sign_up_by_fone_virginia_park_st"]
    # test_labels = ["tests.test_commands.ImportPhotoSurveyImagesTest.test_import_existing_parcel_metadata"]
    # test_labels = ["tests.test_waste_notifier"]
    # test_labels = ["tests.test_waste_wizard"]
    # test_labels = ["tests.test_waste_notifier.WasteNotifierTests.test_confirm_invalid_phone_number"]
    test_labels = ["tests.test_blight_tickets", "tests.test_assessments", "tests.test_cod_utils", "tests.test_commands", "tests.test_data_cache", "tests.test_photo_survey", "tests.test_waste_schedule", "tests.test_waste_notifier", "tests.test_waste_wizard", "tests.test_weather_info"]
    failures = test_runner.run_tests(test_labels)
    sys.exit(bool(failures))
