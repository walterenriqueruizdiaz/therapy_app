from django.urls import path
from .views import ProfessionalCreateView

urlpatterns = [
    path('setup/', ProfessionalCreateView.as_view(), name='professional_create'),
]
