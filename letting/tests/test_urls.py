from django.urls import resolve, reverse

from letting import views


def test_index_url_resolves():
    """Test that the letting index URL resolves to the correct view."""
    url = reverse("letting:index")
    resolved = resolve(url)

    assert resolved.func == views.index
    assert resolved.url_name == "index"
    assert resolved.namespace == "letting"


def test_letting_detail_url_resolves():
    """Test that the letting detail URL resolves to the correct view."""
    url = reverse("letting:letting", args=[1])
    resolved = resolve(url)

    assert resolved.func == views.letting
    assert resolved.url_name == "letting"
    assert resolved.namespace == "letting"
    assert resolved.kwargs == {"letting_id": 1}
    assert resolved.kwargs == {"letting_id": 1}
