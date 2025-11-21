import pytest
from django.urls import reverse
from letting.models import Address, Letting


@pytest.fixture
def sample_address():
    """Create a sample address for testing."""
    return Address.objects.create(
        number=1,
        street="Rue Alfred Nobel",
        city="Paris",
        state="FR",
        zip_code=75001,
        country_iso_code="FRA"
    )


@pytest.fixture
def sample_letting(sample_address):
    """Create a sample letting for testing."""
    return Letting.objects.create(
        title="Test flat",
        address=sample_address
    )


@pytest.mark.django_db
def test_index_view(client, sample_letting):
    """Test the lettings index view displays the lettings list correctly."""
    url = reverse("letting:index")
    response = client.get(url)

    assert response.status_code == 200
    assert "lettings_list" in response.context
    assert sample_letting in response.context["lettings_list"]
    assert "letting/index.html" in [t.name for t in response.templates]
    
    
@pytest.mark.django_db
def test_letting_detail_view(client, sample_letting):
    """Test the letting detail view displays the letting information correctly."""
    url = reverse("letting:letting", args=[sample_letting.id])
    response = client.get(url)

    assert response.status_code == 200
    assert response.context["title"] == sample_letting.title
    assert response.context["address"] == sample_letting.address
    assert "letting/letting.html" in [t.name for t in response.templates]
    