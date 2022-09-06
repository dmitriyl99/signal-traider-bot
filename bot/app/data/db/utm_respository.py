from typing import Optional

from sqlalchemy.future import select

from . import async_session
from app.data.models.utm import UtmCommandClick, UtmCommand


async def utm_click(utm_command_name: str, user_telegram_id: int):
    async with async_session() as session:
        stmt = select(UtmCommand).filter(UtmCommand.name == utm_command_name)
        result = await session.execute(stmt)
        utm_command: Optional[UtmCommand] = result.scalars().first()
        utm_command_click = UtmCommandClick(
            utm_command_name=utm_command_name,
            user_telegram_id=user_telegram_id
        )
        if utm_command is not None:
            utm_command_click.utm_command_id = utm_command.id
        session.add(utm_command_click)
        await session.commit()

