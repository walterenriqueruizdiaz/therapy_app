from django.views.generic import TemplateView
from django.utils import timezone
from django.db.models import Count, Q
from schedule.models import Appointment, Session
from .mixins import ProfessionalRequiredMixin

class DashboardView(ProfessionalRequiredMixin, TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # If the mixin redirects, this code is not reached, essentially.
        # But we need to be careful if mixin logic uses 'dispatch'.
        # Assuming dispatch handles the check.
        if not hasattr(self.request.user, 'professional'):
            return context # Should have redirected already

        professional = self.request.user.professional
        today = timezone.localdate()
        
        # Today's appointments
        context['today_appointments'] = Appointment.objects.filter(
            professional=professional,
            date_time__date=today
        ).order_by('date_time')[:10] 

        # Week summary
        start_week = today - timezone.timedelta(days=today.weekday())
        end_week = start_week + timezone.timedelta(days=6)

        week_appointments = Appointment.objects.filter(
            professional=professional,
            date_time__date__range=[start_week, end_week]
        )

        stats = week_appointments.aggregate(
            total=Count('id'),
            cancelled=Count('id', filter=Q(status='cancelled')),
            no_show=Count('id', filter=Q(status='no_show')),
        )
        
        stats['completed_sessions'] = Session.objects.filter(
            appointment__in=week_appointments
        ).count()

        context['week_stats'] = stats
        return context
