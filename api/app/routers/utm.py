from fastapi import APIRouter, Depends, Body, HTTPException

from app.dependencies import get_current_user, get_utm_repository
from app.data.models.admin_users import AdminUser
from app.data.db.utm_repository import UtmRepository

from app.routers.forms.utm import CreateUtmCommand

router = APIRouter(prefix='/utm', tags=['UTM'])


@router.get('/commands')
async def get_utm_commands(
        utm_repository: UtmRepository = Depends(get_utm_repository),
        current_user: AdminUser = Depends(get_current_user),
):
    return await utm_repository.get_all_utm_commands()


@router.get('/commands/{utm_command_id}')
async def get_utm_command_by_id(
        utm_command_id: int,
        utm_repository: UtmRepository = Depends(get_utm_repository),
        current_user: AdminUser = Depends(get_current_user),
):
    utm_command = await utm_repository.get_utm_command_by_id(utm_command_id)
    if utm_command is None:
        raise HTTPException(
            detail=f'UTM command with id {utm_command_id} not found',
            status_code=404
        )

    return utm_command


@router.post('/commands')
async def store_utm_command(
        utm_repository: UtmRepository = Depends(get_utm_repository),
        current_user: AdminUser = Depends(get_current_user),
        form: CreateUtmCommand = Body()
):
    try:
        return await utm_repository.create_utm_command(form.name)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.delete('/commands/{utm_command_id}')
async def delete_utm_command(
        utm_command_id: int,
        utm_repository: UtmRepository = Depends(get_utm_repository),
        current_user: AdminUser = Depends(get_current_user)
):
    await utm_repository.delete_utm_command(utm_command_id)

    return {
        "detail": "UTM command deleted"
    }
