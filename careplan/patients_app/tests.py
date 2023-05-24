from django.test import Client
from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages
from .models import MedicalComponent
from .forms import MedicalComponentForm
import pytest

def test_main():
    client = Client()
    response = client.get('/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_add_medical_component_success(self):
    response = self.client.post(self.url, data=self.valid_data)
    self.assertRedirects(response, reverse('first-page') + '?success=true')
    self.assertEqual(response.status_code, 302)

    # Check if the success message is displayed
    messages = list(get_messages(response.wsgi_request))
    self.assertEqual(len(messages), 1)
    self.assertEqual(str(messages[0]), 'Dodano wyrób medyczny!')

    # Check if the medical component is created in the database
    self.assertEqual(MedicalComponent.objects.count(), 1)
    medical_component = MedicalComponent.objects.first()
    self.assertEqual(medical_component.name, 'Medical Component 1')
    self.assertEqual(medical_component.description, 'Test description')


@pytest.mark.django_db
def test_add_medical_component_invalid_data(self):
    response = self.client.post(self.url, data=self.invalid_data)
    self.assertEqual(response.status_code, 200)

    # Check if the form is displayed again with errors
    self.assertTemplateUsed(response, 'your_template_name.html')
    form = response.context['form']
    self.assertIsInstance(form, MedicalComponentForm)
    self.assertTrue(form.errors)