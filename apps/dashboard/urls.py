from django.urls import path

from . import views

app_name = "dashboard"

urlpatterns = [
    path("appointments/", views.appointment_dashboard, name="appointments"),
    path("appointments/<int:pk>/update/", views.appointment_update, name="appointment_update"),
]
