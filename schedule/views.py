from django.views.generic import ListView, CreateView, UpdateView, TemplateView, DeleteView
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.contrib import messages
from dateutil.relativedelta import relativedelta
from web.mixins import ProfessionalRequiredMixin
from .models import Appointment, Session
from .forms import AppointmentForm, SessionForm
import datetime

class WeeklyScheduleView(ProfessionalRequiredMixin, TemplateView):
    template_name = 'schedule/weekly_schedule.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not hasattr(self.request.user, 'professional'): return context

        week_start_str = self.request.GET.get('week_start')
        if week_start_str:
            try:
                today = datetime.datetime.strptime(week_start_str, '%Y-%m-%d').date()
            except ValueError:
                today = timezone.localdate()
        else:
            today = timezone.localdate()
        
        # Calculate start of week (Monday)
        start_week = today - datetime.timedelta(days=today.weekday())
        end_week = start_week + datetime.timedelta(days=6)
        
        context['start_week'] = start_week
        context['end_week'] = end_week
        context['prev_week'] = (start_week - datetime.timedelta(days=7)).strftime('%Y-%m-%d')
        context['next_week'] = (start_week + datetime.timedelta(days=7)).strftime('%Y-%m-%d')
        
        appointments = Appointment.objects.filter(
            professional=self.request.user.professional,
            date_time__date__range=[start_week, end_week]
        ).order_by('date_time')
        
        context['appointments'] = appointments
        return context

class AppointmentCreateView(ProfessionalRequiredMixin, CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'schedule/appointment_form.html'
    success_url = reverse_lazy('schedule')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        professional = self.request.user.professional
        form.instance.professional = professional
        response = super().form_valid(form)
        
        # Handle Recurrence
        recurrence = form.cleaned_data.get('recurrence')
        if recurrence in ['weekly', 'monthly']:
            initial_date = form.instance.date_time
            current_year = initial_date.year
            # Use fixed year end logic
            end_of_year = initial_date.replace(year=current_year, month=12, day=31, hour=23, minute=59)
            
            next_date = initial_date
            
            # Prevent infinite loops
            max_count = 60
            count = 0
            
            while count < max_count:
                if recurrence == 'weekly':
                    next_date = next_date + datetime.timedelta(days=7)
                elif recurrence == 'monthly':
                    next_date = next_date + relativedelta(months=1)
                
                if next_date.year > current_year:
                    break
                
                Appointment.objects.create(
                    professional=professional,
                    patient=form.instance.patient,
                    date_time=next_date,
                    status=form.instance.status # Copy status e.g. reserved
                )
                count += 1
                
        return response

class SessionListView(ProfessionalRequiredMixin, ListView):
    model = Session
    template_name = 'schedule/session_list.html'
    context_object_name = 'sessions'

    def get_queryset(self):
        if not hasattr(self.request.user, 'professional'): return Session.objects.none()
        return Session.objects.filter(
            appointment__professional=self.request.user.professional
        ).order_by('-date', '-time')

class SessionCreateView(ProfessionalRequiredMixin, CreateView):
    model = Session
    form_class = SessionForm
    template_name = 'schedule/session_form.html'
    success_url = reverse_lazy('session_list')

    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request.user, 'professional'): return self.handle_no_permission()
        self.appointment = get_object_or_404(
            Appointment, 
            pk=kwargs['appointment_id'], 
            professional=request.user.professional
        )
        if hasattr(self.appointment, 'session'):
            return redirect('session_list')
        
        # Validate that session can only be created on appointment day at or after appointment time
        now = timezone.now()
        appointment_datetime = self.appointment.date_time
        
        # Check if it's the appointment day
        if now.date() != appointment_datetime.date():
            messages.error(request, 'Solo se puede crear una sesión el mismo día de la cita.')
            return redirect('session_list')
        
        # Check if current time is at or after appointment time
        if now.time() < appointment_datetime.time():
            messages.error(request, 'Solo se puede crear una sesión a partir de la hora de inicio de la cita.')
            return redirect('session_list')
        
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.appointment = self.appointment
        form.instance.patient = self.appointment.patient
        form.instance.date = self.appointment.date_time.date()
        form.instance.time = self.appointment.date_time.time()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['appointment'] = self.appointment
        return context

class SessionUpdateView(ProfessionalRequiredMixin, UpdateView):
    model = Session
    form_class = SessionForm
    template_name = 'schedule/session_edit.html'
    success_url = reverse_lazy('session_list')

    def get_queryset(self):
        if not hasattr(self.request.user, 'professional'): 
            return Session.objects.none()
        return Session.objects.filter(
            appointment__professional=self.request.user.professional
        )

class AppointmentDeleteView(ProfessionalRequiredMixin, DeleteView):
    model = Appointment
    template_name = 'schedule/appointment_confirm_delete.html'
    success_url = reverse_lazy('schedule')

    def get_queryset(self):
        if not hasattr(self.request.user, 'professional'):
            return Appointment.objects.none()
        return Appointment.objects.filter(professional=self.request.user.professional)

