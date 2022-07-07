from fastapi import APIRouter, Depends, Body

from app.dependencies import get_signals_repository, get_user_repository, get_current_user
from app.data.db.signals_repository import SignalsRepository
from app.data.db.users_repository import UsersRepository
from app.data.models.admin_users import AdminUser
from app.routers.forms.signals import CreateSignalForm
from app.services import bot


router = APIRouter(
    prefix='/signals'
)


@router.get('/')
async def get_all_signals(
        signals_repository: SignalsRepository = Depends(get_signals_repository),
        current_user: AdminUser = Depends(get_current_user)
):
    signals = await signals_repository.get_all_signals()
    return signals


@router.post('/')
async def create_signal(
        form: CreateSignalForm = Body(),
        signals_repository: SignalsRepository = Depends(get_signals_repository),
        users_repository: UsersRepository = Depends(get_user_repository),
        current_user: AdminUser = Depends(get_current_user)
):
    signal = await signals_repository.save_signal(
        form.currency_pair,
        form.execution_method,
        form.price,
        form.tr_1,
        form.tr_2,
        form.sl
    )
    await bot.send_distribution(signal, users_repository)
