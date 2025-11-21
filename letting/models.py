from django.core.validators import MaxValueValidator, MinLengthValidator
from django.db import models


class Address(models.Model):
    """Model representing a physical address.

    This model stores address information including street number, street name,
    city, state, zip code, and country code. It includes validation for proper
    formatting and value ranges.

    Attributes:
        number: Street number (max 9999).
        street: Street name (max 64 characters).
        city: City name (max 64 characters).
        state: State/province code (exactly 2 characters).
        zip_code: Postal/ZIP code (max 99999).
        country_iso_code: ISO country code (exactly 3 characters).
    """

    number = models.PositiveIntegerField(validators=[MaxValueValidator(9999)])
    street = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    state = models.CharField(max_length=2, validators=[MinLengthValidator(2)])
    zip_code = models.PositiveIntegerField(validators=[MaxValueValidator(99999)])
    country_iso_code = models.CharField(max_length=3, validators=[MinLengthValidator(3)])

    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Addresses"

    def __str__(self):
        """Return string representation of the address.

        Returns:
            str: Address formatted as "number street".
        """
        return f"{self.number} {self.street}"


class Letting(models.Model):
    """Model representing a property letting/rental.

    This model represents a rental property with a title and associated address.
    Each letting has a one-to-one relationship with an Address.

    Attributes:
        title: Descriptive title for the letting (max 256 characters).
        address: One-to-one relationship with Address model.
    """

    title = models.CharField(max_length=256)
    address = models.OneToOneField(Address, on_delete=models.CASCADE)

    def __str__(self):
        """Return string representation of the letting.

        Returns:
            str: The title of the letting.
        """
        return self.title
