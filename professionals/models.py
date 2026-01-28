from django.db import models
from django.contrib.auth.models import User

class Professional(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='professional')
    dni = models.CharField(max_length=20, unique=True, verbose_name="DNI / ID Document")
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    professional_license_number = models.CharField(max_length=50, verbose_name="License Number")
    working_days_and_hours = models.TextField(blank=True, help_text="e.g. Mon-Fri 9-17")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.professional_license_number})"
