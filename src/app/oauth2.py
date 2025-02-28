from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi import HTTPException, Depends, status

from app.models import TokenData


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login1")

SECRET_KEY = "bc714fc37a3e6f18aa8e3dbce9cb5c9bebf1c7b48fd338472d119d52967a583e"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 5


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, credentials_exception: HTTPException):
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
        user_id = payload.get("user_id")
        if user_id is None:
            raise credentials_exception

        token_data = TokenData(user_id=user_id)
        return token_data
    except JWTError:
        raise credentials_exception


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    return verify_access_token(token, credentials_exception)
