import pytest

from profiles.models import Profile


@pytest.mark.django_db
def test_profile_creation(django_user_model):
    """Profile should be created with valid user and optional favorite city."""
    user = django_user_model.objects.create(username="johndoe")
    profile = Profile.objects.create(user=user, favorite_city="Paris")

    assert profile.user.username == "johndoe"
    assert profile.favorite_city == "Paris"


@pytest.mark.django_db
def test_profile_str(django_user_model):
    """__str__ should return the associated user's username."""
    user = django_user_model.objects.create(username="janedoe")
    profile = Profile.objects.create(user=user)

    assert str(profile) == "janedoe"


@pytest.mark.django_db
def test_profile_favorite_city_can_be_blank(django_user_model):
    """favorite_city should allow blank values."""
    user = django_user_model.objects.create(username="bob")
    profile = Profile.objects.create(user=user, favorite_city="")

    assert profile.favorite_city == ""


@pytest.mark.django_db
def test_profile_user_one_to_one_relation(django_user_model):
    """Profile should be linked to a User via OneToOneField."""
    user = django_user_model.objects.create(username="alice")
    profile = Profile.objects.create(user=user)

    assert profile.user == user
    assert user.profile == profile  # Reverse relation


@pytest.mark.django_db
def test_profile_deletion_on_user_delete(django_user_model):
    """Deleting the User should delete the linked Profile (cascade)."""
    user = django_user_model.objects.create(username="mark")
    Profile.objects.create(user=user)

    user.delete()

    assert Profile.objects.count() == 0
