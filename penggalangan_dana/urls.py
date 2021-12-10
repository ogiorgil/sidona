from django.urls import path
from . import views

urlpatterns = [
    path("", views.read_pd, name="read"),
    path("create/", views.create_pd, name="create"),
    path("details/", views.read_pd_details, name="read_details"),
    path("delete/", views.delete_pd, name="delete"),

    path("kategori/", views.get_kategori, name="get_kategori"),
    path("generate-id/", views.generate_id, name="generate_id"),

    path("add-pasien/", views.create_pasien, name="create_pasien"),
]
