import asyncio

import click

from app.data.db.admin_users_repository import AdminUsersRepository
from app.data.db import async_session


async def create_super_user():
    username = input('Username: ')
    password = input('Password: ')
    password_confirmation = input('Confirm password: ')
    if password != password_confirmation:
        click.echo('Password must be confirmed')
        return
    """Command to create admin user"""
    async with async_session() as session:
        repository = AdminUsersRepository(session)
        repository.create_admin_user(username, password, [1])
        click.echo('Admin user %s created!' % username)


if __name__ == '__main__':
    asyncio.run(create_super_user())

