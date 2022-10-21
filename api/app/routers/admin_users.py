from fastapi import APIRouter, Depends, HTTPException, Body

from app.data.models.admin_users import AdminUser
from app.dependencies import get_current_user, get_admin_users_repository
from app.data.db.admin_users_repository import AdminUsersRepository
from app.routers.forms.admin_users import CreateAdminUserForm, ChangePasswordForm
from app.routers.responses.auth import User

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


@router.post('/')
async def create_admin_user(
        current_user: AdminUser = Depends(get_current_user),
        admin_users_repository: AdminUsersRepository = Depends(get_admin_users_repository),
        form: CreateAdminUserForm = Body()
):
    if not admin_users_repository.check_if_user_has_role(current_user, 'Admin'):
        raise HTTPException(
            status_code=401,
            detail='Unauthenticated'
        )
    if form.password != form.password_confirmation:
        raise HTTPException(
            status_code=422,
            detail='Wrong password confirmation'
        )
    created_user = await admin_users_repository.create_admin_user(
        form.username,
        form.password
    )

    return created_user


@router.get('/{admin_user_id}')
async def get_admin_user_by_id(
        admin_user_id: int,
        current_user: AdminUser = Depends(get_current_user),
        admin_users_repository: AdminUsersRepository = Depends(get_admin_users_repository),
):
    if not admin_users_repository.check_if_user_has_role(current_user, 'Admin'):
        raise HTTPException(
            status_code=401,
            detail='Unauthenticated'
        )

    user = admin_users_repository.get_admin_user_by_id(admin_user_id)
    return User(
        id=user.id,
        username=user.username,
        roles=user.roles,
        permissions=admin_users_repository.get_all_admin_user_permissions(user)
    )


@router.post('/{admin_user_id}/change-password')
def change_password(
        admin_user_id: int,
        current_user: AdminUser = Depends(get_current_user),
        admin_users_repository: AdminUsersRepository = Depends(get_admin_users_repository),
        form: ChangePasswordForm = Body()
):
    if not admin_users_repository.check_if_user_has_role(current_user, 'Admin'):
        raise HTTPException(
            status_code=401,
            detail='Unauthenticated'
        )
    if form.password != form.password_confirmation:
        raise HTTPException(
            status_code=422,
            detail='Wrong password confirmation'
        )

    admin_users_repository.change_password(admin_user_id, form.password)

    return {
        "detail": "Пароль изменён"
    }


@router.get('/roles')
def get_roles(
        current_user: AdminUser = Depends(get_current_user),
        admin_users_repository: AdminUsersRepository = Depends(get_admin_users_repository),
):
    if not admin_users_repository.check_if_user_has_role(current_user, 'Admin'):
        raise HTTPException(
            status_code=401,
            detail='Unauthenticated'
        )
    return admin_users_repository.get_roles()


@router.get('/permissions')
def get_permissions(
        current_user: AdminUser = Depends(get_current_user),
        admin_users_repository: AdminUsersRepository = Depends(get_admin_users_repository),
):
    if not admin_users_repository.check_if_user_has_role(current_user, 'Admin'):
        raise HTTPException(
            status_code=401,
            detail='Unauthenticated'
        )
    return admin_users_repository.get_permissions()
