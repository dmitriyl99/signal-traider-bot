from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext

from app.data.models.admin_users import AdminUser


class UsersRepository:
    _session: AsyncSession

    def __init__(self, session: AsyncSession):
        self._session = session

    def _verify_password(self, plain_password: str, hashed_password: str) -> bool:
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return pwd_context.verify(plain_password, hashed_password)

    def _create_password(self, plain_password) -> str:
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return pwd_context.hash(plain_password)

    async def authenticate_user(self, username: str, password: str) -> AdminUser | None:
        result = await self._session.execute(select(AdminUser).filter(AdminUser.username == username))
        user = result.scalars().first()
        if user is None:
            return user
        if not self._verify_password(password, user.password):
            return None
        return user

    async def create_admin_user(self, username: str, password: str) -> AdminUser:
        result = await self._session.execute(select(AdminUser).filter(AdminUser.username == username))
        user = result.scalars().first()
        if user:
            return user
        user = AdminUser(
            username=username,
            password=self._create_password(password)
        )
        self._session.add(user)
        await self._session.commit()
        await self._session.refresh(user)
        return user
