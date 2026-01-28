from django.urls import path
from .views import (
    PatientListView, PatientCreateView, PatientDetailView, 
    PatientUpdateView, FamilyContactCreateView, 
    FamilyContactUpdateView, FamilyContactDeleteView
)

urlpatterns = [
    path('', PatientListView.as_view(), name='patient_list'),
    path('new/', PatientCreateView.as_view(), name='patient_create'),
    path('<int:pk>/', PatientDetailView.as_view(), name='patient_detail'),
    path('<int:pk>/edit/', PatientUpdateView.as_view(), name='patient_update'),
    path('<int:patient_id>/contact/new/', FamilyContactCreateView.as_view(), name='contact_create'),
    path('contact/<int:pk>/edit/', FamilyContactUpdateView.as_view(), name='contact_update'),
    path('contact/<int:pk>/delete/', FamilyContactDeleteView.as_view(), name='contact_delete'),
]
