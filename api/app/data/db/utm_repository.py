from typing import List, Optional

from sqlalchemy.orm import selectinload
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.data.models.utm import UtmCommand, UtmCommandClick


class UtmRepository:
    _session: AsyncSession

    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_all_utm_commands(self):
        stmt = select(UtmCommand)
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def get_utm_command_by_id(self, utm_command_id: int) -> Optional[UtmCommand]:
        stmt = select(UtmCommand).options(selectinload(UtmCommand.clicks)).filter(UtmCommand.id == utm_command_id)
        result = await self._session.execute(stmt)
        return result.scalars().first()

    async def create_utm_command(self, name: str) -> UtmCommand:
        utm_command = UtmCommand(name=name)
        self._session.add(utm_command)
        await self._session.commit()
        await self._session.refresh(utm_command)

        return utm_command

    async def delete_utm_command(self, utm_command_id: int):
        utm_command = await self._session.get(UtmCommand, utm_command_id)
        await self._session.delete(utm_command)
