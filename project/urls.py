from django.urls import path, include
from django.contrib import admin

import penggalangan_dana.urls as pd
import komorbid.urls as komorbid
import pengguna.urls as pengguna
import trigger_3.urls as t3
import trigger_4.urls as t4


urlpatterns = [
    path("pd/", include(pd)),
    path("t3/", include(t3)),
    path("t4/", include(t4)),
    path("admin/", admin.site.urls),
    path("komorbid/", include(komorbid)),
    path("auth/", include(pengguna)),
]
