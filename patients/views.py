from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404
from django.db.models import Q
from web.mixins import ProfessionalRequiredMixin
from .models import Patient, FamilyContact
from .forms import PatientForm, FamilyContactForm

class PatientListView(ProfessionalRequiredMixin, ListView):
    model = Patient
    template_name = 'patients/patient_list.html'
    context_object_name = 'patients'

    def get_queryset(self):
        # Ensure user has professional profile (handled by mixin largely, but double check in query)
        if not hasattr(self.request.user, 'professional'):
            return Patient.objects.none()
            
        professional = self.request.user.professional
        qs = Patient.objects.filter(created_by=professional)
        
        query = self.request.GET.get('q')
        if query:
            qs = qs.filter(
                Q(first_name__icontains=query) | 
                Q(last_name__icontains=query) | 
                Q(dni__icontains=query)
            )
        return qs

class PatientCreateView(ProfessionalRequiredMixin, CreateView):
    model = Patient
    form_class = PatientForm
    template_name = 'patients/patient_form.html'
    success_url = reverse_lazy('patient_list') 

    def form_valid(self, form):
        form.instance.created_by = self.request.user.professional
        return super().form_valid(form)

class PatientDetailView(ProfessionalRequiredMixin, DetailView):
    model = Patient
    template_name = 'patients/patient_detail.html'

    def get_queryset(self):
         if not hasattr(self.request.user, 'professional'):
             return Patient.objects.none()
         return Patient.objects.filter(created_by=self.request.user.professional)

class PatientUpdateView(ProfessionalRequiredMixin, UpdateView):
    model = Patient
    form_class = PatientForm
    template_name = 'patients/patient_form.html'

    def get_queryset(self):
         if not hasattr(self.request.user, 'professional'):
             return Patient.objects.none()
         return Patient.objects.filter(created_by=self.request.user.professional)
    
    def get_success_url(self):
        return reverse('patient_detail', kwargs={'pk': self.object.pk})

class FamilyContactCreateView(ProfessionalRequiredMixin, CreateView):
    model = FamilyContact
    form_class = FamilyContactForm
    template_name = 'patients/contact_form.html'

    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request.user, 'professional'):
             return self.handle_no_permission()
        self.patient = get_object_or_404(Patient, pk=kwargs['patient_id'], created_by=request.user.professional)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.patient = self.patient
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('patient_detail', kwargs={'pk': self.patient.pk})

class FamilyContactUpdateView(ProfessionalRequiredMixin, UpdateView):
    model = FamilyContact
    form_class = FamilyContactForm
    template_name = 'patients/contact_form.html'

    def get_queryset(self):
        if not hasattr(self.request.user, 'professional'): return FamilyContact.objects.none()
        return FamilyContact.objects.filter(patient__created_by=self.request.user.professional)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['patient'] = self.object.patient
        return context

    def get_success_url(self):
        return reverse('patient_detail', kwargs={'pk': self.object.patient.pk})

class FamilyContactDeleteView(ProfessionalRequiredMixin, DeleteView):
    model = FamilyContact
    template_name = 'patients/contact_confirm_delete.html'

    def get_queryset(self):
        if not hasattr(self.request.user, 'professional'): return FamilyContact.objects.none()
        return FamilyContact.objects.filter(patient__created_by=self.request.user.professional)

    def get_success_url(self):
        return reverse('patient_detail', kwargs={'pk': self.object.patient.pk})
