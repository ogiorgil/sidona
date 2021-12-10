from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login),
    path("logout/", views.logout),
    path("register/", views.register),
    path("profil/", views.read_pengguna),
    path("daftar-pengguna/", views.tabel_daftar_pengguna),
    path("admin-detail-pengguna/", views.admin_pov_read_pengguna),
    path("verifikasi-pengguna/", views.verifikasi_pengguna),
]
