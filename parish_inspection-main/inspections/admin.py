from django.contrib import admin
from django import forms

from .models import Parish, Inspection, Question, InspectionQuestion


class InspectionInline(admin.TabularInline):
    model = Inspection
    extra = 0
    readonly_fields = ('created_at', 'updated_at')

    def get_queryset(self, request):
        # Order inspections by updated_at for better readability
        return super().get_queryset(request).order_by('-updated_at')


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'is_default')


class ParishAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    inlines = [InspectionInline]

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj:  # When editing/viewing a specific parish
            inspections = obj.inspections.all().order_by('-updated_at')
            inspection_choices = [(insp.id, str(insp)) for insp in inspections]

            form.base_fields['inspection'] = forms.ChoiceField(
                choices=inspection_choices,
                label='Select Inspection',
                required=False
            )
        return form

    def response_change(self, request, obj):
        # Handles the display of inspection questions and responses
        inspection_id = request.POST.get('inspection', None)
        if inspection_id:
            selected_inspection = Inspection.objects.get(id=inspection_id)
            inspection_questions = InspectionQuestion.objects.filter(inspection=selected_inspection)

            self.message_user(request, f"Showing responses for inspection: {selected_inspection}")
            for iq in inspection_questions:
                self.message_user(request, f"{iq.question.question_text}: {iq.answer}")
        return super().response_change(request, obj)


class InspectionAdmin(admin.ModelAdmin):
    list_display = ('parish', 'created_at', 'updated_at')
    list_filter = 'parish'  # Allows filtering by parish and user for better grouping

    def get_queryset(self, request):
        # Ensure inspections are grouped by user and parish, ordered by creation date
        qs = super().get_queryset(request)
        return qs.order_by('parish', '-created_at')


class InspectionQuestionAdmin(admin.ModelAdmin):
    list_display = ['inspection', 'question', 'answer']
    list_filter = ['inspection__parish']  # Adds filters for Parish and User for better grouping

    def get_queryset(self, request):
        # Group by Inspection (which already groups by parish and user), and order by creation date of the inspection
        qs = super().get_queryset(request)
        return qs.select_related('inspection', 'question').order_by('inspection__parish', 'inspection__created_at')


admin.site.register(Parish)
admin.site.register(Inspection)
admin.site.register(InspectionQuestion)
