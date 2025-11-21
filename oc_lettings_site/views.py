from django.shortcuts import render


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
    return render(request, "index.html")
