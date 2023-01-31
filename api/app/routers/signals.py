from fastapi import APIRouter, Depends, Body, HTTPException, UploadFile, Form, BackgroundTasks, status

from app.dependencies import get_signals_repository, get_user_repository, get_current_user
from app.data.db.signals_repository import SignalsRepository
from app.data.db.users_repository import UsersRepository
from app.data.models.admin_users import AdminUser
from app.helpers import array
from app.routers.forms.signals import CreateSignalForm, ReplySignalForm
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
        background_tasks: BackgroundTasks,
        form: CreateSignalForm = Body(),
        signals_repository: SignalsRepository = Depends(get_signals_repository),
        users_repository: UsersRepository = Depends(get_user_repository),
        current_user: AdminUser = Depends(get_current_user),
):
    signal = await signals_repository.save_signal(
        form.currency_pair,
        form.execution_method,
        form.price,
        current_user.id,
        form.tr_1,
        form.tr_2,
        form.sl
    )
    background_tasks.add_task(bot.send_distribution, signal, users_repository, signals_repository, current_user)
    return {
        'details': 'Signal added to background tasks'
    }


@router.post('/{signal_id}/reply')
async def reply_to_signal_message(
        signal_id: int,
        background_tasks: BackgroundTasks,
        form: ReplySignalForm = Body(),
        signals_repository: SignalsRepository = Depends(get_signals_repository),
):
    async def send_reply_distribution(mapper):
        mapper_chunks = array.chunks(mapper, 50)
        for chunk in mapper_chunks:
            for mapper in chunk:
                telegram_user_id = mapper[1]
                reply_to_message_id = mapper[2]
                await bot.send_message_to_user(telegram_user_id, form.text, reply_to_message_id=reply_to_message_id)
    signal_mapper = await signals_repository.get_mapper_for_signal(signal_id)
    background_tasks.add_task(send_reply_distribution, signal_mapper)
    return {
        'details': 'Reply messages added to background tasks'
    }


@router.post('/message')
async def send_signal_message(
        text: str = Form(),
        importance: int = Form(),
        files: list[UploadFile] | None = None,
        images: list[UploadFile] | None = None,
        users_repository: UsersRepository = Depends(get_user_repository),
        signals_repository: SignalsRepository = Depends(get_signals_repository),
        current_user: AdminUser = Depends(get_current_user)
):
    attachments = []
    if images is not None and files is not None:
        raise HTTPException(
            status_code=400,
            detail='Telegram не позволяет отправлять документы и изображения одновременно'
        )
    if images is not None:
        for i in images:
            if not i.content_type.startswith('image/') or not i.content_type.startswith('video/'):
                raise HTTPException(
                    status_code=400,
                    detail='Если хотите отправить файлы, не пользуйтесь полем для изображений'
                )
        attachments += [{'binary': f.file, 'type': f.content_type, 'filename': f.filename, 'is_image': True} for f in images]
    if files is not None:
        attachments += [{'binary': f.file, 'type': f.content_type, 'filename': f.filename, 'is_image': False} for f in files]
    await bot.send_text_distribution(
        text,
        attachments,
        users_repository,
        current_user,
        importance=importance
    )
    await signals_repository.save_text_distribution(text, importance, current_user)


@router.get('/message')
async def get_signal_messages(
        current_user: AdminUser = Depends(get_current_user),
        signals_repository: SignalsRepository = Depends(get_signals_repository),
):
    if len(list(filter(lambda x: x.name == 'Admin', current_user.roles))) > 0:
        distributions = await signals_repository.get_all_text_distributions()
        return list(
            map(
                lambda x: {
                    'text': x.text,
                    'admin_user': x.admin_user.username if x.admin_user else None,
                    'created_at': x.created_at
                }, distributions
            )
        )
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail='You do not have permission'
    )


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
