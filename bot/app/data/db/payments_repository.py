from . import async_session

from sqlalchemy.future import select

from app.data.models.payments import Payment


async def save_payment(
        amount: int,
        provider: str,
        user_id: int,
        subscription_id: int,
        subscription_condition_id: int
) -> Payment:
    payment = Payment(
        amount=amount,
        provider=provider,
        user_id=user_id,
        subscription_id=subscription_id,
        subscription_condition_id=subscription_condition_id
    )
    async with async_session() as session:
        session.add(payment)
        await session.commit()
        await session.refresh(payment)
        return payment


async def set_clouds_payments_transaction_id(
        payment_id: int,
        transaction_id: str
):
    async with async_session() as session:
        payment = session.get(Payment, payment_id)
        payment.cloud_payments_transaction_id = transaction_id
        await session.commit()


async def set_status(
        payment_id: int,
        status
):
    async with async_session() as session:
        payment = session.get(Payment, payment_id)
        payment.status = status
        await session.commit()
