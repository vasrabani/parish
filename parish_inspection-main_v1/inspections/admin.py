from django.contrib import admin
from .models import Parish, Inspection, Question, GeneralComment, InspectionQuestion


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'is_default')

    def delete_selected(self, request, queryset):
        # This action deletes the selected questions and cascades the deletion to inspections
        queryset.delete()
        self.message_user(request, "Selected questions were deleted successfully.")


class InspectionAdmin(admin.ModelAdmin):
    list_display = ('parish', 'created_at', 'updated_at')


@admin.register(InspectionQuestion)
class InspectionQuestionAdmin(admin.ModelAdmin):
    list_display = ['inspection', 'question', 'answer']


admin.site.register(Parish)
admin.site.register(Inspection, InspectionAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(GeneralComment)
