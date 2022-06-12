from typing import Tuple, Dict
import io

import boto3
from config import ConfigAWS
import uuid
import os
from PIL import Image
import pyheif


class UploadAws:
    @classmethod
    def upload_advert_image(cls, file):
        endpoint = 'f'
        bucket = 'adverts'

        verify, _error = cls.verify_file(file)
        if not verify:
            return verify, _error

        file_name = f"{cls.generate_uniq_name()}.jpeg"
        comp_file, file_info = cls.compression_file(file=file)
        status, _error = cls.upload(file=comp_file, file_name=file_name, endpoint=endpoint, bucket=bucket)
        if status:
            return status, {
                'path': f'{ConfigAWS.AWS_ENDPOINT}/{endpoint}/{bucket}/{file_name}',
                **file_info,
            }
        else:
            return status, _error

    @classmethod
    def upload_full_avatar(cls, file) -> Tuple[bool, str | Dict] | str:
        endpoint = 'avatars'
        bucket = 'full'

        verify, _error = cls.verify_file(file)
        if not verify:
            return verify, _error

        file_name = f"{cls.generate_uniq_name()}.jpeg"
        comp_file, file_info = cls.compression_file(file=file)
        status, _error = cls.upload(file=comp_file, file_name=file_name, endpoint=endpoint, bucket=bucket)

        if status:
            response_upload_mini_avatar = cls.upload_mini_avatar(file=comp_file, endpoint=endpoint, file_name=file_name)
            return status, {
                                'name': file_name,
                                'full_avatar_path': f'{ConfigAWS.AWS_ENDPOINT}/{endpoint}/{bucket}/{file_name}',
                                **response_upload_mini_avatar,
                                **file_info
                            }
        else:
            return status, _error

    @classmethod
    def upload_mini_avatar(cls, endpoint, file, file_name):
        image = Image.open(io.BytesIO(file))
        image = cls.crop_center(image, min(image.size), min(image.size))
        image = image.resize((100, 100), Image.ANTIALIAS)
        upload_dir = f'main/service/aws/temp/{cls.generate_uniq_name()}.jpeg'
        image.save(upload_dir)
        file = open(upload_dir, 'rb').read()
        os.remove(upload_dir)
        status, _error = cls.upload(file=file, file_name=file_name, endpoint="avatars", bucket="mini")
        if status:
            return {
                'mini_avatar_path': f'{ConfigAWS.AWS_ENDPOINT}/{endpoint}/mini/{file_name}'
            }
        else:
            raise Exception("Error!")

    @classmethod
    def upload(cls, file, file_name, endpoint, bucket) -> Tuple[bool, str]:
        try:
            s3 = boto3.client(service_name='s3', endpoint_url=f"{ConfigAWS.AWS_ENDPOINT}/{endpoint}/", region_name=ConfigAWS.REGION, aws_access_key_id=ConfigAWS.AWS_ACCESS_KEY_ID, aws_secret_access_key=ConfigAWS.AWS_SECRET_KEY)
            response = s3.put_object(Bucket=bucket,
                                     Key=file_name,
                                     Body=file,
                                     ContentType="image/jpeg",
                                     ACL="public-read")
            if response['ResponseMetadata']['HTTPStatusCode'] in (200, 201, 202, 203, 204):
                return True, ''
            else:
                return False, 'Error upload!'
        except Exception:
            raise

    @classmethod
    def verify_file(cls, file) -> Tuple[bool, str]:
        size = os.fstat(file.fileno()).st_size
        file_type = cls.check_type(file)

        if not file_type:
            return False, 'This is not correct file type!'
        if not size <= ConfigAWS.MAX_CONTENT_LENGTH:
            return False, 'Sorry,Image size must be less then 6 MB!'
        return True, ''

    @classmethod
    def check_type(cls, file) -> bool | str:
        allowed_types = {'gif': 'image/gif', 'png': 'image/png', 'jpeg': 'image/jpeg', 'jpg': 'image/jpg', 'tiff': 'image/tiff', 'heic': 'image/heic', 'heif': 'image/heif'}
        file_type = file.mimetype
        if file_type in allowed_types.values():
            return file_type
        else:
            return False

    @classmethod
    def generate_uniq_name(cls) -> str:
        return str(uuid.uuid4()).replace('-', '')

    # Return file and his size
    @classmethod
    def compression_file(cls, file):
        # Save file
        filename = f"{cls.generate_uniq_name()}"
        filename_type = f"{file.filename.split('.')[-1]}"
        upload_dir = f'main/service/aws/temp/{filename}.{filename_type}'
        file.save(os.path.join(upload_dir))

        # print("%.1f KB" % round(os.path.getsize(upload_dir) / 1024, 1))
        # Check HEIF
        if filename_type in ['heic', 'heif', 'avif']:
            image, size = cls.convert_heif(upload_dir)
        else:
            image = Image.open(upload_dir).convert('RGB')
            size = image.size

        os.remove(upload_dir)
        # RESIZE
        r_width, r_height = cls.resize(size)
        image = image.resize((r_width, r_height), Image.ANTIALIAS)
        # UPLOAD CONVERT IMAGE
        upload_dir = f'main/service/aws/temp/{filename}.jpeg'
        image.save(upload_dir, 'JPEG')

        # print("%.1f KB" % round(os.path.getsize(f'main/service/aws/temp/{filename}.jpeg') / 1024, 1))
        # RETURN CONVERT IMAGE
        return_info = {
            'size': os.path.getsize(f'main/service/aws/temp/{filename}.jpeg'),
        }
        return_file = open(upload_dir, 'rb').read()
        os.remove(upload_dir)
        return return_file, return_info

    @classmethod
    def convert_heif(cls, upload_dir):
        heif_image = pyheif.read(upload_dir)
        return Image.frombytes(
            heif_image.mode,
            heif_image.size,
            heif_image.data,
            'raw'
        ), heif_image.size

    @classmethod
    def resize(cls, size):
        global re_width, re_height

        w, h = size
        coeff_img = w / h
        if w >= 800:
            re_width = 800
            re_height = int(re_width / coeff_img)
        elif 800 >= w >= 400:
            re_width = 600
            re_height = int(re_width / coeff_img)
        elif w <= 400:
            re_width = 400
            re_height = int(re_width / coeff_img)

        return re_width, re_height

    @classmethod
    def crop_center(cls, pil_img, crop_width: int, crop_height: int):
        img_width, img_height = pil_img.size
        return pil_img.crop(((img_width - crop_width) // 2,
                             (img_height - crop_height) // 2,
                             (img_width + crop_width) // 2,
                             (img_height + crop_height) // 2))
