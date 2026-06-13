from django.urls import path

from . import views

app_name = "hospital"

urlpatterns = [
    path("departments/", views.departments, name="departments"),
    path("departments/<slug:slug>/", views.department_detail, name="department_detail"),
    path("doctors/", views.doctors, name="doctors"),
    path("opd-timing/", views.opd_timing, name="opd_timing"),
    path("services/", views.services, name="services"),
    path("facilities/", views.facilities, name="facilities"),
    path("emergency/", views.emergency, name="emergency"),
    path("ambulance/", views.ambulance, name="ambulance"),
    path("gallery/", views.gallery, name="gallery"),
    path("contact/", views.contact, name="contact"),
    path("updates/", views.updates, name="updates"),
    path("updates/<slug:slug>/", views.update_detail, name="update_detail"),
]
