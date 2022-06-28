from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.data.db.users_repository import UsersRepository
from app.data.db import get_session


def get_user_repository(session: AsyncSession = Depends(get_session)):
    return UsersRepository(session)
