import logging

from django.shortcuts import get_object_or_404, render

from profiles.models import Profile

logger = logging.getLogger(__name__)


def index(request):
    """Display a list of all user profiles.

    Retrieves all Profile objects from the database and renders them
    in a list format on the profiles index page.

    Args:
        request: HTTP request object.

    Returns:
        HttpResponse: Rendered profiles index page with list of all profiles.
    """
    try:
        logger.info("Profiles index page accessed")
        profiles_list = Profile.objects.all()
        logger.debug(f"Retrieved {profiles_list.count()} profiles")
        context = {"profiles_list": profiles_list}
        return render(request, "profiles/index.html", context)
    except Exception as e:
        logger.error(f"Error retrieving profiles list: {str(e)}", exc_info=True)
        raise


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
    try:
        logger.info(f"Accessing profile for username: {username}")
        profile = get_object_or_404(Profile, user__username=username)
        logger.debug(f"Retrieved profile for user: {username}")
        context = {"profile": profile}
        return render(request, "profiles/profile.html", context)
    except Exception as e:
        logger.error(
            f"Error retrieving profile for username {username}: {str(e)}", exc_info=True, extra={"username": username}
        )
        raise
