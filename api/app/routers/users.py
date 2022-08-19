from fastapi import APIRouter, Depends, Body

from app.dependencies import get_user_repository, get_current_user, get_subscriptions_repository
from app.data.db.users_repository import UsersRepository
from app.data.db.subscriptions_repository import SubscriptionsRepository
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
