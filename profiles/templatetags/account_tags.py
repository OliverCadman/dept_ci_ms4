from django import template
from profiles.models import UserProfile
from django.shortcuts import get_object_or_404

register = template.Library()

@register.inclusion_tag("includes/account_navbar.html", takes_context=True)
def display_user(context):
    request_user = context["request"].user
    user_profile = get_object_or_404(UserProfile, user__username=request_user)
    return {"user_profile": user_profile}