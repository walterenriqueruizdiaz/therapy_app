from django import forms
from .models import Appointment, Session
from patients.models import Patient

class AppointmentForm(forms.ModelForm):
    recurrence = forms.ChoiceField(
        choices=[('none', 'None'), ('weekly', 'Weekly'), ('monthly', 'Monthly')],
        required=False, 
        initial='none',
        help_text="Repeat until end of current year"
    )

    class Meta:
        model = Appointment
        fields = ['patient', 'date_time', 'status']
        widgets = {
            'date_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
    
    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if user and hasattr(user, 'professional'):
            self.fields['patient'].queryset = Patient.objects.filter(created_by=user.professional)

class SessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ['session_type', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
