from jose import jwt
from datetime import datetime, timedelta

from app.models.user import User
from app.settings import settings


ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 6 * 60


def create_token(user: User) -> str:
    to_encode = user.dict(exclude={'permissions'})

    to_encode.update({'exp': datetime.utcnow() +
                     timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)})
    to_encode['id'] = str(to_encode['id'])
    print(to_encode)
    return jwt.encode(to_encode, settings.jwt_secret, algorithm=ALGORITHM)


def validate_token(token: str) -> str:
    try:
        data = jwt.decode(token, settings.jwt_secret, algorithms=ALGORITHM)
        if data['exp'] < datetime.utcnow().timestamp():
            raise PermissionError
        return data['id']
    except:
        raise PermissionError
