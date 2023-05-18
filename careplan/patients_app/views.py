from django.shortcuts import render
from django.template.response import TemplateResponse
from django.views import View
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from django.contrib.messages.views import SuccessMessageMixin
from .forms import PatientsForm, DoctorsForm, MedicamentForm
from .models import Patients, Doctors, Medicament, MedicalComponent
from django.contrib import messages


# Create your views here.


class FirstSiteView(View):
    """
    View first site
    """

    def get(self, request):
        return TemplateResponse(request, 'first_page.html')


class AddPatientsView(CreateView):
    """Added to the patient database"""
    model = Patients
    success_url = reverse_lazy('add-patients')
    form_class = PatientsForm
    success_message = 'Dodano pacjenta!'

    def get_success_message(self, cleaned_data):
        return f"Dodano pacjenta {cleaned_data}"

class PatientsListView(ListView):
    """List of all patients"""
    model = Patients
    template_name = 'patients_list.html'  # Name template HTML
    context_object_name = 'patients'  # Nazwa obiektu w kontekście szablonu

    def get_queryset(self):
        query = self.request.GET.get('search')
        if query:
            # Przeszukiwanie pacjentów po nazwisku
            return Patients.objects.filter(pesel__icontains=query)
        else:
            return Patients.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        return context

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


class DoctorsListView(ListView):
    """List of all doctors"""
    model = Doctors
    template_name = 'doctors_list.html'  # Name template HTML
    context_object_name = 'doctors'  # Nazwa obiektu w kontekście szablonu

    def get_queryset(self):
        query = self.request.GET.get('search')
        if query:
            # Przeszukiwanie doctora po nazwisku
            return Doctors.objects.filter(last_name__icontains=query)
        else:
            return Doctors.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        return context


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


class AddMedicalComponentView(SuccessMessageMixin, CreateView):
    """Added to the medicalcomponent database"""
    model = MedicalComponent
    success_url = reverse_lazy('base')
    form_class = MedicamentForm
    success_message = 'Dodano wyrób medyczny!'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response
