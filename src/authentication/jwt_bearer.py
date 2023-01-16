from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from .auth import Auth
from config.error_messages import (
    INVALID_AUTHENTICATION_SCHEME,
    TOKEN_INVALID_OR_EXPIRED,
    INVALID_AUTHORIZATION_CODE,
)


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)
        self.auth = Auth()

    async def __call__(self, request: Request) -> str:
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail=INVALID_AUTHENTICATION_SCHEME)
            if not self.auth.decode_token(credentials.credentials):
                raise HTTPException(status_code=403, detail=TOKEN_INVALID_OR_EXPIRED)
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail=INVALID_AUTHORIZATION_CODE)
