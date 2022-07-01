from typing import List

from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from app.data.models.payments import Payment


class PaymentsRepository:
    _session: AsyncSession

    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_all_payment(self) -> List[Payment]:
        stmt = select(Payment).options(joinedload(Payment.subscription), joinedload(Payment.subscription_condition))
        result = await self._session.execute(stmt)
        return result.scalars().all()
