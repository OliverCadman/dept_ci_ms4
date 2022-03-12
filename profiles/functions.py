from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.http import urlencode

from bookings.models import Invitation
from .models import UserProfile



def calculate_invite_acceptance_delta(username):
    """
    Calculates the difference between the amount of invites 
    a user has received, and those which are accepted.
    """
    user_profile = get_object_or_404(UserProfile, user__username=username)
    if user_profile is not None:
        invite_count = user_profile.invitation_count
        
        accepted_invitations = Invitation.objects.filter(invite_receiver=user_profile).filter(is_accepted=True)
        invite_acceptance_delta = invite_count - accepted_invitations.count()
        return invite_acceptance_delta


def calculate_profile_progress_percentage(username):
    user_profile = get_object_or_404(UserProfile, user__username=username)

    fields = user_profile.__dict__
    print(fields)
    null_object = {}
    rounded_percentage = 0

    for key, value in fields.items():
        if key != "invitation_count" and key != "is_paid":
            if value == None or value == "" or value == False:
                null_object[key] = value
                if null_object[key] == "profile_image":
                    null_object["profile_image"] = None

    users_instruments =  user_profile.instruments_played.all()
    if not users_instruments:
        null_object["instruments_played"] = None

    users_genres = user_profile.genres.all()
    if not users_genres:
        null_object["genres"] = None

    users_equipment = user_profile.equipment.all()
    if not users_equipment or len(users_equipment) == 0:
        null_object["equipment"] = None
   

    users_tracks = user_profile.users_tracks.all()
    if not users_tracks:
        null_object["users_tracks"] = None

    unavailable_dates = user_profile.unavailable_user.all()
    if not unavailable_dates:
        null_object["unavailable_dates"] = None

    num_of_null_values = len(null_object)
    num_of_fields = 11
    if num_of_null_values < num_of_fields:
        num_of_completed_fields = num_of_fields - num_of_null_values
        progress_percentage = (
            (num_of_completed_fields / num_of_fields) * 100
        )
        rounded_percentage = round(progress_percentage)

    return rounded_percentage
        