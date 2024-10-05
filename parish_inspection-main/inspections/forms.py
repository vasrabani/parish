from django import forms
from .models import Question, Parish, Inspection, GeneralComment, InspectionQuestion


class ParishForm(forms.ModelForm):
    class Meta:
        model = Parish
        fields = ['image', 'name', 'description']

    image = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))


class InspectionForm(forms.ModelForm):
    comment_text = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 3}),
        label="General Comment"
    )

    class Meta:
        model = Inspection
        fields = []  # Keep empty, as we will add fields dynamically

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        questions = Question.objects.filter(is_default=True)
        for question in questions:
            field_name = f'question_{question.id}'
            self.fields[field_name] = forms.ChoiceField(
                label=question.question_text,
                choices=[('yes', 'Yes'), ('no', 'No'), ('other', "Other")],
                widget=forms.Select(),
                required=False
            )

        if 'instance' in kwargs and kwargs['instance']:
            inspection_instance = kwargs['instance']
            general_comment = GeneralComment.objects.filter(inspection=inspection_instance).first()
            kwargs['initial']['comment_text'] = general_comment.comment_text if general_comment else ""
            for inspection_question in inspection_instance.inspection_questions.all():
                field_name = f'question_{inspection_question.question.id}'
                self.fields[field_name].initial = inspection_question.answer


class InspectionQuestionForm(forms.ModelForm):
    class Meta:
        model = InspectionQuestion
        fields = ['answer']  # Only allow editing of the answer
