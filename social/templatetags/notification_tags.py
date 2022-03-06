from django import template
from django.shortcuts import get_object_or_404
from social.models import Notification


from profiles.models import UserProfile

register = template.Library()

@register.inclusion_tag("social/show_notifications.html", takes_context=True)
def show_notifications(context):
    user = context["request"].user
    user_profile = get_object_or_404(UserProfile, user__username=user)
    notifications = Notification.objects.filter(
        notification_receiver=user_profile).exclude(is_read=True).order_by("-id")

    return { "notifications": notifications }