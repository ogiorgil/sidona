from django.urls import path
from . import views

urlpatterns = [
    path("", views.daftar_penggalangan_pengguna_pov, name="index"),
]