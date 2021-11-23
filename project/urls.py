from django.urls import path, include
from django.contrib import admin
import trigger_3.urls as t3


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(t3)),
]
