from django.utils import timezone
from django.db import models
from django_countries.fields import CountryField
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.validators import MinValueValidator, MaxValueValidator

from profiles.models import UserProfile
from jobs.models import Job

import uuid
import datetime


class Invitation(models.Model):
    """
    Invitation Model
    ------------------------------

    A model representing a single Invitation instance.

    Attributes:
        Invitation Number (Charfield):
            A field to hold a UUID string representation
            of an invitation instance. Populated automatically
            upon creation of an Invitation object.

        Invite Sender (FK):
            A many-to-one field related to the user
            who sent the invitation.

        Invite Receiver (FK):
            A many-to-one field related to the user
            who received the invitation.

        Event Name (CharField):
            The name of the event.

        Artist Name (CharField):
            The name of the artist who the dep
            will be playing for.

        Event City (CharField):
            The city where the event is taking place.

        Event Country (Country Field):
            The country where the event is taking place.

        Event DateTime (DateTimeField):
            The date and time of the event.

        Fee (Decimal Field):
            The the amount of money due to be earned
            from playing the event.

        Date of Invitation (DateField):
            The date the invitation was sent.

        Additional InfO (TextField):
            Any additional information about the event.

        Is Accepted (Bool):
            A True/False value representing whether the
            invitation has been accepted by the receiver.

    Methods:
        generate_invitation_number:
            Creates a random UUID string to populate
            the invitation_number field of the model.

        save():
            Custom save method to create random
            invitation number, only upon first creation
            of an Invitation object.

        __str__():
            A string representation of an Invitation
            object.
    """
    invitation_number = models.CharField(
        max_length=50, null=False, editable=False)
    invite_sender = models.ForeignKey(
        UserProfile, on_delete=models.SET_NULL,
        related_name="invitations_sent", null=True)
    invite_receiver = models.ForeignKey(
        UserProfile, on_delete=models.SET_NULL,
        related_name="invitations_received", null=True)
    event_name = models.CharField(max_length=150, null=True)
    artist_name = models.CharField(
        max_length=100, null=True, blank=True)
    event_city = models.CharField(max_length=100)
    event_country = CountryField()
    event_datetime = models.DateTimeField()
    fee = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, default=0)
    date_of_invitation = models.DateField(auto_now_add=True)
    additional_info = models.TextField(null=True, blank=True)
    is_accepted = models.BooleanField(default=False, null=True)

    def generate_invitation_number(self):
        """
        Generate random UUID string to represent invitation
        """
        return uuid.uuid4().hex.upper()

    def save(self, *args, **kwargs):
        """
        Generate a random UUID string upon
        first save of an Invitation object.
        """
        if not self.invitation_number:
            self.invitation_number = (
                self.generate_invitation_number())

        super().save(*args, **kwargs)

    def __str__(self):
        """
        String representation of an Invitation object.
        """
        return self.invitation_number


