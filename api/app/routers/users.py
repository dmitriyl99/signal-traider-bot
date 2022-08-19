from fastapi import APIRouter, Depends, Body, HTTPException

from app.dependencies import get_user_repository, get_current_user, get_subscriptions_repository
from app.data.db.users_repository import UsersRepository
from app.data.db.subscriptions_repository import SubscriptionsRepository
from app.data.models.admin_users import AdminUser

from app.routers.forms.users import CreateUserForm, UpdateUserForm

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
        subscription_repository: SubscriptionsRepository = Depends(get_subscriptions_repository),
        form: CreateUserForm = Body(),
        current_user: AdminUser = Depends(get_current_user),
):
    user = await user_repository.create_user(
        form.name,
        form.phone,
    )
    await subscription_repository.add_subscription_to_user(
        user,
        form.subscription_id,
        form.subscription_condition_id,
        proactively_added=True
    )

    return user


@router.get('/{user_id}')
async def get_user_by_id(
        user_id: int,
        user_repository: UsersRepository = Depends(get_user_repository),
        current_user: AdminUser = Depends(get_current_user),
):
    user = await user_repository.get_user_by_id(user_id)

    return user


@router.put('/{user_id}')
async def update_user(
        user_id: int,
        user_repository: UsersRepository = Depends(get_user_repository),
        form: UpdateUserForm = Body()
):
    user = await user_repository.update_user(
        user_id,
        form.name,
        form.phone,
        form.subscription_id,
        form.subscription_condition_id
    )
    if user is None:
        raise HTTPException(
            status_code=404,
            detail='User not found'
        )

    return user
