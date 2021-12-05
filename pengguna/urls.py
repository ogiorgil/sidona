from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login),
    path("register/", views.register),
    path("profil/", views.read_pengguna),
    path("daftar_pengguna/", views.tabel_daftar_pengguna),
    path("admin_detail_pengguna/", views.admin_pov_read_pengguna),
]
