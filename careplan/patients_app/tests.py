from unittest import TestCase

from django.test import Client
from django.urls import reverse
from .models import Slider, Patients, Doctors, Medicament, MedicalComponent
from .forms import PatientsForm
import pytest


@pytest.mark.django_db
def test_main():
    client = Client()
    response = client.get('/')
    assert response.status_code == 200


def test_an_admin_view(admin_client):
    response = admin_client.get("/admin/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_first_site_view(client):
    slider = Slider.objects.create(title='Slider 1', description='To jest nowa aplikacja', image='slider1.jpg')
    response = client.get(reverse('first-page'))
    assert response.status_code == 200
    assert slider.title in str(response.content)
    assert slider.description in str(response.content)
    assert slider.image.url in str(response.content)


@pytest.mark.django_db
def test_add_patients_view(client):
    response = client.get(reverse('add-patients'))
    assert response.status_code == 200
    assert isinstance(response.context['form'], PatientsForm)

@pytest.mark.django_db
def test_add_patients_view_post(client):
    data = {
        "first_name": "Szymon",
        "last_name": "Zietek",
        "year_of_birth": "1994",
        "age": "34",
        "pesel": "15131612145",
        "address": "Warszawa",
        "gender": "Mężczyzna",
        "weight": "100",
        "growth": "178",
        "description_of_diseases": "Opis chorób",
        "drugs_list": "Lista leków"
    }
    response = client.post(reverse('add-patients'), data=data, follow=True)
    assert response.status_code == 200
    assert Patients.objects.count() == 0



@pytest.mark.django_db
def test_patients_list_view(client, patients):
    response = client.get(reverse('patients-list'))
    assert response.status_code == 200
    assert 'patients' in response.context
    assert len(response.context['patients']) == Patients.objects.count()
    assert 'search_query' in response.context
    assert response.context['search_query'] == ''


@pytest.mark.django_db
def test_patients_list_view_search(client, patients):
    response = client.get(reverse('patients-list'), {'search': '15131612145'})
    assert response.status_code == 200
    assert 'patients' in response.context
    assert len(response.context['patients']) == 1
    assert 'search_query' in response.context
    assert response.context['search_query'] == '15131612145'


@pytest.mark.django_db
def test_patients_update_view_get(user, client, patients):
    client.force_login(user=user)
    response = client.get(reverse('patients-edit', kwargs={'pk': patients.id}))
    assert response.status_code == 200

# @pytest.mark.django_db
# def test_patients_update_view_post(client):
#     patients = Patients.objects.create(first_name='Szymon', last_name='Zietek', year_of_birth=1994, age=34)
#
#     edit_data = {
#         "first_name": "Kamil",
#         "last_name": "Kowalski",
#         "year_of_birth": 1994,
#         "age": 32,
#     }
#
#     url = reverse('patients-edit', kwargs={'pk': patients.pk})
#     response = client.post(url, data=edit_data)
#
#     updated_patient = Patients.objects.get(pk=patients.pk)
#     assert updated_patient.first_name == edit_data["first_name"]
#     assert updated_patient.last_name == edit_data["last_name"]
#     assert updated_patient.year_of_birth == edit_data["year_of_birth"]
#     assert updated_patient.age == edit_data["age"]
#
#     assert response.status_code == 302
#     assert response.url == reverse('patients-list')

@pytest.mark.django_db
def test_get_delete_view(client, user, patients):
    client.force_login(user=user)
    response = client.get(reverse('patient-delete', kwargs={'pk': patients.id}))
    assert response.status_code == 200
    assert response.template_name == ['patients_delete.html']

@pytest.mark.django_db
def test_post_delete_view(client, user, patients):
    client.force_login(user=user)
    response = client.post(reverse('patient-delete', kwargs={'pk': patients.id}))
    assert response.status_code == 302
    assert response.url == reverse('patients-list')
    assert not Patients.objects.filter(pk=patients.pk).exists()

@pytest.mark.django_db
def test_add_doctors_view_post(client):
    data = {
        "first_name": "John",
        "last_name": "Doe",
        "specialization": "Cardiology",
        "email": "johndoe@example.com",
    }
    response = client.post(reverse('add-doctors'), data=data, follow=True)
    assert response.status_code == 200
    assert Doctors.objects.count() == 1
    assert response.template_name == 'first_page.html'

@pytest.mark.django_db
def test_doctors_list_view_with_search(client, doctors):
    response = client.get(reverse('doctors-list'), {'search': 'Doe'})
    assert response.status_code == 200
    assert 'doctors' in response.context
    assert len(response.context['doctors']) == 1

@pytest.mark.django_db
def test_doctors_list_view_without_search(client, doctors):
    response = client.get(reverse('doctors-list'))
    assert response.status_code == 200
    assert 'doctors' in response.context
    assert len(response.context['doctors']) == 3

@pytest.mark.django_db
def test_add_medicament_view(client):
    data = {
        "name": "Halset",
        "desriptions": "Lek na ból gardła",

    }
    response = client.post(reverse('add-medicament'), data=data, follow=True)
    assert response.status_code == 200
    assert Medicament.objects.count() == 0
    assert response.template_name == ['patients_app/medicament_form.html']

@pytest.mark.django_db
def test_medicament_list_view_with_search(client):
    medicament1 = Medicament.objects.create(name="Aspirin", descriptions="Lek na grypę")
    medicament2 = Medicament.objects.create(name="Paracetamol", descriptions="Lek na ból głowy")
    response = client.get(reverse('medicament-list'), {'search': 'Aspirin'})
    assert response.status_code == 200
    assert 'medicament' in response.context
    medicament_list = response.context['medicament']
    assert medicament1 in medicament_list
    assert medicament2 not in medicament_list
    assert response.context['search_query'] == 'Aspirin'


@pytest.mark.django_db
def test_medicament_list_view_without_search(client):
    medicament1 = Medicament.objects.create(name="Aspirin", descriptions="Lek na grypę")
    medicament2 = Medicament.objects.create(name="Paracetamol", descriptions="Lek na ból głowy")
    response = client.get(reverse('medicament-list'))
    assert response.status_code == 200
    assert 'medicament' in response.context
    medicament_list = response.context['medicament']
    assert medicament1 in medicament_list
    assert medicament2 in medicament_list
    assert response.context['search_query'] == ''

@pytest.mark.django_db
def test_add_medical_component_view_invalid_form(client):
    data = {
        "name": "",
        "description": "Produkt do leczenia",
    }
    response = client.post(reverse('add-medicalcomponent'), data=data, follow=True)
    assert response.status_code == 200
    assert MedicalComponent.objects.count() == 0
    assert response.context['form'].errors == {
        'name': ['This field is required.']
    }

@pytest.mark.django_db
def test_doctor_printout_view_with_search(client):
    patient1 = Patients.objects.create(first_name="Jan", last_name="Kowalski", pesel="12345678901")
    patient2 = Patients.objects.create(first_name="Anna", last_name="Nowak", pesel="98765432109")
    patient3 = Patients.objects.create(first_name="Adam", last_name="Nowicki", pesel="56789012345")
    response = client.get(reverse('doctor-printout'), {'search': '56789012345'})
    assert response.status_code == 200
    assert len(response.context['patients']) == 1
    assert response.context['patients'][0].pesel == '56789012345'

@pytest.mark.django_db
def test_doctor_printout_view_without_search(client):
    # Tworzenie pacjentów do testu
    patient1 = Patients.objects.create(first_name="Jan", last_name="Kowalski", pesel="12345678901")
    patient2 = Patients.objects.create(first_name="Anna", last_name="Nowak", pesel="98765432109")
    patient3 = Patients.objects.create(first_name="Adam", last_name="Nowicki", pesel="56789012345")
    response = client.get(reverse('doctor-printout'))
    assert response.status_code == 200
    assert len(response.context['patients']) == 3
    assert response.context['patients'][0].id < response.context['patients'][1].id < response.context['patients'][2].id
