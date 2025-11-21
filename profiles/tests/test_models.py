import pytest
from django.contrib.auth.models import User
from profiles.models import Profile


@pytest.mark.django_db
def test_profile_creation():
    """Profile should be created with valid user and optional favorite city."""
    user = User.objects.create(username="johndoe")
    profile = Profile.objects.create(user=user, favorite_city="Paris")

    assert profile.user.username == "johndoe"
    assert profile.favorite_city == "Paris"


@pytest.mark.django_db
def test_profile_str():
    """__str__ should return the associated user's username."""
    user = User.objects.create(username="janedoe")
    profile = Profile.objects.create(user=user)

    assert str(profile) == "janedoe"

@pytest.mark.django_db
def test_profile_favorite_city_can_be_blank():
    """favorite_city should allow blank values."""
    user = User.objects.create(username="bob")
    profile = Profile.objects.create(user=user, favorite_city="")

    assert profile.favorite_city == ""


@pytest.mark.django_db
def test_profile_user_one_to_one_relation():
    """Profile should be linked to a User via OneToOneField."""
    user = User.objects.create(username="alice")
    profile = Profile.objects.create(user=user)

    assert profile.user == user
    assert user.profile == profile # Reverse relation


@pytest.mark.django_db
def test_profile_deletion_on_user_delete():
    """Deleting the User should delete the linked Profile (cascade)."""
    user = User.objects.create(username="mark")
    Profile.objects.create(user=user)

    user.delete()

    assert Profile.objects.count() == 0
