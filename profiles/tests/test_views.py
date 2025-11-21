import pytest
from pytest_django.asserts import assertTemplateUsed

from django.contrib.auth.models import User
from django.urls import reverse

from profiles.models import Profile

@pytest.mark.django_db
def test_profiles_index_view(client):
    """The index view should display a list of all profiles."""
    alice = User.objects.create(username="alice")
    bob = User.objects.create(username="bob")
    Profile.objects.create(user=alice)
    Profile.objects.create(user=bob)
    
    url = reverse("profiles:index")
    response = client.get(url)
    
    assert response.status_code == 200
    assert "profiles_list" in response.context
    assert len(response.context["profiles_list"]) == 2
    assert alice.profile in response.context["profiles_list"]
    assert bob.profile in response.context["profiles_list"]
    assertTemplateUsed(response, "profiles/index.html")
    