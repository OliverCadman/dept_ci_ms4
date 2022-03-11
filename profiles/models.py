from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.validators import MinValueValidator
from django.utils.text import slugify

from django.urls import reverse

import datetime


class Instrument(models.Model):
    """
    Instrument Model
    ------------------------

    Represents a list of individual Instrument choices.

    Used as a ManyToMany field, related to the UserProfile model.

    Attributes:

        instrument_name = Field representing the name of the instrument.
    """

    # Assigning first value in 'choices' tuple to avoid
    # errors and seperate logic.
    VOCALS = "Vocals"
    GUITAR = "Guitar"
    BASS_GUITAR = "Bass Guitar"
    KEYBOARD = "Keyboard"
    PIANO = "Piano"
    DRUMS = "Drums"
    PERC = "Percussion"
    TRUMPET = "Trumpet"
    TENOR_TROMB = "Tenor Trombone"
    BASS_TROMB = "Bass Trombone"
    SOUSAPHONE = "Sousaphone"
    TENOR_SAX = "Tenor Saxophone"
    ALTO_SAX = "Alto Saxphone"
    BARITONE_SAX = "Baritone Saxophone"
    FLUTE = "Flute"
    CLARINET = "Clarinet"
    ACCORDION = "Accordion"
    VIOLIN = "Violin"
    CELLO = "Cello"
    DOUBLE_BASS = "Double Bass"
    VIOLA = "Viola"
    VIBRAPHONE = "Vibraphone"
    HARMONICA = "Harmonica"

    # Define the choices available to the user when selecting their instruments.
    # Passed as 'choices' argument in CharField.
    INSTRUMENTS = [
        (VOCALS, "vocals"),
        (GUITAR, "guitar"),
        (BASS_GUITAR, "bass guitar"),
        (KEYBOARD, "keyboard"),
        (PIANO, "piano"),
        (DRUMS, "drums"),
        (PERC, "percussion"),
        (TRUMPET, "trumpet"),
        (TENOR_TROMB, "tenor trombone"),
        (BASS_TROMB, "bass_trombone"),
        (SOUSAPHONE, "sousaphone"),
        (ALTO_SAX, "alto saxophone"),
        (TENOR_SAX, "tenor saxophone"),
        (BARITONE_SAX, "baritone saxophone"),
        (FLUTE, "flute"),
        (CLARINET, "clarinet"),
        (ACCORDION, "accordion"),
        (VIOLIN, "violin"),
        (VIOLA, "viola"),
        (CELLO, "cello"),
        (DOUBLE_BASS, "double bass"),
        (HARMONICA, "harmonica"),
        (VIBRAPHONE, "vibraphone")
    ]


    instrument_name = models.CharField(max_length=50, unique=True, choices=INSTRUMENTS,
                                       null=True, blank=True, default="All")

    def __str__(self):
        return self.instrument_name


class Genre(models.Model):
    """
    Genre Model
    --------------------

    Represents a list of individual Genre choices.

    Used as a ManyToMany field, related to the UserProfile model.

    Attributes:

        genre_name = Field representing the name of the genre.
    """

    POP = "Pop"
    ROCK = "Rock"
    JAZZ = "Jazz"
    CLASSICAL = "Classical"
    FUNK = "Funk"
    SOUL = "Soul"
    RNB = "RnB"
    PUNK = "Punk"
    LATIN = "Latin"
    BOSSA_NOVA = "Bossa Nova"
    HIP_HOP = "Hip Hop"
    METAL = "Metal"
    PROG_ROCK = "Prog Rock"
    EXPERIMENTAL = "Experimental"
    AMBIENT = "Ambient"
    CLUB_MUSIC = "Club Music"
    HOUSE = "House"

    GENRES = [
        (POP, "pop"),
        (ROCK, "rock"),
        (JAZZ, "jazz"),
        (CLASSICAL, "classical"),
        (FUNK, "funk"),
        (SOUL, "soul"),
        (RNB, "rnb"),
        (PUNK, "punk"),
        (LATIN, "latin"),
        (BOSSA_NOVA, "bossa_nova"),
        (HIP_HOP, "hip_hop"),
        (METAL, "metal"),
        (PROG_ROCK, "prog_rock"),
        (EXPERIMENTAL, "experimental"),
        (AMBIENT, "ambient"),
        (CLUB_MUSIC, "club_music"),
        (HOUSE, "house")
    ]

    genre_name = models.CharField(max_length=50, choices=GENRES, 
                                  null=True, blank=True, unique=True,
                                  default="All")

    def __str__(self):
        return self.genre_name


class UserProfileQueryset(models.QuerySet):
    """
    User Profile Query Set to handle searching and filtering
    through URL query parameters, specified in the "Find a Dep"
    page.

    Methods:

        filter_by_params():
            Query the entire UserProfile object using filter 
            params specified in "Find a Dep" page select 
            elements and buttons.
    """
    
    def filter_by_params(self, filter_params, date_today):
    
        if date_today:
            print("today")
            return self.filter(**filter_params).exclude(unavailable_user__date=date_today)

        return self.filter(**filter_params)
    
    def nested_filter_by_params(self, first_params, second_params):

        return (
            self.filter(**first_params) & self.filter(**second_params)
        )


