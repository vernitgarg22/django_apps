# python manage.py shell
# from photo_survey import init_avail_answers

from photo_survey.models import SurveyQuestion, SurveyQuestionAvailAnswer

survey_template_id = 'default_combined'

SurveyQuestionAvailAnswer.objects.filter(survey_question__survey_template_id=survey_template_id).delete()

survey_questions = SurveyQuestion.objects.filter(survey_template_id=survey_template_id).order_by('question_number')
# for survey_question in survey_questions:
#     print(survey_question.question_id)

survey_question = survey_questions.filter(question_id='is_structure_on_site')[0]
SurveyQuestionAvailAnswer(survey_question=survey_question, value='y', text='Yes').save()
SurveyQuestionAvailAnswer(survey_question=survey_question, value='n', text='No').save()

survey_question = survey_questions.filter(question_id='is_structure_occupied')[0]
SurveyQuestionAvailAnswer(survey_question=survey_question, value='a', text='Occupied').save()
SurveyQuestionAvailAnswer(survey_question=survey_question, value='b', text='Unoccupied').save()
SurveyQuestionAvailAnswer(survey_question=survey_question, value='c', text='Partially Occupied').save()
SurveyQuestionAvailAnswer(survey_question=survey_question, value='d', text='Possibly Unoccupied').save()

survey_question = survey_questions.filter(question_id='site_use_type')[0]
SurveyQuestionAvailAnswer(survey_question=survey_question, value='a', text='Residential').save()
SurveyQuestionAvailAnswer(survey_question=survey_question, value='b', text='Commercial').save()
SurveyQuestionAvailAnswer(survey_question=survey_question, value='c', text='Mixed-use').save()
SurveyQuestionAvailAnswer(survey_question=survey_question, value='d', text='Industrial').save()
SurveyQuestionAvailAnswer(survey_question=survey_question, value='e', text='Institutional').save()
SurveyQuestionAvailAnswer(survey_question=survey_question, value='f', text='Unknown').save()

survey_question = survey_questions.filter(question_id='num_residential_units')[0]
SurveyQuestionAvailAnswer(survey_question=survey_question, value='a', text='Garage or shed').save()
SurveyQuestionAvailAnswer(survey_question=survey_question, value='b', text='Single Family').save()
SurveyQuestionAvailAnswer(survey_question=survey_question, value='c', text='Multi-Family').save()
SurveyQuestionAvailAnswer(survey_question=survey_question, value='d', text='Apartments').save()

survey_question = survey_questions.filter(question_id='residence_type')[0]
SurveyQuestionAvailAnswer(survey_question=survey_question, value='a', text='Single Family').save()
SurveyQuestionAvailAnswer(survey_question=survey_question, value='b', text='Multi-Family').save()
SurveyQuestionAvailAnswer(survey_question=survey_question, value='c', text='Apartments').save()

survey_question = survey_questions.filter(question_id='commercial_occupants_type')[0]
SurveyQuestionAvailAnswer(survey_question=survey_question, value='a', text='Restaurant / Bar').save()
SurveyQuestionAvailAnswer(survey_question=survey_question, value='b', text='Grocery').save()
SurveyQuestionAvailAnswer(survey_question=survey_question, value='c', text='Retail').save()
SurveyQuestionAvailAnswer(survey_question=survey_question, value='d', text='Service').save()
SurveyQuestionAvailAnswer(survey_question=survey_question, value='e', text='Offices').save()
SurveyQuestionAvailAnswer(survey_question=survey_question, value='f', text='Entertainment').save()
SurveyQuestionAvailAnswer(survey_question=survey_question, value='g', text='Multi-Occupant').save()
SurveyQuestionAvailAnswer(survey_question=survey_question, value='h', text='Other').save()

survey_question = survey_questions.filter(question_id='industrial_occupants_type')[0]
SurveyQuestionAvailAnswer(survey_question=survey_question, value='a', text='Industrial').save()
SurveyQuestionAvailAnswer(survey_question=survey_question, value='b', text='Warehouses').save()
SurveyQuestionAvailAnswer(survey_question=survey_question, value='c', text='Multi-Occupant').save()
SurveyQuestionAvailAnswer(survey_question=survey_question, value='d', text='Other').save()

survey_question = survey_questions.filter(question_id='institutional_occupants_type')[0]
SurveyQuestionAvailAnswer(survey_question=survey_question, value='a', text='Schools').save()
SurveyQuestionAvailAnswer(survey_question=survey_question, value='b', text='Religious').save()
SurveyQuestionAvailAnswer(survey_question=survey_question, value='c', text='Public Safety').save()
SurveyQuestionAvailAnswer(survey_question=survey_question, value='d', text='Health').save()
SurveyQuestionAvailAnswer(survey_question=survey_question, value='e', text='Recreation').save()
SurveyQuestionAvailAnswer(survey_question=survey_question, value='f', text='Government').save()
SurveyQuestionAvailAnswer(survey_question=survey_question, value='g', text='Non-Profit/Charity').save()
SurveyQuestionAvailAnswer(survey_question=survey_question, value='h', text='Other').save()

survey_question = survey_questions.filter(question_id='structure_condition')[0]
SurveyQuestionAvailAnswer(survey_question=survey_question, value='a', text='Good').save()
SurveyQuestionAvailAnswer(survey_question=survey_question, value='b', text='Fair').save()
SurveyQuestionAvailAnswer(survey_question=survey_question, value='c', text='Poor').save()
SurveyQuestionAvailAnswer(survey_question=survey_question, value='d', text='Suggest Demolition').save()

survey_question = survey_questions.filter(question_id='is_structure_fire_damaged')[0]
SurveyQuestionAvailAnswer(survey_question=survey_question, value='y', text='Yes').save()
SurveyQuestionAvailAnswer(survey_question=survey_question, value='n', text='No').save()

