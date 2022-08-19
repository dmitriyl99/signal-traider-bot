from fastapi import APIRouter, Depends, Body

from app.dependencies import get_user_repository, get_current_user
from app.data.db.users_repository import UsersRepository
from app.data.models.admin_users import AdminUser

from app.routers.forms.users import CreateUserForm

router = APIRouter(prefix='/users', tags=['Users'])


@router.get('/')
async def get_users_list(
        user_repository: UsersRepository = Depends(get_user_repository),
        current_user: AdminUser = Depends(get_current_user)
):
    users = await user_repository.get_all_users()
    return users


@router.post('/')
async def create_user(
        user_repository: UsersRepository = Depends(get_user_repository),
        form: CreateUserForm = Body(),
        current_user: AdminUser = Depends(get_current_user),
):
    user = await user_repository.create_user(
        form.name,
        form.phone,
        form.subscription_condition_id,
        form.subscription_id
    )

    return user
