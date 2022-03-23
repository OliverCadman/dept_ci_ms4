from django.utils import timezone
from django.db import models
from django_countries.fields import CountryField
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.validators import MinValueValidator, MaxValueValidator

from profiles.models import UserProfile
from jobs.models import Job

import uuid


class Invitation(models.Model):
    invitation_number = models.CharField(max_length=50, null=False, editable=False)
    invite_sender = models.ForeignKey(UserProfile, on_delete=models.SET_NULL,
                                      related_name="invitations_sent", null=True)
    invite_receiver = models.ForeignKey(UserProfile, on_delete=models.SET_NULL,
                                        related_name="invitations_received", null=True)
    event_name = models.CharField(max_length=150, null=True)
    artist_name = models.CharField(max_length=100, null=True, blank=True)
    event_city = models.CharField(max_length=100)
    event_country = CountryField()
    event_datetime = models.DateTimeField()
    fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=0)
    date_of_invitation = models.DateField(auto_now_add=True)
    additional_info = models.TextField(null=True, blank=True)
    is_accepted = models.BooleanField(default=False, null=True)

    def generate_invitation_number(self):
        """
        Generate random UUID string to represent invitation
        """
        return uuid.uuid4().hex.upper()


    def save(self, *args, **kwargs):
        if not self.invitation_number:
            self.invitation_number = self.generate_invitation_number()
           
        super().save(*args, **kwargs)

    def __str__(self):
        return self.invitation_number


class Booking(models.Model):
    related_invitation = models.OneToOneField(Invitation, on_delete=models.CASCADE,
                                              related_name="related_booking", null=True,
                                              blank=True)
    related_job = models.OneToOneField(Job, on_delete=models.CASCADE, related_name="job_booking",
                                       null=True, blank=True)
    venue_name = models.CharField(max_length=100, null=True, blank=True)
    street_address1 = models.CharField(max_length=80, null=True, blank=True)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    travel_provided = models.BooleanField(default=False, null=True)
    travel_info = models.TextField(null=True, blank=True)
    backline_provided = models.BooleanField(default=False, null=True)
    backline_info = models.TextField(null=True, blank=True)
    booking_details_sent = models.BooleanField(default=False)

    def __str__(self):
        if self.related_invitation:
            return f"T1 Booking: {self.related_invitation.event_name}"
        elif self.related_job:
            return self.related_job.event_name


class SheetMusic(models.Model):
    related_booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    file_url = models.FileField(upload_to="sheet_music")

    def __str__(self):
        return self.file_url


@receiver(post_save, sender=Invitation)
def create_tier_one_booking(sender, instance, created, *args, **kwargs):
    if not created:
        invitation = instance
        if invitation.is_accepted == True:
            Booking.objects.create(related_invitation=invitation)


class Review(models.Model):
    """
    Model representing a single Review instance.

    Attributes:
        related_booking (FK) - The Booking instance associated with the review, if any.
                               If related booking exists, information about the 
                               booking will be displayed alongside the review content.
        
        review_receiver (FK) - The UserProfile instance which is being reviewed.

        review_sender (FK) - The UserProfile instance which is writing the review.

        review_content (TextField) - The text content of the review.

        review_created (DateTimeField) - An uneditable DateTimeField representing the
                                         date and time when the review was created.
        
        review_modified (DateTimeField) - An editable DateTimeField representing the 
                                          date and time when the review was modified.

        rating (SmallIntegerField) - An integer range from 1-5, representing a "star"
                                     rating.
    
    """
    related_booking = models.ForeignKey(Booking, on_delete=models.CASCADE,
                                        related_name="reviews", null=True, blank=True)
    review_receiver = models.ForeignKey(UserProfile, on_delete=models.CASCADE,
                                        related_name="received_reviews", null=True, blank=True)
    review_sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE, 
                                      related_name="sent_reviews", null=True, blank=True)
    review_content = models.TextField(max_length=800)
    review_created = models.DateTimeField(editable=False)
    review_modified = models.DateTimeField(null=True, blank=True)
    rating = models.SmallIntegerField(null=True, blank=True,
                                      validators=[MinValueValidator(0), MaxValueValidator(5)])

    def __str__(self):
        """
        Return a string representation of a single Review instance.
        """
        return (
            f"Review for {self.review_receiver}")

    def save(self, *args, **kwargs):
        """
        Override the default save method, populating the "review_created" field
        with current date and time when a review instance is created.

        Date added to review_created field only if there is no Review ID present.

        Otherwise, the review_modified field is updated.
        """
        if not self.pk:
            self.review_created = timezone.now()
        self.review_modified = timezone.now()
        return super(Review, self).save(*args, **kwargs)
