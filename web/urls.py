from django.contrib import admin
from django.urls import path, include
from .views import DashboardView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', DashboardView.as_view(), name='dashboard'),
    path('patients/', include('patients.urls')),
    path('schedule/', include('schedule.urls')),
    # Professionals app URLs might be needed for profile setup, e.g. /profile/setup/
    path('profile/', include('professionals.urls')),
]
