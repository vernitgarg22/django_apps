from django.contrib import admin

from .models import Survey, SurveyQuestion, SurveyQuestionAvailAnswer


class SurveyAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['survey_template_id', 'user_id', 'parcel_id', 'common_name', 'note', 'image_url', 'status']}),
        # ('Destination', {'fields': ['destination'], 'classes': ['collapse']}),
    ]
    # inlines = [ChoiceInline]
    list_display = ('survey_template_id', 'user_id', 'parcel_id', 'common_name', 'note', 'image_url', 'status')
    list_filter = ['survey_template_id', 'user_id', 'parcel_id', 'common_name', 'note', 'image_url', 'status']
    list_editable = ['note', 'status']
    search_fields = ['survey_template_id', 'user_id', 'parcel_id', 'note', 'status']
    ordering = ['survey_template_id', 'parcel_id', 'common_name', 'status']

admin.site.register(Survey, SurveyAdmin)


class SurveyQuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['survey_template_id', 'question_id', 'question_number', 'question_text', 'valid_answers', 'required_by', 'required_by_answer', 'answer_trigger', 'answer_trigger_action']}),
        # ('Destination', {'fields': ['destination'], 'classes': ['collapse']}),
    ]
    # inlines = [ChoiceInline]
    list_display = ('survey_template_id', 'question_id', 'question_number', 'question_text', 'valid_answers', 'required_by', 'required_by_answer', 'answer_trigger', 'answer_trigger_action')
    list_filter = ['survey_template_id']
    list_editable = ['question_id', 'question_number', 'question_text', 'valid_answers', 'required_by', 'required_by_answer', 'answer_trigger', 'answer_trigger_action']
    search_fields = ['survey_template_id', 'question_id', 'question_text']
    ordering = ['survey_template_id', 'question_number']

admin.site.register(SurveyQuestion, SurveyQuestionAdmin)

class SurveyQuestionAvailAnswerAdmin(admin.ModelAdmin):
    """
    Defines different answers available for each question.
    """

    app_label = 'photo_survey'

    fieldsets = [
        (None, {'fields': ['value', 'text']}),
        # ('Destination', {'fields': ['destination'], 'classes': ['collapse']}),
    ]
    # inlines = [ChoiceInline]
    list_display = ('survey_question_question_id', 'value', 'text')
    list_filter = []
    list_editable = ['value', 'text']
    search_fields = ['value', 'text']
    ordering = ['value']

admin.site.register(SurveyQuestionAvailAnswer, SurveyQuestionAvailAnswerAdmin)