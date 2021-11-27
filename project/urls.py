from django.urls import path, include
from django.contrib import admin

import penggalangan_dana.urls as pd
import komorbid.urls as komorbid

# import trigger_1.urls as t1
# import trigger_2.urls as t2
import trigger_3.urls as t3
import trigger_4.urls as t4

# import trigger_4.urls as t4
# import trigger_5.urls as t5


urlpatterns = [
    path("admin/", admin.site.urls),
    path("pd/", include(pd)),
    path("komorbid/", include(komorbid)),
    path("", include(t3)),
    path("t3/", include(t3)),
     path("t4/", include(t4)),
    # path("t4/", include(t4)),
]
