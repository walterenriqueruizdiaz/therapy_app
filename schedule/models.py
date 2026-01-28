from django.db import models

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('reserved', 'Reserved'),
        ('confirmed', 'Confirmed'),
        ('no_show', 'No Show'),
        ('cancelled', 'Cancelled'),
    ]

    professional = models.ForeignKey('professionals.Professional', on_delete=models.CASCADE, related_name='appointments')
    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE, related_name='appointments')
    date_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='reserved')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.date_time} - {self.patient}"

class Session(models.Model):
    TYPE_CHOICES = [
        ('evaluation', 'Evaluation'),
        ('intervention', 'Intervention'),
        ('parents_meeting', 'Parents Meeting'),
    ]

    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name='session')
    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE, related_name='sessions')
    date = models.DateField()
    time = models.TimeField()
    session_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    notes = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Session {self.date} {self.session_type} - {self.patient}"
