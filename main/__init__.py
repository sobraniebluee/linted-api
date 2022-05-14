from flask import Flask, jsonify
from config import Config
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from .db import session, create_metadata

app = Flask(__name__)
cors = CORS(app, resources={"*": {"origins": "*"}}, allow_headers=["Content-Type", "Authorization"])
JWTManager(app)
app.config.from_object(Config)

client = app.test_client()


@app.errorhandler(405)
def server_error(error):
    msg = str(error).split(':')[1].strip()
    return jsonify(message=str(msg))


@app.errorhandler(422)
def handler_error(err):
    headers = err.data.get('headers', None)

    messages = err.data.get('messages', ['Invalid request'])
    print(messages)
    if headers:
        return jsonify({'message': messages['json']}), 400, headers
    else:
        return jsonify({'message': messages['json']}), 400


@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()


from .api.Users.views import users

app.register_blueprint(users)

metadata = create_metadata()
