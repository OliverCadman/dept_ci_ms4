from django import template
from django.shortcuts import get_object_or_404
from social.models import Notification

from profiles.models import UserProfile

# Instantiate the template library
register = template.Library()


@register.inclusion_tag("social/show_notifications.html", takes_context=True)
def show_notifications(context):
    """
    Inclusion tag to retrieve Notifications sent to a User, to
    be displayed in the Navbar.

    Required since the Navbar doesn't have it's own view to
    process business logic.
    """
    user = context["request"].user
    user_profile = get_object_or_404(UserProfile, user__username=user)
    notifications = (
        Notification.objects.filter(notification_receiver=user_profile)
        .exclude(is_read=True).order_by("-id"))
    return {"notifications": notifications}
