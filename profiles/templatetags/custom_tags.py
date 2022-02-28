from django import template
from profiles.models import UserProfile
from django.shortcuts import get_object_or_404

from social.models import Message
from bookings.models import Invitation

register = template.Library()

@register.inclusion_tag("includes/account_navbar.html", takes_context=True)
def display_user(context):
    """
    Inclusion tag used to render request user's profile details in navigation bar's
    "My Account" dropdown.
    """
    
    request_user = context["request"].user
    user_profile = get_object_or_404(UserProfile, user__username=request_user)
    return {"user_profile": user_profile}


@register.filter(name="count_unread_messages")
def count_unread_messages(invitation_id):
    """
    Returns the amount of unread messages for a given invitation.
    To be used in Dashboard page; unread messages are indicated
    on button "Message <user>"
    """
    unread_messages = Message.objects.filter(invitation_id=invitation_id, is_read=False)
    unread_message_count = len(unread_messages)
    return unread_message_count