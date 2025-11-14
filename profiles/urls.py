from django.urls import path

from profiles import views

app_name = "profiles"

urlpatterns = [
    path("", views.profiles_index, name="profiles_index"),
    path("<str:username>/", views.profile, name="profile"),
]
