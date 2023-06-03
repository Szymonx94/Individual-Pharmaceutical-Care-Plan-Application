from django.contrib.auth.models import User
import pytest
from django.forms import model_to_dict
from django.test import Client
from .models import *


@pytest.fixture
def user():
    user = User.objects.create_user(id=1, username="user", password="")
    return user


@pytest.fixture
def client():
    new = Client()
    return new


@pytest.fixture
def patients():
    patient = Patients.objects.create(
        first_name="Janusz",
        last_name="Zietek",
        year_of_birth="1994",
        age="34",
        pesel="15131612145",
        address="Warszawa",
        gender="Mężczyzna",
        weight="100",
        growth="178",
        description_of_diseases="Opis chorób",
        drugs_list="Lista leków",
    )
    return patient


@pytest.fixture
def doctors():
    data = [
        {"first_name": "Jan", "last_name": "Drak"},
        {"first_name": "Jarek", "last_name": "Doe"},
        {"first_name": "Antoni", "last_name": "Smith"},
    ]

    doctors = []
    for entry in data:
        doctor = Doctors.objects.create(
            first_name=entry["first_name"], last_name=entry["last_name"]
        )
        doctors.append(doctor)

    return doctors


@pytest.fixture
def doctor():
    doc = Doctors.objects.create(
        first_name="Szymon",
        last_name="Kowalski",
        specialization="Laryngolog",
        email="sz@wp.pl",
    )
    return doc


@pytest.fixture
def medicaments():
    medi = Medicament.objects.create(name="Halset", descriptions="Lek doustny")
    return medi
