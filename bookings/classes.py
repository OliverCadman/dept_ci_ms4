import boto3
from botocore.client import Config
import os



class DownloadS3Object(object):
    """
    DownloadS3Object
    -------------------------
    Downloads audio resources in relation to a given booking,
    if uploaded by the user upon submitting the Booking form.

    Methods:

        __init__():
            Initializes the attributes passed in as arguments:
                access_key - Amazon AWS Access Key ID
                secret_key - Amazon AWS Secret Access Key

        
        create_boto3_session():
            Instantiate boto3 session, passing in the access key
            and secret access key provided in instance variables.

        
        generate_download_url():
            Create an Amazon AWS "presigned url", containing
            the, bucket name, file path (as key), and expiration,
            as well as required content type and content disposition
            headers.
    """
    access_key = None
    secret_key = None

    def __init__(self, access_key, secret_key, region, *args, **kwargs):
        """
        Initialize instance variables
        """
        self.access_key = access_key
        self.secret_key = secret_key
        self.region = region
        super(DownloadS3Object, self).__init__(*args, **kwargs)

    def create_boto3_session(self):
        """
        Instantiate a boto3 client
        """
        client = boto3.client(
            "s3",
            config=Config(signature_version="s3v4"),
            region_name=self.region,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key
        )
        
        return client

    def generate_download_url(self, bucket_name, path, expiration):
        """
        Create an AWS presigned URL, with bucket_name, path and expiration
        passed in upon calling the method in "bookings/views.py"

        Content Type and Content Disposition headers tell the browser to
        download the file, rather than opening a new page.
        """

        if path:
            client = self.create_boto3_session()
            filename = os.path.basename(path)
            try:
                download_url = client.generate_presigned_url(
                    "get_object",
                    Params={
                        "Bucket": bucket_name,
                        "Key": path,
                        "ResponseContentType": "audio/mpeg;force-download",
                        "ResponseContentDisposition": "attachment;filename=%s"%filename
                    },
                    ExpiresIn=expiration,
                )
                return download_url
            except Exception:
                return None
        else:
            return None
    