"""
URL configuration for careplan project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from patients_app.views import FirstSiteView, AddPatientsView, AddDoctorsView, AddMedicamentView, \
    AddMedicalComponentView, PatientsListView, DoctorsListView, MedicamentListView, MedicalcomponentListView, \
    PatientsPrintOutListView, PatientsUpdateView, PatientsDeleteView, PatientsDetailsListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', FirstSiteView.as_view(), name="first-page"),
    path("add_patients/", AddPatientsView.as_view(), name="add-patients"),
    path("patients_list/", PatientsListView.as_view(), name="patients-list"),
    path("patients/edit/<int:pk>/", PatientsUpdateView.as_view(), name="patients-edit"),
    path('patients/delete/<int:pk>/', PatientsDeleteView.as_view(), name='patient-delete'),
    path("add_doctors/", AddDoctorsView.as_view(), name="add-doctors"),
    path("doctors_list/", DoctorsListView.as_view(), name="doctors-list"),
    path("add_medicament/", AddMedicamentView.as_view(), name="add-medicament"),
    path("medicament_list/", MedicamentListView.as_view(), name="medicament-list"),
    path("add_medicalcomponent/", AddMedicalComponentView.as_view(), name="add-medicalcomponent"),
    path("medicalcomponent_list/", MedicalcomponentListView.as_view(), name="medicalcomponent-list"),
    path("patient_printout/", PatientsPrintOutListView.as_view(), name="patient-printout"),
    path("patient_details/<int:pk>/", PatientsDetailsListView.as_view(), name="patient-details"),
]
