from . import async_session

from app.data.models.payments import Payment


async def save_payment(
        amount: int,
        user_id: int,
        subscription_id: int,
        subscription_condition_id: int
) -> Payment:
    payment = Payment(
        amount = amount,
        user_id=user_id,
        subscription_id=subscription_id,
        subscription_condition_id=subscription_condition_id
    )
    async with async_session() as session:
        session.add(payment)
        await session.commit()
        await session.refresh(payment)
        return payment
