from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.template.response import TemplateResponse
from django.views import View
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    CreateView,
    ListView,
    UpdateView,
    DeleteView,
    DetailView,
)
from django.contrib.messages.views import SuccessMessageMixin
from .forms import (
    PatientsForm,
    DoctorsForm,
    MedicamentForm,
    MedicalComponentForm,
    RegistrationForm,
    MedicalNoteForm,
    PrescriptionForm,
    DateAddForm,
)
from .models import (
    Patients,
    Doctors,
    Medicament,
    MedicalComponent,
    Slider,
    MedicalNote,
    Prescription,
    DateAdd,
)
from django.contrib import messages


# Create your views here.


class FirstSiteView(View):
    """
    View first site
    """

    @staticmethod
    def get(request):
        sliderdata = Slider.objects.all()
        context = {"slider": sliderdata}
        return TemplateResponse(request, "first_page.html", context)


class AddPatientsView(SuccessMessageMixin, CreateView):
    """Added to the patient database"""

    model = Patients
    success_url = reverse_lazy("first-page")
    form_class = PatientsForm
    success_message = "Dodano pacjenta!"

    def form_valid(self, form):
        response = super().form_valid(form)
        self.success_message = f"Dodano pacjenta do bazy"
        self.success_url = self.get_success_url() + "?success=true"
        messages.success(self.request, self.success_message)
        return response


class PatientsListView(ListView):
    """List of all patients"""

    model = Patients
    template_name = "patients_list.html"
    ordering = "id"
    context_object_name = "patients"

    def get_queryset(self):
        query = self.request.GET.get("search")
        if query:
            # Przeszukiwanie pacjentów po nazwisku
            return Patients.objects.filter(pesel__icontains=query).order_by("id")
        else:
            return Patients.objects.all().order_by("id")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_query"] = self.request.GET.get("search", "")
        return context


class PatientsUpdateView(UpdateView):
    """Class to edit the patient"""

    model = Patients
    form_class = PatientsForm
    template_name = "patients_update.html"
    success_url = reverse_lazy("patients-list")

    def form_valid(self, form):
        patient = form.instance
        patient.first_name = form.cleaned_data["first_name"]
        patient.last_name = form.cleaned_data["last_name"]
        patient.save()
        return super().form_valid(form)


class PatientsDeleteView(DeleteView):
    """Delete patients"""

    model = Patients
    template_name = "patients_delete.html"
    success_url = reverse_lazy("patients-list")


class AddDoctorsView(CreateView):
    """Add to the doctor in database"""

    model = Doctors
    success_url = reverse_lazy("first-page")
    form_class = DoctorsForm

    def __init__(self, **kwargs):
        super().__init__(kwargs)
        self.success_message = None

    def form_valid(self, form):
        response = super().form_valid(form)
        self.success_message = f"Dodano lekarza do bazy"
        self.success_url = self.get_success_url() + "?success=true"
        messages.success(self.request, self.success_message)
        return response


class DoctorsListView(ListView):
    """List of all doctors"""

    model = Doctors
    template_name = "doctors_list.html"  # Name template HTML
    context_object_name = "doctors"

    def get_queryset(self):
        query = self.request.GET.get("search")
        if query:
            # Przeszukiwanie doctora po nazwisku
            return Doctors.objects.filter(last_name__icontains=query)
        else:
            return Doctors.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_query"] = self.request.GET.get("search", "")
        return context


class DoctorsDeleteView(DeleteView):
    """Delete doctor"""

    model = Doctors
    template_name = "doctors_delete.html"
    success_url = reverse_lazy("doctors-list")


class AddMedicamentView(SuccessMessageMixin, CreateView):
    """Added to the medicament database"""

    model = Medicament
    success_url = reverse_lazy("first-page")
    form_class = MedicamentForm

    def form_valid(self, form):
        response = super().form_valid(form)
        self.success_message = f"Dodano lek do bazy"
        self.success_url = self.get_success_url() + "?success=true"
        messages.success(self.request, self.success_message)
        return response


class MedicamentListView(ListView):
    """List of all medicament"""

    model = Medicament
    template_name = "medicament_list.html"  # Name template HTML
    context_object_name = "medicament"

    def get_queryset(self):
        query = self.request.GET.get("search")
        if query:
            # Searching a doctor by name
            return Medicament.objects.filter(name__icontains=query)
        else:
            return Medicament.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_query"] = self.request.GET.get("search", "")
        return context


class MedicamentDeleteView(DeleteView):
    """Delete medicament"""

    model = Medicament
    template_name = "medicament_delete.html"
    success_url = reverse_lazy("medicament-list")


class AddMedicalComponentView(SuccessMessageMixin, CreateView):
    """Added to the medicalcomponent database"""

    model = MedicalComponent
    success_url = reverse_lazy("first-page")
    form_class = MedicalComponentForm

    def form_valid(self, form):
        response = super().form_valid(form)
        self.success_message = f"Dodano wyrób medyczny do bazy"
        self.success_url = self.get_success_url() + "?success=true"
        messages.success(self.request, self.success_message)
        return response


class MedicalcomponentListView(ListView):
    """List of all medicament"""

    model = MedicalComponent
    template_name = "medicalcomponent_list.html"  # Name template HTML
    context_object_name = "medicalcomponent"

    def get_queryset(self):
        query = self.request.GET.get("search")
        if query:
            return MedicalComponent.objects.filter(name__icontains=query)
        else:
            return MedicalComponent.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_query"] = self.request.GET.get("search", "")
        return context


