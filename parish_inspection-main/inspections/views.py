from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Parish, Inspection, Question, GeneralComment, InspectionQuestion
from .forms import ParishForm, InspectionForm
from django.utils import timezone
from django.core.paginator import Paginator


class HomeView(ListView):
    model = Parish
    template_name = 'inspections/home.html'
    context_object_name = 'parishes'
    paginate_by = 10

    def get_queryset(self):
        return Parish.objects.all().order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_paginated'] = self.paginate_by < self.get_queryset().count()
        context['count_parishes'] = self.get_queryset().count()
        return context


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'inspections/register.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)  # Log in the user after successful registration
        return redirect(self.success_url)


class ParishCreateView(LoginRequiredMixin, CreateView):
    model = Parish
    form_class = ParishForm
    template_name = 'inspections/create_parish.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        parish = form.save(commit=False)
        parish.save()
        return redirect(self.success_url)


class ParishDetailView(DetailView):
    model = Parish
    template_name = 'inspections/parish_detail.html'
    context_object_name = 'parish'
    pk_url_kwarg = 'parish_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        parish = self.get_object()
        # Fetch all inspections ordered by the most recent update
        context['inspections'] = self.object.inspections.all().order_by('-updated_at')
        context['num_inspections'] = self.object.inspections.count()
        context['is_creator'] = self.request.user.is_authenticated and parish.created_by == self.request.user
        return context




class InspectionCreateView(LoginRequiredMixin, CreateView):
    model = Inspection
    form_class = InspectionForm
    template_name = 'inspections/create_inspection.html'

    def form_valid(self, form):
        parish = Parish.objects.get(id=self.kwargs['parish_id'])
        inspection = form.save(commit=False)
        inspection.parish = parish
        inspection.save()

        # Save responses to questions
        for field_name, field_value in form.cleaned_data.items():
            if field_name.startswith('question_'):
                question_id = int(field_name.split('_')[1])
                question_instance = Question.objects.get(id=question_id)

                InspectionQuestion.objects.create(
                    inspection=inspection,
                    question=question_instance,
                    answer=field_value
                )

        comment_text = form.cleaned_data.get('comment_text', '')
        if comment_text:
            GeneralComment.objects.create(inspection=inspection, comment_text=comment_text)

        return redirect('parish_detail', parish_id=parish.id)


class InspectionDetailView(DetailView):
    model = Inspection
    template_name = 'inspections/inspection_detail.html'
    pk_url_kwarg = 'inspection_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        inspection = self.get_object()

        # Fetch all questions related to this inspection
        inspection_questions = inspection.inspection_questions.all()  # Make sure to have the related name correctly set

    # Set up pagination
        paginator = Paginator(inspection_questions, 5)  # Show 5 questions per page
        page_number = self.request.GET.get('page')  # Get the page number from the URL
        questions_page = paginator.get_page(page_number)  # Get the relevant page of questions

    # Add paginated questions and comments to the context
        context['inspection_questions'] = questions_page  # Use the paginated questions
        context['comment'] = GeneralComment.objects.filter(inspection=inspection).first()

   # def get_context_data(self, **kwargs):
   #     context = super().get_context_data(**kwargs)
        # Fetch all questions and their related answers for this inspection
   #     inspection_questions = self.object.inspection_questions.all()
   #     context['inspection_questions'] = inspection_questions
   #     context['comment'] = GeneralComment.objects.filter(inspection=self.object).first()
        return context


class InspectionEditView(LoginRequiredMixin, UpdateView):
    model = Inspection
    form_class = InspectionForm
    template_name = 'inspections/edit_inspection.html'
    pk_url_kwarg = 'inspection_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        inspection = self.get_object()

        # Fetch all questions related to this inspection with an explicit order
        inspection_questions = inspection.inspection_questions.all().order_by('id')  # Ensure an explicit ordering

        # Set up pagination for the inspection questions
        paginator = Paginator(inspection_questions, 5)  # Show 5 questions per page
        page_number = self.request.GET.get('page')  # Get the current page number from the URL
        questions_page = paginator.get_page(page_number)  # Get the relevant page

        context['inspection_questions'] = questions_page  # Paginated questions

    def form_valid(self, form):
        inspection = form.save(commit=False)
        inspection.updated_at = timezone.now()  # Update the timestamp
        inspection.save()

        # Update responses to questions
        for field_name, field_value in form.cleaned_data.items():
            if field_name.startswith('question_'):
                question_id = int(field_name.split('_')[1])
                question_instance = Question.objects.get(id=question_id)

                # Find and update the response for the inspection question
                inspection_question = InspectionQuestion.objects.get(inspection=inspection, question=question_instance)
                inspection_question.answer = field_value
                inspection_question.save()

        comment_text = form.cleaned_data.get('comment_text', '').strip()
        general_comment = GeneralComment.objects.filter(inspection=inspection).first()

        if comment_text:
            if general_comment:
                general_comment.comment_text = comment_text
                general_comment.save()
            else:
                GeneralComment.objects.create(inspection=inspection, comment_text=comment_text)
        elif general_comment:
            general_comment.delete()

        return redirect('parish_detail', parish_id=inspection.parish.id)


class InspectionDeleteView(DeleteView):
    model = Inspection
    template_name = 'inspections/delete_inspection.html'
    pk_url_kwarg = 'inspection_id'

    def get_object(self, queryset=None):
        parish = get_object_or_404(Parish, id=self.kwargs['parish_id'])
        inspection = get_object_or_404(Inspection, id=self.kwargs['inspection_id'], parish=parish)

        # Check if the user is the creator of the parish
        if parish.created_by != self.request.user:
            raise HttpResponseForbidden("You are not allowed to delete inspections from this parish.")

        return inspection

    def get_success_url(self):
        parish_id = self.kwargs['parish_id']
        return reverse_lazy('parish_detail', kwargs={'parish_id': parish_id})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect(self.get_success_url())


class ParishDeleteView(DeleteView):
    model = Parish
    template_name = 'inspections/delete_parish.html'
    pk_url_kwarg = 'parish_id'

    def get_object(self, queryset=None):
        parish = get_object_or_404(Parish, id=self.kwargs['parish_id'])
        if parish.created_by != self.request.user:
            raise HttpResponseForbidden("You are not allowed to delete this parish.")
        return parish

    def get_success_url(self):
        return reverse_lazy('home')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect(self.get_success_url())
