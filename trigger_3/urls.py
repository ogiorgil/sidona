from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path(
        "daftar-penggalangan/",
        views.daftar_penggalangan_pengguna_pov,
        name="daftar-penggalangan-pengguna",
    ),
    path(
        "daftar-penggalangan-admin/",
        views.daftar_penggalangan_admin_pov,
        name="daftar-penggalangan-admin",
    ),
    path(
        "update-penggalangan/",
        views.form_update_penggalangan,
        name="update-penggalangan",
    ),
    path(
        "verifikasi-penggalangan/",
        views.form_verifikasi_penggalangan,
        name="verifikasi-penggalangan",
    ),
    path(
        "detail-penggalangan/",
        views.detail_penggalangan,
        name="detail-penggalangan",
    ),
    path(
        "create-kategori/",
        views.form_create_kategori,
        name="create-kategori-admin",
    ),
    path(
        "update-kategori/",
        views.form_update_kategori,
        name="update-kategori-admin",
    ),
    path(
        "kategori-penggalangan-admin/",
        views.kategori_penggalangan,
        name="kategori-penggalangan-admin",
    ),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)