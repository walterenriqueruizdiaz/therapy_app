from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse

class ProfessionalRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        # User is authenticated but maybe check for Professional existence?
        # Ideally, we let them view pages, but if they lack a profile, we redirect.
        # But 'test_func' is for 403.
        # So instead of 'UserPassesTest', we might want a dispatch override.
        return super().handle_no_permission()

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        
        # Check if user has a professional profile
        if not hasattr(request.user, 'professional'):
            # Allow access to profile setup page to avoid infinite loop
            if request.resolver_match.url_name == 'professional_create':
                return super().dispatch(request, *args, **kwargs)
            return redirect('professional_create')
            
        return super().dispatch(request, *args, **kwargs)
