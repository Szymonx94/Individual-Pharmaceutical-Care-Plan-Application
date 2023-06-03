from django.db import models

# Create your models here.


class Medicament(models.Model):
    """
    Model of the drug with a description of the application
    """

    name = models.CharField(max_length=200)
    descriptions = models.CharField(max_length=244)


class Patients(models.Model):
    """
    Basic patients data
    """

    GENDER_CHOICES = (
        ("M", "Mężczyzna"),
        ("K", "Kobieta"),
    )
    first_name = models.CharField(max_length=64, blank=True)
    last_name = models.CharField(max_length=64, blank=True)
    year_of_birth = models.PositiveIntegerField(null=True)
    age = models.PositiveIntegerField(null=True)
    pesel = models.CharField(max_length=11)
    address = models.CharField(max_length=200)
    gender = models.CharField(default="M", choices=GENDER_CHOICES)
    weight = models.IntegerField(null=True)
    growth = models.IntegerField(null=True)
    description_of_diseases = models.TextField()
    drugs_list = models.TextField()
    medicament = models.ManyToManyField(Medicament, related_name="patients")

    def __str__(self):
        return self.first_name, self.last_name


class Doctors(models.Model):
    """
    Data of doctors with a description of specialization
    """

    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    specialization = models.CharField(max_length=100)
    email = models.EmailField(max_length=254, default="")


class MedicalComponent(models.Model):
    """
    Data on medical devices
    """

    name = models.CharField(max_length=64)
    description = models.TextField()
    patients = models.ManyToManyField(Patients, related_name="medical_component")


class Slider(models.Model):
    """
        Model for view slider in first site
    """

    title = models.CharField(max_length=100, blank=False)
    description = models.TextField(max_length=800, blank=False)
    image = models.ImageField(upload_to="static/", blank=False)

    def __str__(self):
        return self.title


class MedicalNote(models.Model):
    """
    Model medical note for doctor
    """

    patient = models.ForeignKey(
        Patients, on_delete=models.CASCADE, related_name="medical_notes"
    )
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Prescription(models.Model):
    """
        Model medical note for patient
    """

    patient = models.ForeignKey(
        Patients, on_delete=models.CASCADE, related_name="prescriptions"
    )
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
