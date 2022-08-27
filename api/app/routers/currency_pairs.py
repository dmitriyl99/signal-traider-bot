from fastapi import APIRouter, Depends, Body

from app.dependencies import get_currency_pair_repository, get_current_user
from app.data.db.currency_pair_repository import CurrencyPairRepository
from app.data.models.admin_users import AdminUser
from .forms.currency_pairs import SaveCurrencyPairForm


router = APIRouter(prefix='/currency-pairs', tags=['currency-pairs'])


@router.get('/')
async def list_currency_pairs(
        currency_pair_repository: CurrencyPairRepository = Depends(get_currency_pair_repository),
        current_user: AdminUser = Depends(get_current_user)
):
    return await currency_pair_repository.get_currency_pairs()


@router.post('/')
async def add_currency_pair(
        currency_pair_repository: CurrencyPairRepository = Depends(get_currency_pair_repository),
        current_user: AdminUser = Depends(get_current_user),
        form: SaveCurrencyPairForm = Body()
):
    return await currency_pair_repository.add_currency_pair(form.pair_name)


@router.delete('/{currency_pair_id}')
async def delete_currency_pair(
        currency_pair_id: int,
        currency_pair_repository: CurrencyPairRepository = Depends(get_currency_pair_repository),
        current_user: AdminUser = Depends(get_current_user),
):
    await currency_pair_repository.remove_currency_pair(currency_pair_id)

    return {
        'message': 'Deleted'
    }
