import boto3
from botocore.exceptions import ClientError

from decouple import config
from werkzeug.exceptions import InternalServerError


class S3Service:
    def __init__(self):
        self.key = config("AWS_ACCESS_KEY")
        self.secret = config("AWS_SECRET")
        self.s3 = boto3.client(
            "s3", aws_access_key_id=self.key, aws_secret_access_key=self.secret,
        )
        self.bucket = config("AWS_BUCKET")
        self.region = config("AWS_REGION")

    def upload_photo(self, file_name, object_name):
        try:
            ext = file_name.split('.')[-1]
            self.s3.upload_file(file_name, self.bucket, object_name, ExtraArgs={'ACL': 'bucket-owner-full-control', 'ContentType': f'image/{ext}'})
            return f"https://{config('AWS_BUCKET')}.s3.{config('AWS_REGION')}.amazonaws.com/{object_name}"
        except ClientError:
            raise InternalServerError("AWS is not available at the moment")

    def delete_photo(self, object_key):
        self.s3.Object(self.bucket, object_key).delete()
