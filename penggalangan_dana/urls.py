from django.urls import path
from . import views

urlpatterns = [
    path("", views.read_pd, name="read"),
    path("create/", views.create_pd, name="create"),
    path("details/", views.read_pd_details, name="read_details"),
]