survey_question = survey_questions.filter(question_id='fire_damage_level')[0]
SurveyQuestionAvailAnswer(survey_question=survey_question, value='a', text='Minor').save()
SurveyQuestionAvailAnswer(survey_question=survey_question, value='b', text='Major').save()
SurveyQuestionAvailAnswer(survey_question=survey_question, value='c', text='Collapsed').save()

survey_question = survey_questions.filter(question_id='is_structure_secure')[0]
SurveyQuestionAvailAnswer(survey_question=survey_question, value='y', text='Secured').save()
SurveyQuestionAvailAnswer(survey_question=survey_question, value='n', text='Open to Trespass').save()

survey_question = survey_questions.filter(question_id='site_use')[0]
SurveyQuestionAvailAnswer(survey_question=survey_question, value='a', text='Vacant Lot').save()
SurveyQuestionAvailAnswer(survey_question=survey_question, value='b', text='Parking Lot').save()
SurveyQuestionAvailAnswer(survey_question=survey_question, value='c', text='Park').save()
SurveyQuestionAvailAnswer(survey_question=survey_question, value='d', text='Garden').save()
SurveyQuestionAvailAnswer(survey_question=survey_question, value='e', text='Other').save()
SurveyQuestionAvailAnswer(survey_question=survey_question, value='f', text='Attached Lot').save()

survey_question = survey_questions.filter(question_id='is_lot_maintained')[0]
SurveyQuestionAvailAnswer(survey_question=survey_question, value='y', text='Yes').save()
SurveyQuestionAvailAnswer(survey_question=survey_question, value='n', text='No').save()

survey_question = survey_questions.filter(question_id='is_dumping_on_site')[0]
SurveyQuestionAvailAnswer(survey_question=survey_question, value='y', text='Yes').save()
SurveyQuestionAvailAnswer(survey_question=survey_question, value='n', text='No').save()

survey_question = survey_questions.filter(question_id='blighted_lot_elements')[0]
SurveyQuestionAvailAnswer(survey_question=survey_question, value='a', text='Active billboard').save()
SurveyQuestionAvailAnswer(survey_question=survey_question, value='b', text='Inactive billboard').save()
SurveyQuestionAvailAnswer(survey_question=survey_question, value='c', text='Lot is accessible ').save()
SurveyQuestionAvailAnswer(survey_question=survey_question, value='d', text='Blighted signs').save()
SurveyQuestionAvailAnswer(survey_question=survey_question, value='e', text='Graffiti').save()
SurveyQuestionAvailAnswer(survey_question=survey_question, value='f', text='Overgrown').save()
SurveyQuestionAvailAnswer(survey_question=survey_question, value='g', text='Cement piles').save()
SurveyQuestionAvailAnswer(survey_question=survey_question, value='h', text='Large dirt piles').save()
SurveyQuestionAvailAnswer(survey_question=survey_question, value='i', text='Tires illegally dumped').save()
SurveyQuestionAvailAnswer(survey_question=survey_question, value='j', text='Broken/abandoned fences').save()
SurveyQuestionAvailAnswer(survey_question=survey_question, value='k', text='Abandoned cars (2 or less)').save()
SurveyQuestionAvailAnswer(survey_question=survey_question, value='l', text='Abandoned cars (3 or more)').save()
SurveyQuestionAvailAnswer(survey_question=survey_question, value='m', text='Other').save()

survey_question = survey_questions.filter(question_id='blighted_structure_elements')[0]
SurveyQuestionAvailAnswer(survey_question=survey_question, value='a', text='Needs Demo').save()
SurveyQuestionAvailAnswer(survey_question=survey_question, value='b', text='Needs Board Up').save()
SurveyQuestionAvailAnswer(survey_question=survey_question, value='c', text='Structure is accessible').save()
SurveyQuestionAvailAnswer(survey_question=survey_question, value='d', text='Active billboard').save()
SurveyQuestionAvailAnswer(survey_question=survey_question, value='e', text='Inactive billboard').save()
SurveyQuestionAvailAnswer(survey_question=survey_question, value='f', text='Blighted signs/awnings').save()
SurveyQuestionAvailAnswer(survey_question=survey_question, value='g', text='Graffiti, etc').save()
SurveyQuestionAvailAnswer(survey_question=survey_question, value='h', text='Overgrown').save()
SurveyQuestionAvailAnswer(survey_question=survey_question, value='i', text='Cement piles').save()
SurveyQuestionAvailAnswer(survey_question=survey_question, value='j', text='Large Dirt piles').save()
SurveyQuestionAvailAnswer(survey_question=survey_question, value='k', text='Tires illegaly dumped').save()
SurveyQuestionAvailAnswer(survey_question=survey_question, value='l', text='Broken/abandoned fences').save()
SurveyQuestionAvailAnswer(survey_question=survey_question, value='m', text='Abandoned cars (2 or less)').save()
SurveyQuestionAvailAnswer(survey_question=survey_question, value='n', text='Abandoned cars (3 or more)').save()
SurveyQuestionAvailAnswer(survey_question=survey_question, value='o', text='Other').save()

survey_question = survey_questions.filter(question_id='sidewalk_condition')[0]
SurveyQuestionAvailAnswer(survey_question=survey_question, value='a', text='Cracked').save()
SurveyQuestionAvailAnswer(survey_question=survey_question, value='b', text='Uneven over 1.5"').save()
SurveyQuestionAvailAnswer(survey_question=survey_question, value='c', text='Missing').save()
SurveyQuestionAvailAnswer(survey_question=survey_question, value='d', text='Appears in good condition').save()

print(SurveyQuestionAvailAnswer.objects.count())
