from django.test import TestCase
from django.contrib.auth.models import User
from professionals.models import Professional
from patients.models import Patient, FamilyContact
from .models import Appointment
from django.utils import timezone
import datetime

class RecurrenceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='password')
        self.professional = Professional.objects.create(
            user=self.user, dni='123', first_name='Test', last_name='Prof', professional_license_number='A1'
        )
        self.patient = Patient.objects.create(
            created_by=self.professional, dni='P1', first_name='Patient', last_name='One', 
            birth_date=datetime.date(2000, 1, 1), mobile_phone='123'
        )

    def test_weekly_recurrence(self):
        self.client.login(username='test', password='password')
        start_date = timezone.now().replace(month=1, day=1, hour=10, minute=0, second=0)
        
        response = self.client.post('/schedule/appointments/new/', {
            'patient': self.patient.id,
            'date_time': start_date.strftime('%Y-%m-%dT%H:%M'),
            'status': 'reserved',
            'recurrence': 'weekly'
        })
        self.assertEqual(response.status_code, 302)
        count = Appointment.objects.count()
        self.assertTrue(count >= 52)

    def test_monthly_recurrence(self):
        self.client.login(username='test', password='password')
        start_date = timezone.now().replace(month=1, day=1, hour=10, minute=0, second=0)
        
        response = self.client.post('/schedule/appointments/new/', {
            'patient': self.patient.id,
            'date_time': start_date.strftime('%Y-%m-%dT%H:%M'),
            'status': 'reserved',
            'recurrence': 'monthly'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Appointment.objects.count(), 12)

class ContactTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='password')
        self.professional = Professional.objects.create(
            user=self.user, dni='123', first_name='Test', last_name='Prof', professional_license_number='A1'
        )
        self.patient = Patient.objects.create(
            created_by=self.professional, dni='P1', first_name='Patient', last_name='One', 
            birth_date=datetime.date(2000, 1, 1), mobile_phone='123'
        )

    def test_create_contact(self):
        self.client.login(username='test', password='password')
        response = self.client.post(f'/patients/{self.patient.id}/contact/new/', {
            'first_name': 'Mom',
            'last_name': 'One',
            'relationship_to_patient': 'Mother',
            'mobile_phone': '999',
            'email': 'mom@example.com'
        })
        self.assertRedirects(response, f'/patients/{self.patient.id}/')
        
        contact = FamilyContact.objects.first()
        self.assertIsNotNone(contact)
        self.assertEqual(contact.relationship_to_patient, 'Mother')
        self.assertEqual(contact.patient, self.patient)

    def test_update_contact(self):
        contact = FamilyContact.objects.create(
            patient=self.patient, first_name='Dad', last_name='One', 
            relationship_to_patient='Father', mobile_phone='888'
        )
        self.client.login(username='test', password='password')
        response = self.client.post(f'/patients/contact/{contact.id}/edit/', {
            'first_name': 'Dad',
            'last_name': 'Updated',
            'relationship_to_patient': 'Father',
            'mobile_phone': '888',
            'email': 'dad@example.com'
        })
        self.assertRedirects(response, f'/patients/{self.patient.id}/')
        
        contact.refresh_from_db()
        self.assertEqual(contact.last_name, 'Updated')

    def test_delete_contact(self):
        contact = FamilyContact.objects.create(
            patient=self.patient, first_name='Bro', last_name='One', 
            relationship_to_patient='Brother', mobile_phone='777'
        )
        self.client.login(username='test', password='password')
        response = self.client.post(f'/patients/contact/{contact.id}/delete/')
        self.assertRedirects(response, f'/patients/{self.patient.id}/')
        
        self.assertEqual(FamilyContact.objects.count(), 0)
