from django.shortcuts import render
from django.template.response import TemplateResponse
from django.views import View
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from django.contrib.messages.views import SuccessMessageMixin
from .forms import PatientsForm, DoctorsForm, MedicamentForm
from .models import Patients, Doctors, Medicament
from django.contrib import messages

# Create your views here.


class FirstSiteView(View):
    """
    View first site
    """
    def get(self, request):
        return TemplateResponse(request, 'base.html')

class AddPatientsView(CreateView):
    """Added to the patient database"""
    model = Patients
    success_url = reverse_lazy('add-patients')
    form_class = PatientsForm
    success_message = 'Dodano pacjenta!'

    def get_success_message(self, cleaned_data):
        return f"Dodano pacjenta {cleaned_data}"


class AddDoctorsView(SuccessMessageMixin, CreateView):
    """Added to the patient database"""
    model = Doctors
    success_url = reverse_lazy('base')
    form_class = DoctorsForm
    success_message = 'Dodano lekarza!'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response

    # def get_success_message(self, cleaned_data):
    #     return f"Dodano lekarza {cleaned_data}"


class AddMedicamentView(SuccessMessageMixin, CreateView):
    """Added to the medicament database"""
    model = Medicament
    success_url = reverse_lazy('base')
    form_class = MedicamentForm
    success_message = 'Dodano lek!'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response
