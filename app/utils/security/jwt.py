from jose import jwt
from datetime import datetime, timedelta

from app.models.user import User
from app.settings import settings


ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 6 * 60


def create_token(user: User) -> str:
    to_encode = user.dict()
    to_encode.update({'exp', datetime.utcnow() +
                     timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)})
    return jwt.encode(to_encode, settings.jwt_secret, algorithm=ALGORITHM)