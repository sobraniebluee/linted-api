from passlib.hash import bcrypt
import socket


def hash_password(password):
    password = bcrypt.hash(password)
    return password


def get_ip_addr():
    host_name = socket.gethostname()
    return socket.gethostbyname(host_name)


def _error_response(field, error):
    return {field: error}


def _except(session):
    def decorate(func):
        def wrapper(self,*args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except Exception as e:
                session.rollback()
                raise e
        return wrapper
    return decorate


data = {"password": ["Missing data for required field."]}


def repr_msg_errors(msg):
    for item in msg:
        error_text = msg[item][0]
        msg[item] = error_text
    return msg

# repr_msg_errors(data)
