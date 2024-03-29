from typing import List

from passlib.context import CryptContext

from . import BaseRepository, Session
from ..models.admin_users import AdminUser
from app.data.models.roles_and_permissions import Role, Permission
from sqlalchemy.future import select
from sqlalchemy.orm import subqueryload


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

    def create_admin_user(self, username: str, password: str, roles: List[int] = None) -> tuple[AdminUser, bool]:
        with Session() as session:
            user = session.query(AdminUser).filter(AdminUser.username == username).first()
            if user:
                return user
            user = AdminUser(
                username=username,
                password=self._create_password(password)
            )
            need_to_divide_users = False
            if roles is not None:
                for role_id in roles:
                    role_entity = session.query(Role).get(role_id)
                    if role_entity is None:
                        continue
                    user.roles.append(role_entity)
                    if role_entity.name == 'Analyst':
                        need_to_divide_users = True
                session.add(user)
                session.commit()
        return user, need_to_divide_users

    def delete_admin_user(self, admin_user_id):
        with Session() as session:
            user: AdminUser = session.query(AdminUser).get(admin_user_id)
            roles = user.roles
            for role in roles:
                user.roles.remove(role)
            permissions = user.permissions
            for permission in permissions:
                user.permissions.remove(permission)
            session.delete(user)
            session.commit()

    def get_admin_user_by_id(self, user_id: int) -> AdminUser:
        with Session() as session:
            return session.query(AdminUser). \
                options(subqueryload(AdminUser.roles), subqueryload(AdminUser.permissions)). \
                filter(AdminUser.id == user_id). \
                first()

    def get_admin_user_by_id_and_password(self, user_id: int, password: str) -> AdminUser:
        with Session() as session:
            return session.query(AdminUser). \
                options(subqueryload(AdminUser.roles), subqueryload(AdminUser.permissions)). \
                filter(AdminUser.id == user_id). \
                filter(AdminUser.password == password). \
                first()

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

    def get_all_admin_user_permissions(self, admin_user: AdminUser) -> List[Permission]:
        permissions_via_roles = []

        def mark_permission_from_role(role):
            def _(permission):
                permission.from_role = role.name
                return permission

            return _

        with Session() as session:
            admin_user = session.query(AdminUser).get(admin_user.id)
            direct_permissions = admin_user.permissions
            for role in admin_user.roles:
                permissions_via_roles += list(map(mark_permission_from_role(role), role.permissions))

        return direct_permissions + permissions_via_roles

    def get_admin_roles(self, admin_user: AdminUser) -> List[Role]:
        with Session() as session:
            admin_user = session.query(AdminUser).get(admin_user.id)
            return admin_user.roles

    def check_if_user_has_role(self, admin_user: AdminUser, role: str | int) -> bool:
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
        with Session() as session:
            admin_user: AdminUser = session.query(AdminUser).get(admin_user_id)
            admin_user.password = self._create_password(password)
            session.commit()

    def get_roles(self) -> List[Role]:
        with Session() as session:
            return session.query(Role).join(Role.permissions).all()

    def get_permissions(self) -> List[Permission]:
        with Session() as session:
            return session.query(Permission).all()
