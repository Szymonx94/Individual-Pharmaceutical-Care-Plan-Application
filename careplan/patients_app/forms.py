from .models import Patients, Doctors, Medicament
from django.forms import ModelForm
from django import forms


class PatientsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PatientsForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Patients
        fields = ['first_name', 'last_name', 'year_of_birth', 'age', 'pesel', 'address', 'gender', 'weight',
                  'growth', 'description_of_diseases', 'drugs_list']


class DoctorsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DoctorsForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Podaj Imię'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Podaj Nazwisko'
        self.fields['specialization'].widget.attrs['placeholder'] = 'Podaj Specjalizację'

    class Meta:
        model = Doctors
        fields = ['first_name', 'last_name', 'specialization']


class MedicamentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MedicamentForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'Podaj nazwę'
        self.fields['descriptions'].widget.attrs['placeholder'] = 'Podaj zastosowanie'

    class Meta:
        model = Medicament
        fields = ['name', 'descriptions']
