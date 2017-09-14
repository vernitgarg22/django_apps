from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import User, Group

from .models import Survey, Surveyor, SurveyorGroup, SurveyType, SurveyQuestion, SurveyQuestionAvailAnswer


class SurveyTypeAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['survey_template_id']}),
        # ('Destination', {'fields': ['destination'], 'classes': ['collapse']}),
    ]
    # inlines = [ChoiceInline]
    list_display = ['survey_template_id']
    list_display_links = ['survey_template_id']
    list_filter = []
    # list_editable = ['survey_template_id']
    search_fields = []

admin.site.register(SurveyType, SurveyTypeAdmin)


class SurveyAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['survey_template_id', 'user_id', 'parcel_id', 'common_name', 'note', 'image_url', 'status']}),
        # ('Destination', {'fields': ['destination'], 'classes': ['collapse']}),
    ]
    # inlines = [ChoiceInline]
    list_display = ('survey_template_id', 'user_id', 'parcel_id', 'common_name', 'note', 'image_url', 'status')
    list_filter = ['survey_type__survey_template_id', 'user_id', 'parcel_id', 'common_name', 'note', 'image_url', 'status']
    list_editable = ['note', 'status']
    search_fields = ['survey_template_id', 'user_id', 'parcel_id', 'note', 'status']

admin.site.register(Survey, SurveyAdmin)


class SurveyQuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['survey_type', 'question_id', 'question_number', 'question_text', 'valid_answers', 'required_by', 'required_by_answer', 'answer_trigger', 'answer_trigger_action', 'scoring_type']}),
        # ('Destination', {'fields': ['destination'], 'classes': ['collapse']}),
    ]
    # inlines = [ChoiceInline]
    list_display = ('survey_type', 'question_id', 'question_number', 'question_text', 'valid_answers', 'required_by', 'required_by_answer', 'answer_trigger', 'answer_trigger_action', 'scoring_type')
    list_filter = ['survey_type__survey_template_id']
    list_editable = ['question_id', 'question_number', 'question_text', 'valid_answers', 'required_by', 'required_by_answer', 'answer_trigger', 'answer_trigger_action', 'scoring_type']
    search_fields = ['survey_type', 'question_id', 'question_text']
    ordering = ['survey_type_id', 'question_number']

admin.site.register(SurveyQuestion, SurveyQuestionAdmin)

class SurveyQuestionAvailAnswerAdmin(admin.ModelAdmin):
    """
    Defines different answers available for each question.
    """

    app_label = 'photo_survey'

    fieldsets = [
        (None, {'fields': ['value', 'text', 'weight']}),
        # ('Destination', {'fields': ['destination'], 'classes': ['collapse']}),
    ]
    # inlines = [ChoiceInline]
    list_display = ('survey_question_question_id', 'value', 'text', 'weight')
    list_filter = []
    list_editable = ['value', 'text', 'weight']
    search_fields = ['value', 'text']
    ordering = ['id', 'value']

admin.site.register(SurveyQuestionAvailAnswer, SurveyQuestionAvailAnswerAdmin)

# Define a new User admin
class SurveyorAdmin(UserAdmin):
    """
    Admin class to administer surveyors.
    """

    app_label = 'photo_survey'

    list_display = ('username', 'email', 'first_name', 'last_name')
    list_filter = ()

    def get_queryset(self, request):    # pragma: no cover  (only used in admin page)
        """
        Filter the objects displayed in the change_list to not show bridging_neighborhoods users.
        """

        # surveyor_group = SurveyorGroup.objects.filter(name="surveyors")[0]
        # surveyors = Surveyor.objects.filter(username__contains='@')
        # for surveyor in surveyors:
        #     surveyor_group.user_set.db_manager('photo_survey').add(surveyor)


        qs = super(SurveyorAdmin, self).get_queryset(request)
        return qs.filter(groups__name = "surveyors")

admin.site.register(Surveyor, SurveyorAdmin)

# Define a new Group admin
class SurveyorGroupAdmin(GroupAdmin):
    """
    Admin class to administer groups of surveyors.
    """

    app_label = 'photo_survey'

    list_display = ['name']
    list_filter = ()

admin.site.register(SurveyorGroup, SurveyorGroupAdmin)
