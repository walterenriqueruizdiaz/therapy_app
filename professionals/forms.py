from django import forms
from .models import Professional

class ProfessionalForm(forms.ModelForm):
    class Meta:
        model = Professional
        fields = ['dni', 'first_name', 'last_name', 'professional_license_number', 'working_days_and_hours']
        widgets = {
            'working_days_and_hours': forms.Textarea(attrs={'rows': 3}),
        }
