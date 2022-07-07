from fastapi import APIRouter, Depends

from app.dependencies import get_user_repository, get_current_user
from app.data.db.users_repository import UsersRepository
from app.data.models.admin_users import AdminUser

router = APIRouter(prefix='/users', tags=['Users'])


@router.get('/')
async def get_users_list(
        user_repository: UsersRepository = Depends(get_user_repository),
        current_user: AdminUser = Depends(get_current_user)
):
    users = await user_repository.get_all_users()
    return users
