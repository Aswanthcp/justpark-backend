from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin_/", admin.site.urls),
    path("api/", include("api.urls")),
    path("admin/", include("admin.urls")),
    path("support/", include("support.urls")),
]
