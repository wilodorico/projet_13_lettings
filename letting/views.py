from django.shortcuts import render, get_object_or_404

from letting.models import Letting


def index(request):
    """Display a list of all available lettings.

    Retrieves all Letting objects from the database and renders them
    in a list format on the lettings index page.

    Args:
        request: HTTP request object.

    Returns:
        HttpResponse: Rendered lettings index page with list of all lettings.
    """
    lettings_list = Letting.objects.all()
    context = {"lettings_list": lettings_list}
    return render(request, "letting/index.html", context)


def letting(request, letting_id):
    """Display detailed information for a specific letting.
    
    Retrieves a specific Letting object by ID and displays its details
    including title and associated address information.
    
    Args:
        request: HTTP request object.
        letting_id: ID of the letting to display.
        
    Returns:
        HttpResponse: Rendered letting detail page with title and address.
        
    Raises:
        Http404: If no letting exists with the provided ID.
    """
    letting = get_object_or_404(Letting, id=letting_id)
    context = {
        "title": letting.title,
        "address": letting.address,
    }
    return render(request, "letting/letting.html", context)