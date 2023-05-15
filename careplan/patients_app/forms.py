from .models import Patients, Doctors
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
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Doctors
        fields = ['first_name', 'last_name', 'specialization']

