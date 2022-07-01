from fastapi import APIRouter, Depends

from app.data.db.payments_repository import PaymentsRepository
from app.dependencies import get_payments_repository

router = APIRouter(prefix='/payments', tags=['Payments'])


@router.get('/')
async def get_payments_list(
        payment_repository: PaymentsRepository = Depends(get_payments_repository)
):
    return await payment_repository.get_all_payment()
