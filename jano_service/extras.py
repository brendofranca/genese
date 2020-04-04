import os
import binascii
from flask_bcrypt import generate_password_hash, check_password_hash


def create_hash_id():
    hash_id = binascii.hexlify(os.urandom(16))
    id_encrypted = generate_password_hash(hash_id)
    return id_encrypted


def create_hash_pwd(password):
    password_encrypted = generate_password_hash(password)
    return password_encrypted
