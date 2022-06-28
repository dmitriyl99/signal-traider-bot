from datetime import timedelta, datetime

from fastapi import APIRouter, Depends, HTTPException, status

from jose import JWTError, jwt

from app.data.db.users_repository import UsersRepository
from app.dependencies import get_user_repository
from app.config import settings
from app.routers.forms.auth import LoginForm


router = APIRouter(prefix='/auth', tags=['auth'])


def _create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    return encoded_jwt


@router.post('/token')
async def token(
        form_data: LoginForm,
        user_repository: UsersRepository = Depends(get_user_repository)
):
    user = await user_repository.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    access_token_expires = timedelta(settings.jwt_ttl)
    access_token = _create_access_token(
        data={'sub': user.id},
        expires_delta=access_token_expires
    )

    return {'access_token': access_token, 'token_type': 'bearer'}