class UserProfileManager(models.Manager):
    """
    Custom codex manager to handle Custom UserProfileQuerySet

    get_queryset():

    """

    def get_queryset(self):

        return UserProfileQueryset(self.model, using=self._db)

    
    def filter_queryset(self, filter_params, date_today):

        return (
            self.get_queryset().filter_by_params(filter_params, date_today).order_by("-id")
        )
    
    def nested_filter_queryset(self, first_params, second_params):
        return (
            self.get_queryset().nested_filter_by_params(first_params, second_params)
        )


class UserProfile(models.Model):
    """
    UserProfile Model
    ------------------------

    Represents a UserProfile instance.
    
    All fields are editable by the user excluding:

    - subscription_chosen
    - is_paid (Editable if they upgrade subscription of course)
    - invitation_count
    - slug

    Attributes:

    user - A OneToOne field with relation to AllAuth user account.

    first_name - User's First Name

    last_name - User's Last Name

    city - The city where the user resides.

    country - The country where the user resides.

    profile_image - An image field if user chooses to display profile image.

    instruments_played - A ManyToMany field providing user
                        with a choice list of instruments.

    genres - A ManyToMany field providing user with a choice list of genres.

    user_info - A large text field for users to provide their pitch and details.

    subscription_chosen - A Boolean representing if a user has chosen a subscription.

    is_paid - A Boolean representing the user's subscription status.

    invitation_count - An incremental field representing 
                       how many invites a user has received.

    slug - A slug representation of the user's username. Used as parameter in
           profile URL.
    """
 
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=60, null=True, blank=True)
    last_name = models.CharField(max_length=60, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    country = CountryField(blank_label="Country", null=True, blank=True)
    profile_image = models.ImageField(upload_to="uploads", null=True, blank=True)
    instruments_played = models.ManyToManyField(Instrument)
    genres = models.ManyToManyField(Genre)
    user_info = models.TextField(null=True, blank=True)
    subscription_chosen = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    invitation_count = models.IntegerField(default=0, null=True, blank=True, validators=[MinValueValidator(0)])
    slug = models.SlugField(null=True, blank=True, db_index=True)

    # Instantiate custom UserProfileManager
    objects=UserProfileManager()


    def __str__(self):
        return self.user.username

    
    def save(self, *args, **kwargs):
        """ 
        Automatically create a slug from the user's
        username when a UserProfile object is created.
        """
        self.slug = slugify(self.user.username)
        super().save(*args, **kwargs)

    @property
    def calculate_average_rating(self):
        received_reviews = self.received_reviews.all()
        if len(received_reviews) > 0:      
            num_of_reviews = len(received_reviews) 
            total_rating = 0
            for review in received_reviews:
                rating = review.rating
                total_rating += rating
            average_rating = round(total_rating/num_of_reviews)
            return average_rating
        else:
            return None


class Equipment(models.Model):
    """
    Equipment Model
    -----------------

    Represents an individual item of Equipment which a user may declare.

    Attributes:

        equipment_name = Represents the name of the equipment item.
        related_user = A ManytoOne relationship with a given UserProfile.
    """

    class Meta:
        verbose_name_plural = "Equipment"

    equipment_name = models.CharField(max_length=300)
    related_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE,
                                     null=True, blank=True,
                                     related_name="equipment")

    def __str__(self):
        return self.equipment_name


class AudioFile(models.Model):
    """
    AudioFile model
    -----------------

    Represents an individual AudioFile item which a user may add to their
    profile.

    Attributes:
        
        file - The actual file being uploaded.

        file_name - An auto-generated string representation of the uploaded file.

        related_user - A ManyToOne field representing a relationship with a 
                       given UserProfile instance. This is optional since the
                       AudioFile model is shared with the Booking model.

        related_booking - A ManyToOne field representing a relationship with
                          a given Booking instance. Optional, since the AudioFile
                          model is shared with the UserProfile model.
    """

    file = models.FileField(upload_to="audio", null=True, blank=True)
    file_name = models.CharField(max_length=100, null=True, blank=True)
    related_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE,
                                     related_name="users_tracks", null=True, blank=True)
    related_booking = models.ForeignKey("bookings.Booking", on_delete=models.CASCADE,
                                        related_name="audio_resources", null=True, blank=True)

    def get_filename(self, file_path):
        """
        Returns the filename of the audio tracks a user uploads,
        to be used to represent the name each track in the user profile's 
        music player.
        """
        if file_path != "":
            file_url = file_path.url
            file_name = file_url.split("/")[-1]
            self.file_name = file_name

            return self.file_name

    
    def save(self, *args, **kwargs):
        """
        Override default save method to generated
        string representation of filename.
        """
        if self.file:
            if not self.file_name:
                self.file_name = self.get_filename(self.file)
            super().save(*args, **kwargs)


    def __str__(self):
        return self.file.name




class UnavailableDate(models.Model):
    """
    Unavailable Date Model
    -------------------------

    Represents an individual Date object, for the user to declare the 
    dates they are unavailable to perform.

    Attributes:
        date - DateField represented a Python datetime object.

        related_user - ManyToOne field related to a given user.
    """

    date = models.DateField(auto_now=False, null=True)
    related_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE,
                                     related_name="unavailable_user")

    def __str__(self):

        return str(self.date)


@receiver(post_save, sender=User)
def create_or_update_user(sender, instance, created, **kwargs):
    """
    Create a User Profile when a user registers,
    or update the profile if it's already been created.
    """
    if created:
        UserProfile.objects.create(user=instance)
        print(UserProfile.objects.get(user=instance))
    
    # Otherwise, save the profile.
    instance.userprofile.save()






    


    


