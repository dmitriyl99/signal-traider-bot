from fastapi import APIRouter, Depends

from app.dependencies import get_current_user, get_subscriptions_repository
from app.data.models.admin_users import AdminUser
from app.data.db.subscriptions_repository import SubscriptionsRepository


router = APIRouter(prefix='/subscriptions', tags=['Subscriptions'])


@router.get('/')
async def get_subscriptions_list(
        current_user: AdminUser = Depends(get_current_user),
        subscriptions_repository: SubscriptionsRepository = Depends(get_subscriptions_repository)
):
    subscriptions = await subscriptions_repository.get_subscriptions_list()

    return subscriptions
