from typing import List, Optional

from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from app.data.models.payments import Payment, PaymentStatus


class PaymentsRepository:
    _session: AsyncSession

    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_all_payment(self) -> List[Payment]:
        stmt = select(Payment).options(joinedload(Payment.subscription), joinedload(Payment.subscription_condition))
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def get_payment_by_order_id(self, order_id) -> Optional[Payment]:
        stmt = select(Payment).filter(Payment.order_id == order_id)
        result = await self._session.execute(stmt)
        return result.scalars().first()

    async def set_status_for_payment_by_order_id(self, order_id, status):
        payment = await self.get_payment_by_order_id(order_id)
        payment.status = status
        await self._session.commit()

    async def complete_payment(self, order_id, payment_provider):
        payment = await self.get_payment_by_order_id(order_id)
        payment.status = PaymentStatus.CONFIRMED
        payment.provider = payment_provider
        await self._session.commit()
