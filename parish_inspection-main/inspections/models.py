from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Parish(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(default="")
    location = models.CharField(max_length=255, default="")
    contact = models.CharField(max_length=100, default="")
    phone_number = models.CharField(max_length=20, default="")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to='profile_pics/', default='default.jpg')

    def __str__(self):
        return self.name


class Inspection(models.Model):
    CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
        ('other', "Other")
    ]
    parish = models.ForeignKey(Parish, on_delete=models.CASCADE, related_name="inspections")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Inspection for {self.parish.name} on {self.created_at}"


class Question(models.Model):
    question_text = models.TextField()
    is_default = models.BooleanField(default=False)
    inspection = models.ForeignKey(Inspection, on_delete=models.CASCADE, related_name='questions', null=True,
                                   blank=True)
    response = models.CharField(
        max_length=20,
        choices=[('yes', 'Yes'), ('no', 'No'), ('other', "Other")],
        blank=True
    )

    def __str__(self):
        return self.question_text


class InspectionQuestion(models.Model):
    inspection = models.ForeignKey(Inspection, on_delete=models.CASCADE,
                                   related_name='inspection_questions')
    question = models.ForeignKey(Question, on_delete=models.CASCADE,
                                 related_name='inspection_questions')
    answer = models.CharField(max_length=20, choices=[('yes', 'Yes'), ('no', 'No'), ('other', "Other")], blank=True,
                              null=True)

    def __str__(self):
        return f"{self.inspection.parish.name} - {self.question.question_text}: {self.answer}"


class GeneralComment(models.Model):
    inspection = models.OneToOneField(Inspection, on_delete=models.CASCADE)
    comment_text = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Comment for {self.inspection.parish.name}"
