import logging

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt, JWTError

from app.data.db.users_repository import UsersRepository
from app.data.db.payments_repository import PaymentsRepository
from app.data.db.signals_repository import SignalsRepository
from app.data.db import get_session
from app.data.models.admin_users import AdminUser
from app.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_user_repository(session: AsyncSession = Depends(get_session)):
    return UsersRepository(session)


def get_payments_repository(session: AsyncSession = Depends(get_session)):
    return PaymentsRepository(session)


def get_signals_repository(session: AsyncSession = Depends(get_session)):
    return SignalsRepository(session)


async def get_current_user(
        token: str = Depends(oauth2_scheme),
        user_repository: UsersRepository = Depends(get_user_repository)
) -> AdminUser:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        user_id: str = payload.get("sub")
        if user_id is None:
            logging.info("JWT doesn't have user id")
            raise credentials_exception
    except JWTError as e:
        logging.error('Error with jwt: ' + str(e))
        raise credentials_exception
    user = await user_repository.get_user_by_id(int(user_id))
    if user is None:
        logging.info('User with id %s not found' % user_id)
        raise credentials_exception
    return user
