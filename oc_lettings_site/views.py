import logging

from django.shortcuts import render

logger = logging.getLogger(__name__)


def index(request):
    """Display the main homepage.

    Renders the homepage template that serves as the entry point
    to the Holiday Homes application, providing navigation to
    lettings and profiles sections.

    Args:
        request: HTTP request object.

    Returns:
        HttpResponse: Rendered homepage template.
    """
    try:
        logger.info("Homepage accessed")
        return render(request, "index.html")
    except Exception as e:
        logger.error(f"Error rendering homepage: {str(e)}", exc_info=True)
        raise
