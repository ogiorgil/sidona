from django.urls import path
from .views import pencairanDana
from django.urls import path

urlpatterns = [
    path('pencairan-dana', pencairanDana, name='pencairan-dana')
]
