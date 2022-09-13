from fastapi import APIRouter, Depends, Body, HTTPException, UploadFile, Form

from app.dependencies import get_signals_repository, get_user_repository, get_current_user
from app.data.db.signals_repository import SignalsRepository
from app.data.db.users_repository import UsersRepository
from app.data.models.admin_users import AdminUser
from app.routers.forms.signals import CreateSignalForm, SignalMessageForm
from app.services import bot, trading_view


router = APIRouter(
    prefix='/signals',
    tags=['Signals']
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


@router.post('/message')
async def send_signal_message(
        text: str = Form(default="hello"),
        files: list[UploadFile] | None = None,
        users_repository: UsersRepository = Depends(get_user_repository),
        current_user: AdminUser = Depends(get_current_user)
):
    if files is not None:
        await bot.send_text_distribution(text, [f.file for f in files], users_repository)
    else:
        await bot.send_text_distribution(text, None, users_repository)


@router.get('/suggestion')
async def get_currency_suggestion(
    current_user: AdminUser = Depends(get_current_user),
    currency_pair: str | None = None
):
    if currency_pair is None:
        raise HTTPException(
            status_code=400,
            detail="Please, choose currency pair"
        )

    trading_view_response: trading_view.TradingViewScanResponse | None = trading_view.trading_view_scan(currency_pair)
    if trading_view_response is None:
        raise HTTPException(
            status_code=404,
            detail=f'Currency pair {currency_pair} not found in tradingview.com'
        )

    return trading_view_response
