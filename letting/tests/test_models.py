import pytest

from letting.models import Address, Letting


@pytest.mark.django_db
def test_address_str():
    address = Address(
        number=10, street="Place de la victoire", city="Bordeaux", state="FR", zip_code=33000, country_iso_code="FRA"
    )
    assert str(address) == "10 Place de la victoire"


@pytest.mark.django_db
def test_letting_str():
    address = Address(
        number=12, street="Rue de la Paix", city="Lyon", state="FR", zip_code=69001, country_iso_code="FRA"
    )
    letting = Letting(title="Charming Flat", address=address)
    assert str(letting) == "Charming Flat"


@pytest.mark.django_db
def test_letting_address_relation():
    address = Address(
        number=5, street="Rue Victor Hugo", city="Marseille", state="FR", zip_code=13000, country_iso_code="FRA"
    )
    letting = Letting(title="Sunny Apartment", address=address)
    assert letting.address == address
