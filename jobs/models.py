from django.db import models
from django_countries.fields import CountryField

from profiles.models import UserProfile, Instrument

from pathlib import Path
from PIL import Image


class JobQuerySet(models.QuerySet):

    def filter_by_params(self, filter_params, min_fee, max_fee):
        if not min_fee and not max_fee:
            return self.filter(**filter_params)
        else:
            return self.filter(**filter_params, fee__range=(min_fee, max_fee))

class JobManager(models.Manager):

    def get_queryset(self):
        return JobQuerySet(self.model, using=self._db)

    def filter_queryset(self, filter_params, min_fee, max_fee):
        if not min_fee and not max_fee:
             return self.get_queryset().filter_by_params(filter_params).order_by("-id")
        else:
            return self.get_queryset().filter_by_params(filter_params, min_fee, max_fee)


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

        Event City (CharField) - The city where the event is taking place.

        Event Country (CountryField) - The country where the event is taking place.

        Event DateTime (DateTimeField) - THe date and time of the event.

        Interest Count (IntegerField) - An incremental field representing the amount
                                        of interest the job has received.

        Is Taken (Boolean) - Represents whether a dep has been confirmed to play the job.
    """

    job_poster = models.ForeignKey(UserProfile, on_delete=models.CASCADE,
                                   related_name="posted_jobs")
    interested_member = models.ForeignKey(UserProfile, on_delete=models.SET_NULL,
                                          null=True, blank=True, related_name="jobs")
    job_title = models.CharField(null=True, max_length=150)
    image = models.ImageField(upload_to="job_images", null=True, blank=True)
    event_name = models.CharField(max_length=150)
    instrument_required = models.ManyToManyField(Instrument)
    artist_name = models.CharField(max_length=100, null=True, blank=True)
    job_description = models.TextField(max_length=500)
    fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=0)
    event_city = models.CharField(max_length=100)
    event_country = CountryField()
    event_datetime = models.DateTimeField()
    interest_count = models.IntegerField(null=True, blank=True, default=0)
    is_taken = models.BooleanField(default=False)

    objects = JobManager()

    def __str__(self):
        return f"{self.job_poster}'s job: {self.event_name}"

    def convert_to_webp(self, source):
        

        if self.image is not None or source is not None:
            image_to_convert = source
            image = Image.open(image_to_convert)
            image.save(image_to_convert.name, format="webp")
            print(image.size)
            return image

    def save(self, *args, **kwargs):
        if self.image:
            self.convert_to_webp(self.image.file)
        super().save(*args, **kwargs)




        
