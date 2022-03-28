from django.shortcuts import get_object_or_404
from django.test import TestCase
from django.utils import timezone

from .models import Job
from profiles.models import UserProfile

from test_helpers import create_test_user, create_test_job

import datetime
from math import inf

class TestJobModel(TestCase):
    """
    Unit Testing for the Job Model, to confirm that
    each field of the Job model handles and returns
    the fields successfully.
    """

    def setUp(self):
        """
        Setup Test user to relate to Job object
        """
        username = "test"
        password = "test"
        email = "test@test.com"

        self.test_user_1 = create_test_user(username, password, email)
        self.test_user_profile_1 = get_object_or_404(
            UserProfile, user__username=self.test_user_1)

        # Create a Job object (function defined in test_helpers.py)
        self.test_job = create_test_job(
            self.test_user_profile_1
        )

        # Confirm that the fields of the returned job match fields inputted
        self.assertEqual(self.test_job.job_title, "test_job")
        self.assertEqual(self.test_job.event_name, "test_event")
        self.assertEqual(self.test_job.artist_name, "test_artist")
        self.assertEqual(self.test_job.event_city, "test_city")
        self.assertEqual(self.test_job.event_country, "GB")
        self.assertEqual(self.test_job.event_datetime, datetime.datetime(
            2022, 2, 23, 19, 36, 57))
        self.assertEqual(self.test_job.job_description, "test_desc")
        self.assertEqual(self.test_job.job_poster, self.test_user_profile_1)
        

    def test_job_str(self):
        """
        Confirm that the Job model's string method returns
        the correct string representation.
        """
        control_str = f"{self.test_user_profile_1}'s job: {self.test_job.event_name}"
        self.assertEqual(str(self.test_job), control_str)

    
    def test_filter_queryset(self):

        filter_params = {"event_city__iexact" : "test_city"}

        query = Job.objects.filter_queryset(
            filter_params=filter_params,
            min_fee=1,
            max_fee=inf
        )

        print(query)


        