class Booking(models.Model):
    """
    Booking Model
    --------------------------

    A model to represent a Booking.

    Attributes:
        Related Invitation (OneToOne):
            A OneToOne field related to an accepted invitation.
            Nullable since a Booking object can be shared between
            either a Job or Invitation, depending on the particular case.

        Related Job (OneToOne):
            A OneToOne field related to a confirmed Job.
            Nullable since a Booking object can be shared between
            either a Job or Invitation, depending on the particular case.

        Venue Name (CharField):
            The name of the venue where the event is taking place.

        Street Address 1 (CharField):
            The first line of the venue address.

        Street Address 2 (CharField):
            The second line of the venue address.

        Postcode (CharField):
            The venue's postcode.

        Travel Provided (Bool):
            A True/False value representing whether travel
            is being provided or not.

        Travel Info (TextField):
            Any travel information for the event. Available
            only when travel_provided value is True.

        Backline Provided (Bool):
            A True/False value representing whether backline
            is being provided or not.

        Backline Info (TextField):
            Any backline information for the event. Available
            only when backline_provided value is True.

    Methods:
        __str__(): The string representation of a Booking object.
    """

    related_invitation = models.OneToOneField(
        Invitation, on_delete=models.CASCADE,
        related_name="related_booking", null=True,
        blank=True)
    related_job = models.OneToOneField(
        Job, on_delete=models.CASCADE, related_name="job_booking",
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
        if invitation.is_accepted:
            Booking.objects.create(related_invitation=invitation)


class Review(models.Model):
    """
    Review Model
    --------------------------------------------

    Model representing a single Review instance.

    Attributes:
        related_booking (FK):
            The Booking instance associated with the review, if any.
            If related booking exists, information about the
            booking will be displayed alongside the review content.

        review_receiver (FK):
            The UserProfile instance which is being reviewed.

        review_sender (FK):
            The UserProfile instance which is writing the review.

        review_content (TextField):
            The text content of the review.

        review_created (DateTimeField):
            An uneditable DateTimeField representing the
            date and time when the review was created.

        review_modified (DateTimeField):
            An editable DateTimeField representing the
            date and time when the review was modified.

        rating (SmallIntegerField):
            An integer range from 1-5, representing a "star"
            rating.

    Methods:
        __str__():
            A string representation of a Review object.

        round_time():
            A function to round a datetime object.
            Used in order to provide comparison in time between
            review creation and review modification in model property
            'is_modified', since efforts to compare the time without
            this function lead to unexpected results, possibly due to
            the time-lapse of the objects differing
            by a matter of milliseconds.

        save():
            Populates the review_created DateTime field with a datetime
            object, and updates the review_modified field with the present
            datetime each time the model is updated.

        is_modified():
            A property to compare the two review_created and review_modified
            fields, in order to render an '(edited)' stamp on a review,
            if it has been edited.
    """

    related_booking = models.ForeignKey(
        Booking, on_delete=models.CASCADE,
        related_name="reviews", null=True, blank=True)
    review_receiver = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE,
        related_name="received_reviews", null=True, blank=True)
    review_sender = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE,
        related_name="sent_reviews", null=True, blank=True)
    review_content = models.TextField(max_length=800)
    review_created = models.DateTimeField(editable=False)
    review_modified = models.DateTimeField(null=True, blank=True)
    rating = models.SmallIntegerField(null=True, blank=True,
                                      validators=[MinValueValidator(0),
                                                  MaxValueValidator(5)])

    def __str__(self):
        """
        Return a string representation of a single Review instance.
        """
        return (
            f"Review for {self.review_receiver}")

    def round_time(self, dt=None, roundTo=60):
        """
        Round a datetime object to any time lapse in seconds
        dt : datetime.datetime object, default now.
        roundTo : Closest number of seconds to round to, default 1 minute.

        Used to overcome issues with 'is_modified' method not returning
        the expected result, possibly due to the time-lapse from
        review_created and review_modified DateTime objects differing
        by a matter of milliseconds.

        Code referenced from Stack Overflow:

        https://stackoverflow.com/questions/3463930/\n
        how-to-round-the-minute-of-a-datetime-object/10854034#10854034
        """
        if dt is None:
            dt = datetime.datetime.now()
        seconds = (dt.replace(tzinfo=None) - dt.min).seconds
        rounding = (seconds+roundTo/2) // roundTo * roundTo
        return dt + datetime.timedelta(0, rounding-seconds, -dt.microsecond)

    def save(self, *args, **kwargs):
        """
        Override the default save method, populating
        the "review_created" field with current date and time when a
        review instance is created.

        Date added to review_created field only if
        there is no Review ID present.

        Otherwise, the review_modified field is updated.
        """
        if not self.pk:
            self.review_created = timezone.now()
        self.review_modified = timezone.now()
        return super(Review, self).save(*args, **kwargs)

    @property
    def is_modified(self):
        """
        Returns True if the date a review has been modified
        is 'larger' than the date it was created.
        Used in the Profile page to inform the user that
        a given review has been edited.

        round_time() function is used to round the
        time objects to the nearest minute.
        """

        rounded_modified_date = self.round_time(
            self.review_modified, roundTo=1*60)
        rounded_created_date = self.round_time(
            self.review_created, roundTo=1*60)
        return rounded_modified_date > rounded_created_date
