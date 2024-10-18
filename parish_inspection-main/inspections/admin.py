from django.contrib import admin
from .models import Parish, Inspection, Question, InspectionQuestion


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'is_default')


admin.site.register(Parish)
admin.site.register(Inspection)
admin.site.register(InspectionQuestion)
