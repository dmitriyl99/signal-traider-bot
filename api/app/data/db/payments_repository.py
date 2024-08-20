from asyncpg.exceptions import DataError
from typing import List, Optional
from datetime import datetime

from sqlalchemy import func
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from app.data.models.payments import Payment
from app.data.models.subscription import SubscriptionCondition


class PaymentsRepository:
    _session: AsyncSession

    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_all_payment(
            self,
            filter_sum: int | None = None,
            filter_provider: str | None = None,
            filter_status: str | None = None,
            filter_duration: int | None = None,
            filter_date_from: str | None = None,
            filter_date_to: str | None = None
    ) -> List[Payment]:
        stmt = select(Payment).options(joinedload(Payment.subscription), joinedload(Payment.subscription_condition))\
            .order_by(Payment.created_at.desc())
        if filter_sum:
            stmt = stmt.filter(Payment.amount == filter_sum)
        if filter_provider:
            stmt = stmt.filter(Payment.provider == filter_provider)
        if filter_status:
            stmt = stmt.filter(Payment.status == filter_status)
        if filter_duration:
            stmt = stmt.filter(SubscriptionCondition.duration_in_month == filter_duration)
        if filter_date_from and filter_date_to:
            stmt = stmt.filter(Payment.created_at.between(func.date(filter_date_from), func.date(filter_date_to)))
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def get_payment_by_id(self, payment_id) -> Optional[Payment]:
        try:
            return await self._session.get(Payment, payment_id)
        except Exception:
            return None

    async def set_payment_status(self, payment_id, status):
        payment = await self.get_payment_by_id(payment_id)
        payment.status = status
        await self._session.commit()

    async def get_payment_by_clouds_payment_transaction_id(self, transaction_id) -> Payment:
        stmt = select(Payment).filter(Payment.cloud_payments_transaction_id == transaction_id)
        result = await self._session.execute(stmt)
        payment = result.scalars().first()
        return payment
