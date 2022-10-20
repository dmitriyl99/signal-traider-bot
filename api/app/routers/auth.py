from datetime import timedelta, datetime

from fastapi import APIRouter, Depends, HTTPException, status

from jose import JWTError, jwt

from app.data.models.admin_users import AdminUser
from app.dependencies import get_current_user, get_admin_users_repository
from app.config import settings

from .forms.auth import LoginForm
from .responses.auth import Token, User
from ..data.db.admin_users_repository import AdminUsersRepository

router = APIRouter(prefix='/auth', tags=['Auth'])


def _create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    return encoded_jwt


@router.post('/token', response_model=Token)
async def token(
        form_data: LoginForm,
        user_repository: AdminUsersRepository = Depends(get_admin_users_repository)
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
        data={'sub': str(user.id)},
        expires_delta=access_token_expires
    )

    return {'access_token': access_token, 'token_type': 'bearer'}


@router.get('/me', response_model=User)
async def get_me(current_user: AdminUser = Depends(get_current_user)):
    return User(
        id=current_user.id,
        username=current_user.username,
    )


@router.get('/me/permissions')
async def get_current_user_permissions(
        admin_users_repository: AdminUsersRepository = Depends(get_admin_users_repository),
        current_user: AdminUser = Depends(get_current_user)
):
    return await admin_users_repository.get_all_admin_user_permissions(current_user)
