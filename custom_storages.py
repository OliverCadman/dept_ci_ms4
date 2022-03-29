from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage

"""
Custom Storages to store Media and Static
Files using Amazon AWS, in production.
"""


class StaticStorage(S3Boto3Storage):
    """
    Define location for static files.
    """
    location = settings.STATICFILES_LOCATION


class MediaStorage(S3Boto3Storage):
    """
    Define location for media files.
    """
    location = settings.MEDIAFILES_LOCATION
