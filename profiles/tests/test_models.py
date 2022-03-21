from django.shortcuts import get_object_or_404
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.utils import timezone

from profiles.models import (UserProfile, Instrument, Genre,
                             Equipment, UnavailableDate, AudioFile)

from bookings.models import Review

import tempfile

class TestProfileModel(TestCase):
    """
    Unit Test Profile Model
    """
    
    def setUp(self):
        """
        Create user and log them in, then retrieve
        user's user profile.

        N.B. User Profile model is created upon Auth User creation

        Initialize UserProfile fields to instance
        variables.
        """
        username = "test"
        password = "abc123"
        user_model = get_user_model()
        self.user = user_model.objects.create_user(
            username=username,
            password=password
        )
        self.user_profile = UserProfile.objects.get(user__username=self.user)
        self.logged_in = self.client.login(username=username, password=password)

        self.first_name = "test_fname"
        self.last_name = "test_lname"
        self.city = "test_city"
        self.country = "test_country"
        self.profile_image = tempfile.NamedTemporaryFile(suffix=".jpg").name
        self.user_info = "test_user_info"


    def test_userprofile_update(self):
        """
        Update User Profile model with instance variables provided in setup
        and confirm that the fields are saved correctly.
        """

        user_profile = self.user_profile

        user_profile.first_name = self.first_name
        user_profile.last_name = self.last_name
        user_profile.city = self.city
        user_profile.country = self.country
        user_profile.profile_image = self.profile_image
        user_profile.user_info = self.user_info
        user_profile.save()

    
        self.assertTrue(self.first_name, user_profile.first_name)
        self.assertTrue(self.last_name, user_profile.last_name)
        self.assertTrue(self.city, user_profile.city)
        self.assertTrue(self.country, user_profile.country)
        self.assertTrue(self.user_profile.first_name, "test_fname")
        self.assertTrue(self.profile_image, user_profile.profile_image.name)
        self.assertTrue(self.user_info, user_profile.user_info)

    def test_userprofile_str(self):
        """
        Test the string method of the UserProfile model.
        """
        self.assertEqual(str(self.user_profile), "test")

    def test_userprofile_slug_creation(self):
        """
        Confirm that a representative slug is created upon
        creation of a user profile model.
        """
        self.assertEqual(self.user_profile.slug, "test")

    def test_calculate_average_rating(self):
        """
        Confirm the "calculate_average_rating" method
        returns the correct value.

        Create three review objects related to the UserProfile
        instantiated in setUp method, and create control dictionary
        to compare against dictionary returned from model property.
        """
        user_model = get_user_model()
        test_review_sender = user_model.objects.create_user(
            username="review_sender",
            password="reviewer_password",
            email="reviewer_email"
        )
        test_reviewsender_userprofile = get_object_or_404(UserProfile,
                                                          user=test_review_sender)

        test_reviewreceiver_userprofile = get_object_or_404(UserProfile,
                                                            user=self.user)
        Review.objects.bulk_create([
            Review(
                review_sender=test_reviewsender_userprofile,
                review_receiver=test_reviewreceiver_userprofile,
                review_content="test review 1",
                review_created=timezone.now(),
                rating=3
            ),
             Review(
                review_sender=test_reviewsender_userprofile,
                review_receiver=test_reviewreceiver_userprofile,
                review_content="test review 2",
                review_created=timezone.now(),
                rating=5
            ),
             Review(
                review_sender=test_reviewsender_userprofile,
                review_receiver=test_reviewreceiver_userprofile,
                review_content="test review 3",
                review_created=timezone.now(),
                rating=2
            )     
        ])  

        # Calculate control values 
        control_total_rating = 3 + 5 + 2
        control_num_of_reviews = 3
        control_average_rating = round(control_total_rating / control_num_of_reviews)

        # Create control dict
        control_dict = {
            "average_rating": control_average_rating,
            "num_of_reviews": control_num_of_reviews
        }

        # Dictionary returned from UserProfile method
        test_dict = self.user_profile.calculate_average_rating
        self.assertEqual(control_dict, test_dict)


class TestInstrumentModel(TestCase):
    """
    Unit Tests - Instrument Model
    """

    def setUp(self):
        """
        Create an instrument object with instrument name
        """
        self.instrument = Instrument.objects.create(
            instrument_name="test_instrument_1"
        )
    
    def test_instrument_creation(self):
        """
        Retrieve instrument instance created in setUp method,
        and confirm that the instrument names match.
        """
        control_instrument = Instrument.objects.get(pk=1)
        self.assertTrue( self.instrument.instrument_name, "test_instrument_1")


    def test_instrument_str(self):
        """
        Confirm the Instrument model's string method returns
        correct value.
        """
        control_instrument = self.instrument
        self.assertEqual(str(control_instrument), "test_instrument_1")


class TestGenreModel(TestCase):
    """
    Unit Tests - Genre Model
    """

    def setUp(self):
        """
        Create a Genre object with genre_name included.
        """

        self.genre = Genre.objects.create(
            genre_name="test_genre_1"
        )

    def test_genre_creation(self):
        """
        Retrieve genre instance created in setUp method,
        and confirm that the genre names match.
        """

        control_genre = Genre.objects.get(pk=1)
        self.assertEqual(control_genre.genre_name, "test_genre_1")


    def test_genre_str(self):
        """
        Confirm the Genre model's string method returns correct
        value.
        """
        control_genre = self.genre
        self.assertEqual(str(control_genre), "test_genre_1")


class TestAudiofileModel(TestCase):
    """
    Unit Tests - AudioFile Model
    """

    def setUp(self):
        """
        Create an AudioFile object with NamedTemporaryFile as test
        file.
        """
        self.test_file = tempfile.NamedTemporaryFile(suffix=".mp3").name
        self.audiofile = AudioFile.objects.create(
            file = self.test_file,
        )


    def test_audiofile_creation(self):
        """
        Confirm that the correct audiofile object is 
        retrieved.
        """
        test_audiofile = AudioFile.objects.get(
            pk=1
        )
    
        self.assertTrue(self.audiofile, test_audiofile)

    def test_audiofile_str(self):
        """
        Confirm that the AudioFile's string method returns
        the correct value.

        To do this, get the test_file from setUp method,
        and copy the string, then extract the filename
        from the last item in the filepath represented in
        the string, and compare that value to the str() value
        of the control audiofile.
        """

        control_audiofile = self.audiofile

        # Turn test_filepath into a string
        test_filepath = "%s"%self.test_file

        # Extract the filename from the string.
        test_filename = "".join(test_filepath.split("/")[-1:])

        self.assertEqual(str(control_audiofile), test_filename)


class TestUnavailableDateModel(TestCase):
    """
    Unit Tests - UnavailableDate Model
    """
    def setUp(self):
        """
        Create an UnavailableDate object, and a UserProfile
        for the object to relate to.
        """
        username = "test"
        password = "abc123"
        user_model = get_user_model()
        self.user = user_model.objects.create_user(
            username=username,
            password=password
        )
        self.user_profile = UserProfile.objects.get(user__username=self.user)

        self.test_date = timezone.localdate()
        self.unavailable_date = UnavailableDate.objects.create(
            date=self.test_date,
            related_user=self.user_profile
        )

    def test_unavailabledate_str(self):
        """
        Confirm the UnavailableDate string method returns the 
        correct value.
        """
        self.assertEqual(str(self.unavailable_date), str(timezone.localdate()))
