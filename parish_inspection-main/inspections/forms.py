from django import forms
from .models import Question, Parish, Inspection, GeneralComment, InspectionQuestion


class ParishForm(forms.ModelForm):
    class Meta:
        model = Parish
        fields = ['image', 'name', 'description', 'location', 'contact', 'phone_number']

    image = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    location = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))  # New field
    contact = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))  # New field
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))


class InspectionForm(forms.ModelForm):
    class Meta:
        model = Inspection
        fields = []  # Keep empty, as we will add fields dynamically

    comment_text = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 3}),
        label="General Comment"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        questions = Question.objects.filter(is_default=True)
        # Dynamically add question fields
        for question in questions:
            field_name = f'question_{question.id}'
            self.fields[field_name] = forms.ChoiceField(
                label=question.question_text,
                choices=[('yes', 'Yes'), ('no', 'No'), ('other', 'Other')],
                widget=forms.RadioSelect(),  # Changed to RadioSelect for better rendering
                required=False
            )

        # Set the general comment field's initial value
        if 'instance' in kwargs and kwargs['instance']:
            inspection_instance = kwargs['instance']
            general_comment = GeneralComment.objects.filter(inspection=inspection_instance).first()
            self.fields['comment_text'].initial = general_comment.comment_text if general_comment else ""

            # Set initial values for question responses
            for inspection_question in inspection_instance.inspection_questions.all():
                field_name = f'question_{inspection_question.question.id}'
                self.fields[field_name].initial = inspection_question.answer

        # Move 'comment_text' field to the end
        self.order_fields(field_order=[field for field in self.fields if field != 'comment_text'] + ['comment_text'])


class InspectionQuestionForm(forms.ModelForm):
    class Meta:
        model = InspectionQuestion
        fields = ['answer']  # Only allow editing of the answer
