from django import forms
from .models import Patient, FamilyContact

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        exclude = ['created_by', 'created_at']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }

class FamilyContactForm(forms.ModelForm):
    class Meta:
        model = FamilyContact
        exclude = ['patient']
