import os
import binascii
from werkzeug.security import generate_password_hash, check_password_hash


def create_random_id():
    return binascii.hexlify(os.urandom(16))


def create_password_hash(password):
    return generate_password_hash(password, method='sha256')


def check_password(password_hash, password):
    return check_password_hash(password_hash, password)
