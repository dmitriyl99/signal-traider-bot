from fastapi import APIRouter, Depends

from app.dependencies import get_user_repository
from app.data.db.users_repository import UsersRepository

router = APIRouter(prefix='/users', tags=['Users'])


@router.get('/')
async def get_users_list(
        user_repository: UsersRepository = Depends(get_user_repository)
):
    users = await user_repository.get_all_users()
    return users
