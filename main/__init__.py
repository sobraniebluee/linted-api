from flask import Flask, jsonify
from config import Config
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from .db import session, create_metadata
from .utils import repr_msg_errors
from .service.token_service import is_revoked_token_service
from apispec import APISpec
from flask_apispec import FlaskApiSpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin

app = Flask(__name__)
cors = CORS(app, resources={"*": {"origins": "*"}}, supports_credentials=True, allow_headers=["Content-Type", "Authorization"])
jwt = JWTManager(app)
app.config.from_object(Config)

client = app.test_client()

app.config.update({
    'APISPEC_SPEC': APISpec(
        title='Linted',
        version='v.1.0',
        plugins=[FlaskPlugin(), MarshmallowPlugin()],
        openapi_version="2.0"
    ),
    'APISPEC_SWAGGER_URL': '/swagger/',
})
docs = FlaskApiSpec(app)


@app.errorhandler(405)
def server_error(error):
    msg = str(error).split(':')[1].strip()
    return jsonify(message=str(msg))


@app.errorhandler(422)
def handler_error(err):
    headers = err.data.get('headers', None)
    messages = err.data.get('messages', ['Invalid request'])
    if headers:
        return jsonify({'message': repr_msg_errors(messages['json'])}), 400, headers
    else:
        return jsonify({'message': repr_msg_errors(messages['json'])}), 400


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

app.register_blueprint(users, url_prefix=f"/{app.config['ROOT_API_PATH']}/user")
app.register_blueprint(profile, url_prefix=f"/{app.config['ROOT_API_PATH']}/profile")
app.register_blueprint(adverts, url_prefix=f"/{app.config['ROOT_API_PATH']}/adverts")

metadata = create_metadata()
