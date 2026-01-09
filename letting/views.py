import logging

from django.shortcuts import get_object_or_404, render

from letting.models import Letting

logger = logging.getLogger(__name__)


def index(request):
    """Display a list of all available lettings.

    Retrieves all Letting objects from the database and renders them
    in a list format on the lettings index page.

    Args:
        request: HTTP request object.

    Returns:
        HttpResponse: Rendered lettings index page with list of all lettings.
    """
    try:
        logger.info("Lettings index page accessed")
        lettings_list = Letting.objects.all()
        logger.debug(f"Retrieved {lettings_list.count()} lettings")
        context = {"lettings_list": lettings_list}
        return render(request, "letting/index.html", context)
    except Exception as e:
        logger.error(f"Error retrieving lettings list: {str(e)}", exc_info=True)
        raise


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
    try:
        logger.info(f"Accessing letting detail for ID: {letting_id}")
        letting = get_object_or_404(Letting, id=letting_id)
        logger.debug(f"Retrieved letting: {letting.title}")
        context = {
            "title": letting.title,
            "address": letting.address,
        }
        return render(request, "letting/letting.html", context)
    except Exception as e:
        logger.error(
            f"Error retrieving letting {letting_id}: {str(e)}", exc_info=True, extra={"letting_id": letting_id}
        )
        raise
