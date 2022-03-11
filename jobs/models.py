from django.db import models
from django_countries.fields import CountryField

from profiles.models import UserProfile


class Job(models.Model):
    """
    Model representing an instance of a job.

    Attributes:

        Job Poster (FK) - The member posting the job advertisement.

        Interested Member (FK) - The member registering interest in doing job.(

        Event Name (CharField) - The name of the event taking place.

        Artist Name (CharField) - The name of the artist who the job is for.

        Job Description (TextField) - A description of what the job entails.

        Fee (DecimalField) - The fee for the job.

        Venue Name (CharField) - The name of the venue where the job is taking place.

        Street Address 1 (CharField) - The venue name/number and street.

        Street Address 2 (CharField) - A second street address line (if required).

        Postcode (CharField) - The venue's postcode.

        Event City (CharField) - The city where the event is taking place.

        Event Country (CountryField) - The country where the event is taking place.

        Event DateTime (DateTimeField) - THe date and time of the event.

        Travel Provided (Boolean) - Represents whether travel is provided or not.

        Travel Info (TextField) - Travel information (if applicable).

        Backline Provided (Boolean) - Represents whether equipment is provided or not.

        Backline Info (TextField) - Equipment Information (if applicable).

        Interest Count (IntegerField) - An incremental field representing the amount
                                        of interest the job has received.

        Is Taken (Boolean) - Represents whether a dep has been confirmed to play the job.



    """

    job_poster = models.ForeignKey(UserProfile, on_delete=models.CASCADE,
                                   related_name="posted_jobs")
    interested_member = models.ForeignKey(UserProfile, on_delete=models.SET_NULL,
                                          null=True, related_name="jobs")
    event_name = models.CharField(max_length=150)
    artist_name = models.CharField(max_length=100, null=True, blank=True)
    job_description = models.TextField(max_length=500)
    fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=0)
    venue_name = models.CharField(max_length=100, null=True, blank=True)
    street_address1 = models.CharField(max_length=80, null=True, blank=True)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    event_city = models.CharField(max_length=100)
    event_country = CountryField()
    event_datetime = models.DateTimeField()
    travel_provided = models.BooleanField(default=False, null=True)
    travel_info = models.TextField(null=True, blank=True)
    backline_provided = models.BooleanField(default=False, null=True)
    backline_info = models.TextField(null=True, blank=True)
    interest_count = models.IntegerField(null=True, blank=True, default=0)
    is_taken = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.job_poster}'s job: {self.event_name}"



