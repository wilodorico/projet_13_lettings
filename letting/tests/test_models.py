import pytest

from letting.models import Address, Letting


@pytest.fixture
def sample_address():
    return Address(
        number=10, street="Place de la victoire", city="Bordeaux", state="FR", zip_code=33000, country_iso_code="FRA"
    )


@pytest.mark.django_db
def test_address_str(sample_address):
    address = sample_address

    assert str(address) == "10 Place de la victoire"


@pytest.mark.django_db
def test_letting_str(sample_address):
    letting = Letting(title="Charming Flat", address=sample_address)
    assert str(letting) == "Charming Flat"


@pytest.mark.django_db
def test_letting_address_relation(sample_address):
    address = sample_address
    letting = Letting(title="Sunny Apartment", address=address)
    assert letting.address == address
