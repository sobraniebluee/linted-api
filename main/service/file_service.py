from main.models.File.file_model import File
from config import Config
from main.service.Aws.upload_aws import UploadAws
from main.middleware.error import Error
from uuid import uuid4


def upload_advert_image(id_user, image):
    response_status, response_info = True, ('file', 2344)
    if not response_status:
        return Error.server_error(response_info)
    path, size = response_info
    try:
        new_file = File(id_user=id_user, type_file='Advert', path=path, size=size)
        new_file.save()
    except Exception as e:
        return Error.server_error(e)

    return new_file, 200


