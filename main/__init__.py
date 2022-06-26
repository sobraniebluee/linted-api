from flask import Flask, jsonify, send_from_directory
from config import Config, Const
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from .db import session, create_metadata
from .utils import repr_msg_errors
# from helpers.help import upload_data_to_table_condition
from .service.token_service import is_revoked_token_service
from apispec import APISpec
from flask_apispec import FlaskApiSpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask_swagger_ui import get_swaggerui_blueprint


app = Flask(__name__)
app.config.from_object(Config)
cors = CORS(resources={"*": {"origins": "*"}}, supports_credentials=True, allow_headers=["Content-Type", "Authorization"])
jwt = JWTManager()
docs = FlaskApiSpec()
app.config.update({
    'APISPEC_SPEC': APISpec(
        title='Linted',
        version='2.0',
        plugins=[FlaskPlugin(), MarshmallowPlugin()],
        openapi_version="3.0.0"
    )
})

SWAGGER_URL = '/docs'
API_URL = '/static/docs'
swagger_ui_blueprint = get_swaggerui_blueprint(
   SWAGGER_URL,
   API_URL,
   config={
       'app_name': 'My App'
   }
)


@app.route('/static/docs')
def swagger_json():
    return jsonify(app.config.get('APISPEC_SPEC').to_dict())


@app.errorhandler(404)
def not_found_error(error):
    msg = 'The requested URL was not found on the server.'
    return jsonify(message=msg)


@app.errorhandler(405)
def server_error(error):
    msg = str(error).split(':')[1].strip()
    return jsonify(message=str(msg))


@app.errorhandler(422)
def handler_error(err):
    headers = err.data.get('headers', None)
    messages = err.data.get('messages', ['Invalid request'])
    if messages.get('json', None) is not None:
        if headers:
            return jsonify({'message': repr_msg_errors(messages['json'])}), 400, headers
        else:
            return jsonify({'message': repr_msg_errors(messages['json'])}), 400

    return jsonify({'msg': messages})


@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    identity = jwt_payload['sub']
    return is_revoked_token_service(identity=identity, jwt_header=jwt_header, jwt_payload=jwt_payload)


from .api.Auth.views import users
from .api.AuthProfile.views import profile
from .api.Advert.views import adverts
from .api.Category.views import categories
from .api.Size.views import sizes
from .api.File.views import files
from .api.Offer.views import offers
from .api.Transaction.views import transaction
from .api.Member.views import members
from .api.Review.views import reviews
from .api.Notification.views import notifications
from .api.Review.views import add_review

app.register_blueprint(users, url_prefix=f"{Const.ROOT_API_PATH}/user")
app.register_blueprint(profile, url_prefix=f"{Const.ROOT_API_PATH}/profile")
app.register_blueprint(adverts, url_prefix=f"{Const.ROOT_API_PATH}/adverts")
app.register_blueprint(categories, url_prefix=f"{Const.ROOT_API_PATH}/categories")
app.register_blueprint(sizes, url_prefix=f"{Const.ROOT_API_PATH}/sizes")
app.register_blueprint(files, url_prefix=f"{Const.ROOT_API_PATH}/files")
app.register_blueprint(offers, url_prefix=f"{Const.ROOT_API_PATH}/offers")
app.register_blueprint(transaction, url_prefix=f"{Const.ROOT_API_PATH}/transactions")
app.register_blueprint(members, url_prefix=f"{Const.ROOT_API_PATH}/members")
app.register_blueprint(reviews, url_prefix=f"{Const.ROOT_API_PATH}/reviews")
app.register_blueprint(notifications, url_prefix=f"{Const.ROOT_API_PATH}/notifications")
app.register_blueprint(swagger_ui_blueprint)

with app.app_context():
    docs.init_app(app)
cors.init_app(app)
jwt.init_app(app)

metadata = create_metadata()
