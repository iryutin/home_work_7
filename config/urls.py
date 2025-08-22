from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("materials.urls", namespace="materials")),
    path("user/", include("user.urls", namespace="user")),
    path("", include("docs")),
]
