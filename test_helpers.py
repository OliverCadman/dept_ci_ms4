from django.contrib.auth import get_user_model
from django.utils import timezone
from bookings.models import Invitation
from jobs.models import Job
from social.models import Message

import datetime

"""
Test Helpers
----------------

Functions to create test users, invitations and jobs
to use when Unit Testing.
"""


def create_test_user(username, password, email):
    """
    Test helper to create a test user for Unit Testing
    """
    user_model = get_user_model()
    user = user_model.objects.create_user(
        username=username,
        password=password,
        email=email
    )
    return user


def create_test_invitation(invite_sender, invite_receiver):

    test_invitation = Invitation.objects.create(
            invite_sender=invite_sender,
            invite_receiver=invite_receiver,
            event_name="test_event",
            artist_name="test_artist",
            event_city="test_city",
            event_country="GB",
            event_datetime=timezone.now(),
            fee=150.00,
            additional_info="test_additional_info"
        )

    return test_invitation


def create_test_job(job_poster):

    test_job = Job.objects.create(
            job_poster=job_poster,
            job_title="test_job",
            event_name="test_event",
            artist_name="test_artist",
            event_city="test_city",
            event_country="GB",
            event_datetime=datetime.datetime(
                2022, 2, 23, 19, 36, 57),
            job_description="test_desc"
        )

    return test_job


def create_test_job_variable_city(job_poster, city_name):

    test_job = Job.objects.create(
            job_poster=job_poster,
            job_title="test_job",
            event_name="test_event",
            artist_name="test_artist",
            event_city=city_name,
            event_country="GB",
            event_datetime=datetime.datetime(
                2022, 2, 23, 19, 36, 57),
            job_description="test_desc"
        )

    return test_job


def create_test_message(message_sender, message_receiver,
                        related_job=None, related_invitation=None):

    test_message = Message.objects.create(
        message_sender=message_sender,
        message_receiver=message_receiver,
        related_job=related_job,
        invitation_id=related_invitation,
        message="test"
    )

    return test_message
