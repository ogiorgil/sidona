from django.urls import path
from . import views
from django.conf import settings

urlpatterns = [
    path(
        "data-donasi/",
        views.data_donasi,
        name="data-donasi",
    ),
    path(
        "detail-penggalangan/",
        views.detail_penggalangan_pengguna_pov,
        name="detail-penggalangan-pengguna",
    ),
    path(
        "detail-donasi/",
        views.detail_donasi_pengguna_pov,
        name="detail-donasi-pengguna",
    ),
    path(
        "create-donasi/",
        views.form_create_donasi,
        name="create-donasi-pengguna",
    ),
    path(
        "profil-pengguna/",
        views.profil_pengguna,
        name="profil-pengguna",
    ),
    path(
        "daftar-penggalangan/",
        views.daftar_penggalangan_pengguna_pov,
        name="daftar-penggalangan-pengguna",
    ),
    path(
        "add-wishlist/",
        views.tambah_wishlist,
        name="add-wishlist"
    ),
    path(
        "delete-wishlist/",
        views.delete_wishlist,
        name="delete-wishlist"
    )

]