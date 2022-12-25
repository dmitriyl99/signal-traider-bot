from fastapi import APIRouter, Depends, Body, HTTPException, status

from app.config import settings
from app.dependencies import get_user_repository, get_current_user, get_subscriptions_repository
from app.data.db.users_repository import UsersRepository
from app.data.db.subscriptions_repository import SubscriptionsRepository
from app.data.models.admin_users import AdminUser

from app.services import bot

from app.routers.forms.users import CreateUserForm, UpdateUserForm

router = APIRouter(prefix='/users', tags=['Users'])


@router.get('/')
async def get_users_list(
        user_repository: UsersRepository = Depends(get_user_repository),
        current_user: AdminUser = Depends(get_current_user),
        page: int = 1,
        search: str = None
):
    if len(list(filter(lambda x: x.name == 'Analyst', current_user.roles))) > 0:
        users = await user_repository.get_all_users(current_user.id, page=page, search=search)
    else:
        users = await user_repository.get_all_users(page=page, search=search)
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
    user_repository.divide_users_between_analytics()
    if form.subscription_id and (form.subscription_condition_id or form.subscription_duration_in_days):
        await subscription_repository.add_subscription_to_user(
            user,
            form.subscription_id,
            form.subscription_duration_in_days,
            form.subscription_condition_id,
            proactively_added=True,
            active=True
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
        subscription_repository: SubscriptionsRepository = Depends(get_subscriptions_repository),
        form: UpdateUserForm = Body()
):
    user = await user_repository.update_user(
        user_id,
        form.name,
        form.phone
    )
    if user is None:
        raise HTTPException(
            status_code=404,
            detail='User not found'
        )
    if form.subscription_id and (form.subscription_condition_id or form.subscription_duration_in_days):
        user_subscription = await subscription_repository.add_subscription_to_user(
            user,
            form.subscription_id,
            form.subscription_duration_in_days,
            form.subscription_condition_id,
            proactively_added=False,
            active=True
        )
        if user.telegram_user_id:
            await bot.send_message_to_user(user.telegram_user_id, f'Вам добавлена подписка на {user_subscription.duration_in_days} дней!')
            if settings.telegram_group_id:
                await bot.add_user_to_group(settings.telegram_group_id, user.telegram_user_id)

    return user


@router.delete('/{user_id}')
async def delete_user(
        user_id: int,
        user_repository: UsersRepository = Depends(get_user_repository),
        subscription_repository: SubscriptionsRepository = Depends(get_subscriptions_repository),
        current_user: AdminUser = Depends(get_current_user),
):
    await subscription_repository.delete_subscription_from_user(user_id)
    deleted = await user_repository.delete_user(user_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )
    return {
        'detail': 'User deleted!'
    }
