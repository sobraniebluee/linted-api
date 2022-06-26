from flask import Blueprint, request
from flask_apispec import use_kwargs, marshal_with
from flask_jwt_extended import jwt_required, get_jwt_identity
from main.service.file_service import upload_advert_image
from main.schemas.file_schema import FileSchema
from main import docs

files = Blueprint('files', __name__)


@files.route('/advert', methods=['POST'])
@jwt_required()
@marshal_with(FileSchema)
def upload_advert_photo():
    image = request.files.get('image')
    identity = get_jwt_identity()
    return upload_advert_image(id_user=identity, image=image)


docs.register(upload_advert_photo, blueprint='files')


