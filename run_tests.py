#!/usr/bin/env python
import os
import pkgutil
import sys

import django
from django.conf import settings
from django.test.utils import get_runner

import tests


if __name__ == "__main__":

    os.environ['DJANGO_HOME'] = os.getcwd()
    os.environ['DJANGO_SETTINGS_MODULE'] = 'django_apps.settings'
    os.environ['RUNNING_UNITTESTS'] = 'yes'
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    test_labels = []

    # test_labels = ["tests"]
    # failures = test_runner.run_tests(["tests"])
    # test_labels = ["tests.test_cod_utils"]
    # test_labels = ["tests.test_assessments"]
    # test_labels = ["tests.test_assessments.AssessmentsTests.test_get_images"]
    # test_labels = ["tests.test_blight_tickets"]
    # test_labels = ["tests.test_commands"]
    # test_labels = ["tests.test_commands.ExportDataCSVTest.test_output_foreign_key"]
    # test_labels = ["tests.test_data_cache"]
    # test_labels = ["tests.test_data_cache.DataCitySummaryTests"]
    # test_labels = ["tests.test_data_cache.DataCacheTests.test_data_cache_invalid_source"]
    # test_labels = ["tests.test_messenger"]
    # test_labels = ["tests.test_messenger.MessengerTests.test_confirm_subscription"]
    # test_labels = ["tests.test_messenger.MessengerSubscriberValidationTests.test_validate_timestamps"]
    # test_labels = ["tests.test_photo_survey"]
    # test_labels = ["tests.test_property_data"]
    # test_labels = ["tests.test_photo_survey.BridgingNeighborhoodsTests"]
    # test_labels = ["tests.test_waste_schedule"]
    # test_labels = ["tests.test_waste_notifier.WasteNotifierTests.test_sign_up_by_fone_virginia_park_st"]
    # test_labels = ["tests.test_commands.ImportPhotoSurveyImagesTest.test_import_existing_parcel_metadata"]
    # test_labels = ["tests.test_waste_notifier"]
    # test_labels = ["tests.test_waste_wizard"]
    # test_labels = ["tests.test_waste_notifier.WasteNotifierTests.test_confirm_invalid_phone_number"]
    # test_labels = ["tests.test_website_data"]

    if not test_labels:

        all_tests = [ mod.name for mod in pkgutil.walk_packages(path=tests.__path__, prefix=tests.__name__ + '.') if mod.name.startswith('tests.test_') ]
        test_labels = sorted(all_tests)

    print("\n\nTesting the following packages: {}\n".format(test_labels))

    failures = test_runner.run_tests(test_labels)
    sys.exit(bool(failures))
