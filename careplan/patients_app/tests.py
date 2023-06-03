from unittest import TestCase

from django.contrib.auth.backends import UserModel
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse
from .models import (
    Slider,
    Patients,
    Doctors,
    Medicament,
    MedicalComponent,
    MedicalNote,
    Prescription,

)
from .forms import PatientsForm, RegistrationForm
import pytest


@pytest.mark.django_db
def test_main():
    client = Client()
    response = client.get("/")
    assert response.status_code == 200


def test_an_admin_view(admin_client):
    response = admin_client.get("/admin/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_first_site_view(client):
    slider = Slider.objects.create(
        title="Slider 1", description="To jest nowa aplikacja", image="slider1.jpg"
    )
    response = client.get(reverse("first-page"))
    assert response.status_code == 200
    assert slider.title in str(response.content)
    assert slider.description in str(response.content)
    assert slider.image.url in str(response.content)


@pytest.mark.django_db
def test_add_patients_view(client):
    response = client.get(reverse("add-patients"))
    assert response.status_code == 200
    assert isinstance(response.context["form"], PatientsForm)


@pytest.mark.django_db
def test_add_patients_view_form_validation(client):
    data = {
        "last_name": "Zietek",

    }
    response = client.post(reverse("add-patients"), data=data, follow=True)
    assert response.redirect_chain == []
    assert "field is required" in response.content.decode()
    assert Patients.objects.count() == 0


@pytest.mark.django_db
def test_add_patients_view_get(client):
    response = client.get(reverse("add-patients"))
    assert response.status_code == 200
    assert response.template_name == ["patients_app/patients_form.html"]
    assert "form" in response.context
    form = response.context["form"]
    assert isinstance(form, PatientsForm)

@pytest.mark.django_db
def test_patients_list_view(client, patients):
    response = client.get(reverse("patients-list"))
    assert response.status_code == 200
    assert "patients" in response.context
    assert len(response.context["patients"]) == Patients.objects.count()
    assert "search_query" in response.context
    assert response.context["search_query"] == ""


@pytest.mark.django_db
def test_patients_list_view_search(client, patients):
    response = client.get(reverse("patients-list"), {"search": "15131612145"})
    assert response.status_code == 200
    assert "patients" in response.context
    assert len(response.context["patients"]) == 1
    assert "search_query" in response.context
    assert response.context["search_query"] == "15131612145"


@pytest.mark.django_db
def test_patients_update_view_get(user, client, patients):
    client.force_login(user=user)
    response = client.get(reverse("patients-edit", kwargs={"pk": patients.id}))
    assert response.status_code == 200


@pytest.mark.django_db
def test_patients_update_view_invalid_form(client):
    patient = Patients.objects.create(first_name="John", last_name="Doe")
    url = reverse("patients-edit", kwargs={"pk": patient.pk})
    data = {
        "first_name": "",
        "last_name": "Zietek",
    }
    response = client.post(url, data=data)
    assert response.status_code == 200
    assert "patients_update.html" in [t.name for t in response.templates]
    assert response.context["form"].errors


@pytest.mark.django_db
def test_get_patients_delete_view(client, user, patients):
    client.force_login(user=user)
    response = client.get(reverse("patient-delete", kwargs={"pk": patients.id}))
    assert response.status_code == 200
    assert response.template_name == ["patients_delete.html"]


@pytest.mark.django_db
def test_post_patients_delete_view(client, user, patients):
    client.force_login(user=user)
    response = client.post(reverse("patient-delete", kwargs={"pk": patients.id}))
    assert response.status_code == 302
    assert response.url == reverse("patients-list")
    assert not Patients.objects.filter(pk=patients.pk).exists()


@pytest.mark.django_db
def test_add_doctors_view_post(client):
    data = {
        "first_name": "John",
        "last_name": "Doe",
        "specialization": "Cardiology",
        "email": "johndoe@example.com",
    }
    response = client.post(reverse("add-doctors"), data=data, follow=True)
    assert Doctors.objects.count() == 1
    assert response.template_name == "first_page.html"


@pytest.mark.django_db
def test_doctors_list_view_with_search(client, doctors):
    response = client.get(reverse("doctors-list"), {"search": "Doe"})
    assert response.status_code == 200
    assert "doctors" in response.context
    assert len(response.context["doctors"]) == 1


@pytest.mark.django_db
def test_doctors_list_view_without_search(client, doctors):
    response = client.get(reverse("doctors-list"))
    assert response.status_code == 200
    assert "doctors" in response.context
    assert len(response.context["doctors"]) == 3


@pytest.mark.django_db
def test_doctor_delete_view_get(client, user, doctor):
    client.force_login(user=user)
    response = client.get(reverse("doctor-delete", kwargs={"pk": doctor.id}))
    assert response.status_code == 200
    assert response.template_name == ["doctors_delete.html"]


@pytest.mark.django_db
def test_doctor_delete_view_post(client, user, doctor):
    client.force_login(user=user)
    response = client.post(reverse("doctor-delete", kwargs={"pk": doctor.id}))
    assert response.status_code == 302
    assert response.url == reverse("doctors-list")
    assert not Doctors.objects.filter(pk=doctor.pk).exists()


@pytest.mark.django_db
def test_add_medicament_view(client):
    data = {
        "name": "Halset",
        "desriptions": "Lek na ból gardła",
    }
    response = client.post(reverse("add-medicament"), data=data, follow=True)
    assert response.template_name == ["patients_app/medicament_form.html"]


@pytest.mark.django_db
def test_medicament_list_view_with_search(client):
    medicament1 = Medicament.objects.create(name="Aspirin", descriptions="Lek na grypę")
    medicament2 = Medicament.objects.create(
        name="Paracetamol", descriptions="Lek na ból głowy"
    )
    response = client.get(reverse("medicament-list"), {"search": "Aspirin"})
    assert response.status_code == 200
    assert "medicament" in response.context
    medicament_list = response.context["medicament"]
    assert medicament1 in medicament_list
    assert medicament2 not in medicament_list
    assert response.context["search_query"] == "Aspirin"


@pytest.mark.django_db
def test_medicament_list_view_without_search(client):
    medicament1 = Medicament.objects.create(name="Aspirin", descriptions="Lek na grypę")
    medicament2 = Medicament.objects.create(
        name="Paracetamol", descriptions="Lek na ból głowy"
    )
    response = client.get(reverse("medicament-list"))
    assert response.status_code == 200
    assert "medicament" in response.context
    medicament_list = response.context["medicament"]
    assert medicament1 in medicament_list
    assert medicament2 in medicament_list
    assert response.context["search_query"] == ""


@pytest.mark.django_db
def test_medicament_delete_view_get(client, user, medicaments):
    client.force_login(user=user)
    response = client.get(reverse("medicament-delete", kwargs={"pk": medicaments.id}))
    assert response.status_code == 200
    assert response.template_name == ["medicament_delete.html"]


@pytest.mark.django_db
def test_medicament_delete_view_post(client, user, medicaments):
    client.force_login(user=user)
    response = client.post(reverse("medicament-delete", kwargs={"pk": medicaments.id}))
    assert response.status_code == 302
    assert response.url == reverse("medicament-list")
    assert not Medicament.objects.filter(pk=medicaments.pk).exists()


@pytest.mark.django_db
def test_add_medical_component_view_invalid_form(client):
    data = {
        "name": "",
        "description": "Produkt do leczenia",
    }
    response = client.post(reverse("add-medicalcomponent"), data=data, follow=True)
    assert response.context["form"].errors == {"name": ["This field is required."]}


@pytest.mark.django_db
def test_doctor_printout_view_with_search(client):
    patient1 = Patients.objects.create(
        first_name="Jan", last_name="Kowalski", pesel="12345678901"
    )
    patient2 = Patients.objects.create(
        first_name="Anna", last_name="Nowak", pesel="98765432109"
    )
    patient3 = Patients.objects.create(
        first_name="Adam", last_name="Nowicki", pesel="56789012345"
    )
    response = client.get(reverse("doctor-printout"), {"search": "56789012345"})
    assert response.status_code == 200
    assert len(response.context["patients"]) == 1
    assert response.context["patients"][0].pesel == "56789012345"


@pytest.mark.django_db
def test_patient_printout_view_with_search(client):
    patient1 = Patients.objects.create(
        first_name="Jan", last_name="Kowalski", pesel="12345678901"
    )
    patient2 = Patients.objects.create(
        first_name="Anna", last_name="Nowak", pesel="98765432109"
    )
    patient3 = Patients.objects.create(
        first_name="Adam", last_name="Nowicki", pesel="56789012345"
    )
    response = client.get(reverse("patient-printout"), {"search": "56789012345"})
    assert response.status_code == 200
    assert len(response.context["patients"]) == 1
    assert response.context["patients"][0].pesel == "56789012345"


@pytest.mark.django_db
def test_patient_details_view(client):
    # Tworzenie pacjenta do testu
    patient = Patients.objects.create(
        first_name="Jan", last_name="Kowalski", pesel="12345678901"
    )
    response = client.get(reverse("patient-details", kwargs={"pk": patient.id}))
    assert response.status_code == 200
    assert response.context["patient"].id == patient.id
    assert response.context["patient"].first_name == "Jan"
    assert response.context["patient"].last_name == "Kowalski"
    assert response.context["patient"].pesel == "12345678901"


@pytest.mark.django_db
def test_patient_details_view_invalid_id(client):
    response = client.get(reverse("patient-details", kwargs={"pk": 9954599}))
    assert response.status_code == 404


@pytest.mark.django_db
def test_registration_view_invalid_form(client):
    response = client.post(reverse("register"), data={})
    assert isinstance(response.context["form"], RegistrationForm)


@pytest.mark.django_db
class LoginViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse("login")
        self.first_page_url = reverse("first-page")
        self.username = "testuser"
        self.password = "testpassword"
        self.user = User.objects.create_user(
            username=self.username, password=self.password
        )

    def test_login_view_get(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)


@pytest.mark.django_db
def test_add_medication_view_get(client):
    patient = Patients.objects.create(first_name="Kamil")
    medicament1 = Medicament.objects.create(name="Medicament 1")
    medicament2 = Medicament.objects.create(name="Medicament 2")
    url = reverse("add_medication", kwargs={"patient_id": patient.id})

    response = client.get(url)

    assert response.status_code == 200
    assert any(
        template.name == "patient_medicament_add.html"
        for template in response.templates
    )
    assert medicament1.name in response.content.decode()
    assert medicament2.name in response.content.decode()
    assert response.context["patient_id"] == patient.id


@pytest.mark.django_db
def test_add_medical_component_view_get(client):
    patient = Patients.objects.create(first_name="Kamil")
    component1 = MedicalComponent.objects.create(name="Component 1")
    component2 = MedicalComponent.objects.create(name="Component 2")
    url = reverse("add_medical_component", kwargs={"patient_id": patient.id})

    response = client.get(url)

    assert response.status_code == 200
    assert any(
        template.name == "patient_medical_component_add.html"
        for template in response.templates
    )
    assert component1.name in response.content.decode()
    assert component2.name in response.content.decode()
    assert response.context["patient_id"] == patient.id


@pytest.mark.django_db
def test_medical_note_create_view_post(client):
    patient = Patients.objects.create(first_name="Kamil")
    data = {
        "description": "Notatka.",
    }
    url = reverse("add-medicalnote", kwargs={"patient_id": patient.id})
    response = client.post(url, data=data)
    assert response.status_code == 302  # Check the expected redirect status code
    medical_note = MedicalNote.objects.last()
    assert medical_note.patient == patient
    assert medical_note.description == data["description"]


@pytest.mark.django_db
def test_prescription_create_view_post(client):
    patient = Patients.objects.create(first_name="Kamil")
    data = {
        "description": "Notatka dla lekarza",
    }
    url = reverse("add-prescription", kwargs={"patient_id": patient.id})
    response = client.post(url, data=data)
    assert response.status_code == 302  # Check the expected redirect status code
    medical_note = Prescription.objects.last()
    assert medical_note.patient == patient
    assert medical_note.description == data["description"]




@pytest.mark.django_db
def test_detail_for_patients_list_view():
    client = Client()
    patient = Patients.objects.create(first_name="Kamil", last_name="Kowalski")
    url = reverse("patient-details", kwargs={"pk": patient.id})

    response = client.get(url)

    assert response.status_code == 200
    assert response.template_name == ["details_list.html"]
    assert response.context["patient"] == patient
