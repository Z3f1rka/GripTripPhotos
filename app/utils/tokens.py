from typing import Annotated

from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt

from app.core import settings

secured = OAuth2PasswordBearer(tokenUrl=f"{settings.MAIN_API}/auth/docs/login")


def get_jwt_payload(token: Annotated[str, Depends(secured)]) -> dict | str:
    """
    This function decodes token
    if token invalid :return: name of error
    else :return: payload(json)
    :param token: str
    """
    try:
        decoded = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.ENCRYPT_ALG])
        return decoded
    except jwt.ExpiredSignatureError:
        raise HTTPException(401, "Bearer token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(401, "Invalid bearer token")
