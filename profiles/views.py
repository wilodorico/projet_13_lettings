from django.shortcuts import get_object_or_404, render

from profiles.models import Profile


def index(request):
    """Display a list of all user profiles.

    Retrieves all Profile objects from the database and renders them
    in a list format on the profiles index page.

    Args:
        request: HTTP request object.

    Returns:
        HttpResponse: Rendered profiles index page with list of all profiles.
    """
    profiles_list = Profile.objects.all()
    context = {"profiles_list": profiles_list}
    return render(request, "profiles/index.html", context)


def profile(request, username):
    """Display detailed information for a specific user profile.

    Retrieves a specific Profile object by username and displays its details
    including user information and favorite city.

    Args:
        request: HTTP request object.
        username: Username of the profile to display.

    Returns:
        HttpResponse: Rendered profile detail page with user information.

    Raises:
        DoesNotExist: If no profile exists with the provided username.
    """
    profile = get_object_or_404(Profile, user__username=username)
    context = {"profile": profile}
    return render(request, "profiles/profile.html", context)
