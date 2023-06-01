from django.test import Client
from django.urls import reverse
from .models import Slider, Patients
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
def test_add_patients_view_post(client, patients):
    response = client.post(reverse('add-patients'), data=patients, follow=True)
    assert response.status_code == 200
    assert Patients.objects.count() == 1


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
def test_update_patients_view(user, client, patients):
    client.force_login(user=user)
    response = client.get(reverse('patients-edit', kwargs={"pk": patients.id}))
    assert response.status_code == 200
    edit = {
        "first_name": 'Kamil',
        "last_name": 'Kowalski',
        "year_of_birth": 1994,
        "age": 32,
    }
    response = client.post(
        reverse('patients-edit', kwargs={"pk": patients.id}), data=edit
    )
    assert response.status_code == 302
    patients.refresh_from_db()
    assert patients.first_name == edit["first_name"]
    assert patients.last_name == edit["last_name"]
    assert patients.year_of_birth == edit["year_of_birth"]
    assert patients.age == edit["age"]
