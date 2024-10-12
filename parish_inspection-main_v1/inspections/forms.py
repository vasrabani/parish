from django import forms
from .models import Question, Parish, Inspection, GeneralComment, InspectionQuestion


class ParishForm(forms.ModelForm):
    class Meta:
        model = Parish
        fields = ['image', 'name', 'description']

    image = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))


class InspectionForm(forms.ModelForm):
    # Adding comment_text to the form manually
    comment_text = forms.CharField(
        required=False,  # Allow this to be empty
        widget=forms.Textarea(attrs={'rows': 3}),
        label="General Comment"
    )

    class Meta:
        model = Inspection
        fields = []  # Keep this empty, as we will add fields dynamically

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add dynamic fields for each default question
        questions = Question.objects.filter(is_default=True)
        for question in questions:
            field_name = f'question_{question.id}'
            self.fields[field_name] = forms.ChoiceField(
                label=question.question_text,
                choices=[('yes', 'Yes'), ('no', 'No'), ('dont_know', "Don't Know")],
                widget=forms.Select(),
                required=False
            )
            self.fields[field_name].question_instance = question  # Attach the question instance for reference

        # Allow passing the existing comment when editing
        if 'instance' in kwargs and kwargs['instance']:
            # Set initial comment_text from the existing GeneralComment (if any)
            inspection_instance = kwargs['instance']
            general_comment = GeneralComment.objects.filter(inspection=inspection_instance).first()
            kwargs['initial'] = kwargs.get('initial', {})
            kwargs['initial']['comment_text'] = general_comment.comment_text if general_comment else ""

            # Set initial responses for existing questions
            for question in questions:
                inspection_question = inspection_instance.questions.filter(question_text=question.question_text).first()
                if inspection_question:
                    self.fields[f'question_{question.id}'].initial = inspection_question.response


class InspectionQuestionForm(forms.ModelForm):
    class Meta:
        model = InspectionQuestion
        fields = ['answer']  # Only allow editing of the answer
