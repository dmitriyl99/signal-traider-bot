from typing import List

from passlib.context import CryptContext

from . import BaseRepository, sync_engine
from ..models.admin_users import AdminUser
from app.data.models.roles_and_permissions import Role, Permission
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select


class AdminUsersRepository(BaseRepository):
    def _verify_password(self, plain_password: str, hashed_password: str) -> bool:
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return pwd_context.verify(plain_password, hashed_password)

    def _create_password(self, plain_password) -> str:
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return pwd_context.hash(plain_password)

    async def get_all_admin_users(self) -> List[AdminUser]:
        result = await self._session.execute(select(AdminUser))
        return result.scalars().all()

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

    def get_admin_user_by_id(self, user_id: int) -> AdminUser:
        Session = sessionmaker(sync_engine)
        with Session() as session:
            return session.query(AdminUser).get(user_id)

    async def add_role_to_admin_user(self, admin_user_id: int, role: str | int):
        if role is str:
            query = select(Role).filter(Role.name == role)
            role_model: Role = (await self._session.execute(query)).scalars().first()
        elif role is int:
            role_model: Role = (await self._session.get(Role, role))
        else:
            raise ValueError(f"Unexpected type of role: {type(role)}")

        admin_user = self.get_admin_user_by_id(admin_user_id)
        if admin_user is None:
            raise Exception("Admin user not found")
        admin_user.roles += [role_model]
        await self._session.commit()

    async def get_all_admin_user_permissions(self, admin_user: AdminUser) -> List[Permission]:
        Session = sessionmaker(sync_engine)
        permissions_via_roles = []
        with Session() as session:
            admin_user = session.query(AdminUser).get(admin_user.id)
            direct_permissions = admin_user.permissions
            for role in admin_user.roles:
                permissions_via_roles += role.permissions

        return direct_permissions + permissions_via_roles

    def get_admin_roles(self, admin_user: AdminUser) -> List[Role]:
        Session = sessionmaker(sync_engine)
        with Session() as session:
            admin_user = session.query(AdminUser).get(admin_user.id)
            return admin_user.roles

    def check_if_user_has_role(self, admin_user: AdminUser, role: str | int) -> bool:
        Session = sessionmaker(sync_engine)
        with Session() as session:
            admin_user = session.query(AdminUser).get(admin_user.id)
            if type(role) is int:
                role_entity = session.query(Role).get(role)
            else:
                role_entity = session.query(Role).filter(Role.name == role).first()
            if role_entity is None:
                raise Exception(f"Role {role} not found")
            admin_users_role_names = list(map(lambda x: x.name, admin_user.roles))
            if role_entity.name not in admin_users_role_names:
                return False
            return True

    def change_password(self, admin_user_id: int, password: str):
        Session = sessionmaker(sync_engine)
        with Session() as session:
            admin_user: AdminUser = session.query(AdminUser).get(admin_user_id)
            admin_user.password = self._create_password(password)
            session.commit()

