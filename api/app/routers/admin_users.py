from fastapi import APIRouter, Depends, HTTPException

from app.data.models.admin_users import AdminUser
from app.dependencies import get_current_user, get_admin_users_repository
from app.data.db.admin_users_repository import AdminUsersRepository

router = APIRouter(prefix='/admin-users', tags=['admin-users'])


@router.get('/')
async def list_admin_users(
    current_user: AdminUser = Depends(get_current_user),
    admin_users_repository: AdminUsersRepository = Depends(get_admin_users_repository)
):
    if not admin_users_repository.check_if_user_has_role(current_user, 'Admin'):
        raise HTTPException(
            status_code=401,
            detail='Unauthenticated'
        )
    return await admin_users_repository.get_all_admin_users()
