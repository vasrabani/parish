from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Inspection, Question, InspectionQuestion


@receiver(post_save, sender=Inspection)
def create_inspection_questions(sender, instance, created, **kwargs):
    """Signal to link existing questions to the new inspection."""
    if created:
        # Fetch the default questions
        default_questions = Question.objects.filter(is_default=True)

        # Link each default question with the new inspection
        for question in default_questions:
            InspectionQuestion.objects.create(inspection=instance, question=question)

