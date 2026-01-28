from django.db import models

class Patient(models.Model):
    created_by = models.ForeignKey('professionals.Professional', on_delete=models.CASCADE, related_name='patients')
    dni = models.CharField(max_length=20, verbose_name="DNI / ID Document")
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField()
    mobile_phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    medical_coverage = models.CharField(max_length=100, blank=True)
    social_security_number = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class FamilyContact(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='contacts')
    relationship_to_patient = models.CharField(max_length=50, verbose_name="Relationship")
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    mobile_phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.relationship_to_patient})"
