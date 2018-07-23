#!/usr/bin/env python

import os
import sys
import json
from datetime import date
from datetime import datetime
import requests
from requests.auth import HTTPBasicAuth

import django
from django.conf import settings


def test(condition, msg):

	if not condition:

		raise(Exception("Test failed: " + msg))

if __name__ == '__main__':

	os.environ['DJANGO_SETTINGS_MODULE'] = 'django_apps.settings'
	django.setup()

	from photo_survey.models import SurveyType, Survey

	temp = SurveyType.objects.filter(survey_template_id = 'bridging_neighborhoods')
	test(len(temp) == 1, 'found bridging neighborhoods survey type')

	bn_survey_type = temp[0]

	surveys = bn_survey_type.survey_set.filter(status = '')
	test(len(surveys) == 69, 'found correct bridging neighborhoods surveys')

	for survey in surveys:

		survey.note = 'marked deleted - 2018/07/18'
		survey.status = 'deleted'
		survey.save()
