from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("bibi-kaulan-ji-hospital/", views.bibi_kaulan_hospital, name="bibi_kaulan_hospital"),
    path("miri-piri-mission-hospital/", views.miri_piri_hospital, name="miri_piri_hospital"),
    path("about/", views.about, name="about"),
    path("privacy/", views.privacy, name="privacy"),
    path("terms/", views.terms, name="terms"),
    path("robots.txt", views.robots_txt, name="robots_txt"),
]
