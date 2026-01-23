"""Tests for main site views."""

import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_index_view(client):
    """Test that the homepage loads successfully."""
    url = reverse("index")
    response = client.get(url)

    assert response.status_code == 200
    assert "index.html" in [t.name for t in response.templates]


@pytest.mark.django_db
def test_index_view_content(client):
    """Test that the homepage contains expected content."""
    url = reverse("index")
    response = client.get(url)

    assert response.status_code == 200
    content = response.content.decode()
    assert "Holiday Homes" in content or "Welcome" in content
