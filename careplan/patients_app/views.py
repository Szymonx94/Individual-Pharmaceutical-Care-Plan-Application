from django.shortcuts import render
from django.template.response import TemplateResponse
from django.views import View
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from .forms import PatientsForm
from .models import Patients

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