class DoctorPrintOutListView(ListView):
    """Views for doctor printout"""

    model = Patients
    template_name = "doctor_printout.html"  # Name template HTML
    context_object_name = "patients"  # Nazwa obiektu w kontekście szablonu

    def get_queryset(self):
        query = self.request.GET.get("search")
        if query:
            # Searching patients by name
            return Patients.objects.filter(pesel__icontains=query).order_by("id")
        else:
            return Patients.objects.all().order_by("id")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_query"] = self.request.GET.get("search", "")
        return context


class PatientPrintOutListView(ListView):
    """Views for patients printout"""

    model = Patients
    template_name = "patient_printout.html"  # Name template HTML
    context_object_name = "patients"

    def get_queryset(self):
        query = self.request.GET.get("search")
        if query:
            return Patients.objects.filter(pesel__icontains=query).order_by("id")
        else:
            return Patients.objects.all().order_by("id")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_query"] = self.request.GET.get("search", "")
        return context


class PatientsDetailsListView(DetailView):
    """Details one patient"""

    model = Patients
    template_name = "details_list.html"
    context_object_name = "patient"
    slug_field = "id"
    slug_url_kwarg = "id"


class RegistrationView(View):
    """ View registratrion for new users"""

    def get(self, request):
        form = RegistrationForm()
        return render(request, "registration.html", {"form": form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("first-page")
        return render(request, "registration.html", {"form": form})


class LoginView(View):
    """Login Users"""

    def get(self, request):
        return render(request, "login.html")

    def post(self, request):
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("first-page")
        else:
            messages.error(request, "Niepoprawna nazwa użytkownika lub hasło.")
            return redirect("login")


class LogoutView(LoginRequiredMixin, View):
    """Logout Users"""

    def get(self, request):
        logout(request)
        return redirect("login")


class AddMedicationView(View):
    """Added to the patients list new actual medicament"""

    template_name = "patient_medicament_add.html"

    def get(self, request, patient_id):
        medications = Medicament.objects.all()
        return render(
            request,
            self.template_name,
            {"medications": medications, "patient_id": patient_id},
        )

    def post(self, request, patient_id):
        medication_ids = request.POST.getlist("medication")
        patient = Patients.objects.get(id=patient_id)

        for medication_id in medication_ids:
            medication = Medicament.objects.get(id=medication_id)
            patient.medicament.add(medication)

        return redirect(reverse("patient-details", kwargs={"pk": patient_id}))


class AddMedicalComponentForPatientView(View):
    """Add new medical components to the patient's list"""

    template_name = "patient_medical_component_add.html"

    def get(self, request, patient_id):
        medical_components = MedicalComponent.objects.all()
        return render(
            request,
            self.template_name,
            {"medical_components": medical_components, "patient_id": patient_id},
        )

    def post(self, request, patient_id):
        medical_component_id_list = request.POST.getlist("medical_component")
        patient = get_object_or_404(Patients, id=patient_id)

        for medical_component_id in medical_component_id_list:
            medical_component = get_object_or_404(
                MedicalComponent, id=medical_component_id
            )
            medical_component.patients.add(
                patient
            )  # We add the patient to the ManyToManyField

        # patient = get_object_or_404(Patients, id=patient_id)

        return redirect(reverse("patient-details", kwargs={"pk": patient_id}))


class MedicalNoteCreateView(CreateView):
    """For details list can create new MedicalNote"""

    model = MedicalNote
    form_class = MedicalNoteForm
    template_name = "medicalnote_form.html"

    def form_valid(self, form):
        patient_id = self.kwargs["patient_id"]
        patient = get_object_or_404(Patients, id=patient_id)
        form.instance.patient = patient
        return super().form_valid(form)

    def get_success_url(self):
        # patient_id = self.kwargs['patient_id']
        return reverse_lazy("patient-details", kwargs={"pk": self.kwargs["patient_id"]})


class PrescriptionCreateView(CreateView):
    """For details list can create new MedicalNote for doctor"""

    model = Prescription
    form_class = PrescriptionForm
    template_name = "prescription_form.html"

    def form_valid(self, form):
        patient_id = self.kwargs["patient_id"]
        patient = get_object_or_404(Patients, id=patient_id)
        form.instance.patient = patient
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("patient-details", kwargs={"pk": self.kwargs["patient_id"]})


class DateAddCreateView(CreateView):
    """View DataAdd - data vist patient"""

    model = DateAdd
    form_class = DateAddForm
    template_name = "date_add_form.html"

    def form_valid(self, form):
        patient_id = self.kwargs["patient_id"]
        patient = get_object_or_404(Patients, id=patient_id)
        form.instance.patients = patient
        return super().form_valid(form)

    def get_success_url(self):
        patient_id = self.kwargs["patient_id"]
        return reverse("patient-details", kwargs={"pk": patient_id})


class DetailForPatientsListView(DetailView):
    """Views for patients printout"""

    model = Patients
    template_name = "detail_list_for_patients.html"  # Name template HTML
    context_object_name = "patient"
    slug_field = "id"
    slug_url_kwarg = "id"


class DetailForDoctorsListView(DetailView):
    """Views for doctors printout"""

    model = Patients
    template_name = "detail_list_for_doctors.html"  # Name template HTML
    context_object_name = "patient"
    slug_field = "id"
    slug_url_kwarg = "id"
