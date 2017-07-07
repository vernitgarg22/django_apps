from django.contrib import admin

from .models import Survey, SurveyQuestion


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
    ordering = ['survey_template_id']

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
