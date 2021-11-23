from django.urls import path, include
from django.contrib import admin

# import trigger_1.urls as t1
# import trigger_2.urls as t2
import trigger_3.urls as t3

# import trigger_4.urls as t4

# import trigger_5.urls as t5


urlpatterns = [
    path("admin/", admin.site.urls),
    path("t3/", include(t3)),
    # path("t4/", include(t4)),
]
