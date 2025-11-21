from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    """Model representing a user profile with additional information.

    This model extends the Django User model with additional profile
    information. Each profile has a one-to-one relationship with a User
    and stores optional preferences like favorite city.

    Attributes:
        user: One-to-one relationship with Django User model.
        favorite_city: Optional favorite city (max 64 characters, can be blank).
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorite_city = models.CharField(max_length=64, blank=True)

    class Meta:
        db_table = "profiles_profile"
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    def __str__(self):
        """Return string representation of the profile.

        Returns:
            str: The username of the associated user.
        """
        return self.user.username
