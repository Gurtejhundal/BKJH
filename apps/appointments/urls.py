from django.urls import path

from . import views

app_name = "appointments"

urlpatterns = [
    path("appointment/", views.appointment_request, name="appointment"),
]
