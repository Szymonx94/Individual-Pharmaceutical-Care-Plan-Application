from .models import Patients, Doctors, Medicament, MedicalComponent
from django.forms import ModelForm
from django import forms


class PatientsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PatientsForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Patients
        fields = ['first_name', 'last_name', 'year_of_birth', 'age', 'pesel',
                  'address', 'gender', 'weight', 'growth', 'description_of_diseases', 'drugs_list'
                  ]
        labels = {
            'first_name': 'Imię',
            'last_name': 'Nazwisko',
            'year_of_birth': 'Rok urodzenia',
            'age': 'Wiek',
            'pesel': 'PESEL',
            'address': 'Adres zamieszkania',
            'gender': 'Płeć',
            'weight': 'Waga',
            'growth': 'Wzrost',
            'description_of_diseases': 'Opis chorób',
            'drugs_list': 'Lista leków'
        }


class DoctorsForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(DoctorsForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['placeholder'] = 'Podaj Imię'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Podaj Nazwisko'
        self.fields['specialization'].widget.attrs['placeholder'] = 'Podaj Specjalizację'

    class Meta:
        model = Doctors
        fields = ['first_name', 'last_name', 'specialization']
        labels = {
            'first_name': 'Imię',
            'last_name': 'Nazwisko',
            'specialization': 'Specjalizacja'
        }


class MedicamentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MedicamentForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['name'].widget.attrs['placeholder'] = 'Podaj nazwę'
        self.fields['descriptions'].widget.attrs['placeholder'] = 'Podaj zastosowanie'

    class Meta:
        model = Medicament
        fields = ['name', 'descriptions']
        labels = {
            'name': 'Nazwa',
            'descriptions': 'Opis leku'
        }


class MedicalComponentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MedicalComponentForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['name'].widget.attrs['placeholder'] = 'Podaj nazwę'
        self.fields['description'].widget.attrs['placeholder'] = 'Opis'

    class Meta:
        model = MedicalComponent
        fields = ['name', 'description']
        labels = {
            'name': 'Nazwa',
            'description': 'Opis wyrobu'
        }
