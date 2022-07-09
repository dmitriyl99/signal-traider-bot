from typing import Tuple
from datetime import date
from dateutil import relativedelta

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func

from app.data.models.users import User


class StatisticsRepository:
    _session: AsyncSession

    def __init__(self, session: AsyncSession):
        self._session = session

    async def users_statistics(self) -> Tuple[int, int, int]:
        today = date.today()
        yesterday = today - relativedelta.relativedelta(days=1)

        all_users_count_stmt = select(func.count(User.id))
        all_users_count_result = await self._session.execute(all_users_count_stmt)
        all_users_count = all_users_count_result.scalars().one()

        new_users_count_stmt = select(func.count(User.id)).filter(func.date(User.created_at) == today)
        new_users_count_result = await self._session.execute(new_users_count_stmt)
        new_users_count = new_users_count_result.scalars().one()

        yesterday_users_count_stmt = select(func.count(User.id)).filter(func.date(User.created_at) == yesterday)
        yesterday_users_count_result = await self._session.execute(yesterday_users_count_stmt)
        yesterday_users_count = yesterday_users_count_result.scalars().one()
        users_growth_count = new_users_count - yesterday_users_count

        return all_users_count, new_users_count, users_growth_count
