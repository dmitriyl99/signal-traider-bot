from fastapi import APIRouter, Depends

from app.data.db.statistics_repository import StatisticsRepository
from app.data.models.admin_users import AdminUser
from app.dependencies import get_statistics_repository, get_current_user
from .responses.dashboard import UsersStatisticsResponse


router = APIRouter(
    prefix='/dashboard',
    tags=['Dashboard']
)


@router.get('/users', response_model=UsersStatisticsResponse)
async def get_users_statistics(
    statistics_repository: StatisticsRepository = Depends(get_statistics_repository),
    current_user: AdminUser = Depends(get_current_user)
) -> UsersStatisticsResponse:
    all_users_count, new_users_count, growth_users_count = await statistics_repository.users_statistics()

    return UsersStatisticsResponse(
        all_users_count=all_users_count,
        new_users_count=new_users_count,
        growth_users_count=growth_users_count
    )
