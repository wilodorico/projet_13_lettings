import pytest
from pytest_django.asserts import assertTemplateUsed

from django.urls import reverse

from profiles.models import Profile


@pytest.fixture
def alice_profile(django_user_model):
    """Fixture to create a user and associated profile for testing."""
    user = django_user_model.objects.create(first_name="Alice", last_name="Doe", email="alice@example.com", username="alicedoe")
    profile = Profile.objects.create(user=user, favorite_city="Paris")
    return profile

@pytest.fixture
def bob_profile(django_user_model):
    """Fixture to create another user and associated profile for testing."""
    user = django_user_model.objects.create(first_name="Bob", last_name="Smith", email="bob@example.com", username="bobsmith")
    profile = Profile.objects.create(user=user, favorite_city="New York")
    return profile

@pytest.mark.django_db
def test_profiles_index_view(client, alice_profile, bob_profile):
    """The index view should display a list of all profiles."""
    
    url = reverse("profiles:index")
    response = client.get(url)
    
    assert response.status_code == 200
    assert "profiles_list" in response.context
    assert len(response.context["profiles_list"]) == 2
    assert alice_profile in response.context["profiles_list"]
    assert bob_profile in response.context["profiles_list"]
    assertTemplateUsed(response, "profiles/index.html")
    
    
@pytest.mark.django_db
def test_profiles_detail_view(client, alice_profile):
    """The profile detail view should display the correct profile information."""
    
    url = reverse("profiles:profile", args=[alice_profile.user.username])
    response = client.get(url)
    
    assert response.status_code == 200
    assert response.context["profile"] == alice_profile
    assert response.context["profile"].user.first_name == "Alice"
    assert response.context["profile"].user.last_name == "Doe"
    assert response.context["profile"].user.email == "alice@example.com"
    assert response.context["profile"].favorite_city == "Paris"
    assertTemplateUsed(response, "profiles/profile.html")
    
    
@pytest.mark.django_db
def test_profiles_detail_view_404_not_found(client):
    """The profile detail view should return 404 for non-existent username."""
    
    url = reverse("profiles:profile", args=["nonexistentuser"])
    response = client.get(url)
    
    assert response.status_code == 404