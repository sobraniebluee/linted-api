from passlib.hash import bcrypt
import socket
import json


def hash_password(password):
    password = bcrypt.hash(password)
    return password


def get_ip_addr():
    host_name = socket.gethostname()
    return socket.gethostbyname(host_name)


def _error_response(field, error):
    return {field: [error]}


