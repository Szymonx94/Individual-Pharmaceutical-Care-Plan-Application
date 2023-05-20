from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from django.views import View
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.contrib.messages.views import SuccessMessageMixin
from .forms import PatientsForm, DoctorsForm, MedicamentForm, MedicalComponentForm, RegistrationForm
from .models import Patients, Doctors, Medicament, MedicalComponent
from django.contrib import messages


# Create your views here.


class FirstSiteView(View):
    """
    View first site
    """

    @staticmethod
    def get(request):
        return TemplateResponse(request, 'first_page.html')


class AddPatientsView(SuccessMessageMixin, CreateView):
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
    template_name = 'patients_list.html'
    ordering = 'id'
    context_object_name = 'patients'


    def get_queryset(self):
        query = self.request.GET.get('search')
        if query:
            # Przeszukiwanie pacjentów po nazwisku
            return Patients.objects.filter(pesel__icontains=query).order_by('id')
        else:
            return Patients.objects.all().order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        return context


class PatientsUpdateView(UpdateView):
    """Class to edit the patient"""
    model = Patients
    form_class = PatientsForm
    template_name = 'patients_update.html'
    success_url = '/patients_list/'


class PatientsDeleteView(DeleteView):
    """ Delete patients"""
    model = Patients
    template_name = 'patients_delete.html'
    success_url = reverse_lazy('patients-list')




class AddDoctorsView(SuccessMessageMixin, CreateView):
    """Added to the patient database"""
    model = Doctors
    success_url = reverse_lazy('add-doctors')
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
    success_url = reverse_lazy('first-page')
    form_class = MedicamentForm
    success_message = 'Dodano lek!'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response


class MedicamentListView(ListView):
    """List of all medicament"""
    model = Medicament
    template_name = 'medicament_list.html'  # Name template HTML
    context_object_name = 'medicament'  # Nazwa obiektu w kontekście szablonu

    def get_queryset(self):
        query = self.request.GET.get('search')
        if query:
            # Przeszukiwanie doctora po nazwisku
            return Medicament.objects.filter(name__icontains=query)
        else:
            return Medicament.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        return context


class AddMedicalComponentView(SuccessMessageMixin, CreateView):
    """Added to the medicalcomponent database"""
    model = MedicalComponent
    success_url = reverse_lazy('first-page')
    form_class = MedicalComponentForm
    success_message = 'Dodano wyrób medyczny!'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response


class MedicalcomponentListView(ListView):
    """List of all medicament"""
    model = MedicalComponent
    template_name = 'medicalcomponent_list.html'  # Name template HTML
    context_object_name = 'medicalcomponent'  # Nazwa obiektu w kontekście szablonu

    def get_queryset(self):
        query = self.request.GET.get('search')
        if query:
            # Przeszukiwanie doctora po nazwisku
            return MedicalComponent.objects.filter(name__icontains=query)
        else:
            return MedicalComponent.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        return context


class PatientsPrintOutListView(ListView):
    """ Views for patient printout"""
    model = Patients
    template_name = 'patient_printout.html'  # Name template HTML
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


class PatientsDetailsListView(DetailView):
    """Details one patient"""
    model = Patients
    template_name = 'details_list.html'
    context_object_name = 'patient'
    slug_field = 'id'
    slug_url_kwarg = 'id'


class RegistrationView(View):
    def get(self, request):
        form = RegistrationForm()
        return render(request, 'registration.html', {'form': form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('first-page')
        return render(request, 'registration.html', {'form': form})


class LoginView(View):
    """ Login Users"""

    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('first-page')
        else:
            messages.error(request, 'Niepoprawna nazwa użytkownika lub hasło.')
            return redirect('login')


class LogoutView(LoginRequiredMixin, View):
    """ Logout Users"""

    def get(self, request):
        logout(request)
        return redirect('login')
