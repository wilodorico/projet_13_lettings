from django.urls import reverse, resolve
from profiles import views


def test_profiles_index_url_resolves():
    """Test that the profiles index URL resolves to the correct view."""
    url = reverse("profiles:index")
    resolved = resolve(url)

    assert resolved.func == views.index
    assert resolved.url_name == "index"
    assert resolved.namespace == "profiles"


def test_profiles_detail_url_resolves():
    """Test that the profile detail URL resolves to the correct view with username parameter."""
    url = reverse("profiles:profile", args=["johndoe"])
    resolved = resolve(url)

    assert resolved.func == views.profile
    assert resolved.url_name == "profile"
    assert resolved.namespace == "profiles"
    assert resolved.kwargs == {"username": "johndoe"}
