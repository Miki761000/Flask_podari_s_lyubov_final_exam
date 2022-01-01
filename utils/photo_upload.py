import os
import uuid

from constants import TEMP_FILE_FOLDER
from services.s3 import S3Service
from utils.helpers import decode_photo

s3 = S3Service()


def photo_upload(data):
    photo_name = f"{str(uuid.uuid4())}.{data.pop('image_extension')}"
    path = os.path.join(TEMP_FILE_FOLDER, photo_name)
    decode_photo(data.pop("product_image"), path)
    product_image = s3.upload_photo(path, photo_name)
    os.remove(path)
    data["product_image"] = product_image
    return data
