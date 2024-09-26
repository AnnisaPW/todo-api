from hashlib import pbkdf2_hmac
from app.config import Config
import os

import jwt


class Generator:

    @staticmethod
    def generate_salt():
        salt = os.urandom(16)
        return salt.hex()

    @staticmethod
    def generate_hash(plain_pass, salt_pass):
        password_hash = pbkdf2_hmac(
            "sha256",
            plain_pass.encode("utf-8"),  # Encode plain_pass directly
            bytes.fromhex(salt_pass),  # Convert hex string to bytes
            10000,
        )
        return password_hash.hex()

    @staticmethod
    def generate_jwt_token(content):
        encoded_content = jwt.encode(content, Config.JWT_SECRET_KEY, algorithm="HS256")
        token = str(encoded_content).split("'")[1]
        return token
