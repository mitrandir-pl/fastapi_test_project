import os
import datetime
from passlib.context import CryptContext

import jwt
from fastapi import HTTPException

from config.error_messages import (
    TOKEN_EXPIRED_MESSAGE,
    INVALID_TOKEN_MESSAGE
)


JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
JWT_ALGORITHM = os.environ.get('JWT_ALGORITHM')


class Auth:
    hasher = CryptContext(schemes=['bcrypt'])
    secret = os.environ.get('JWT_SECRET_KEY')
    algorithm = os.environ.get('JWT_ALGORITHM')

    def encode_password(self, password: str) -> str:
        """Encoding user's password."""
        return self.hasher.hash(password)

    def verify_password(self, password: str, encoded_password: str) -> bool:
        """Verifies user's password."""
        return self.hasher.verify(password, encoded_password)

    def generate_access_token(self, user_id: int) -> str:
        """Generates access token by user's id"""
        access_token_payload = {
            'user_id': user_id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=5),
            'iat': datetime.datetime.utcnow(),
        }
        access_token = jwt.encode(access_token_payload,
                                  self.secret,
                                  algorithm=self.algorithm)
        return access_token

    def generate_refresh_token(self, user_id: int) -> str:
        """Generates refresh token by user's id"""
        refresh_token_payload = {
            'user_id': user_id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
            'iat': datetime.datetime.utcnow()
        }
        refresh_token = jwt.encode(
            refresh_token_payload, self.secret, algorithm=self.algorithm
        )
        return refresh_token

    def decode_token(self, token: str) -> dict[str: str]:
        """Decoding access token and returns payload"""
        try:
            payload = jwt.decode(token, self.secret, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail=TOKEN_EXPIRED_MESSAGE)
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail=INVALID_TOKEN_MESSAGE)
        return payload
