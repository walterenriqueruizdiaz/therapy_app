from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Professional
from .forms import ProfessionalForm

class ProfessionalCreateView(LoginRequiredMixin, CreateView):
    model = Professional
    form_class = ProfessionalForm
    template_name = 'professionals/professional_form.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
