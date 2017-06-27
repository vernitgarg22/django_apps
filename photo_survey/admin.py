from django.contrib import admin

from .models import SurveyTemplate


class SurveyTemplateAdmin(admin.ModelAdmin):
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

admin.site.register(SurveyTemplate, SurveyTemplateAdmin)
