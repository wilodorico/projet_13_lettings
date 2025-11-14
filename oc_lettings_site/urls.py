from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("profiles/", include("profiles.urls")),
    path("letting/", include("letting.urls")),
    path("admin/", admin.site.urls),
]
