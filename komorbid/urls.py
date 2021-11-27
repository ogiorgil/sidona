from django.urls import path
from . import views

urlpatterns = [
    path("", views.read_komorbid, name="read"),
    path("create/", views.create_komorbid, name="create"),
    path("update/", views.update_komorbid, name="update"),
]
