from django.urls import path
from .views import (
    WeeklyScheduleView, AppointmentCreateView, AppointmentDeleteView,
    SessionListView, SessionCreateView, SessionUpdateView
)

urlpatterns = [
    path('', WeeklyScheduleView.as_view(), name='schedule'),
    path('appointments/new/', AppointmentCreateView.as_view(), name='appointment_create'),
    path('appointments/<int:pk>/delete/', AppointmentDeleteView.as_view(), name='appointment_delete'),
    path('sessions/', SessionListView.as_view(), name='session_list'),
    path('appointments/<int:appointment_id>/session/new/', SessionCreateView.as_view(), name='session_create'),
    path('sessions/<int:pk>/edit/', SessionUpdateView.as_view(), name='session_edit'),
]
