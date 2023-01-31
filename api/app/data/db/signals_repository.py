from typing import List, Optional

from sqlalchemy import insert
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.data.models.admin_users import AdminUser
from app.data.models.signal import Signal, signal_chat_message_mapper_table, TextDistribution
from app.data.db import Session, sync_engine


class SignalsRepository:
    _session: AsyncSession

    def __init__(self, session: AsyncSession):
        self._session = session

    async def save_text_distribution(self, text: str, importance: int, admin_user: AdminUser):
        self._session.add(TextDistribution(
            text=text,
            admin_user_id=admin_user.id,
            importance=importance
        ))
        await self._session.commit()

    async def get_all_text_distributions(self) -> List[TextDistribution]:
        stmt = select(TextDistribution).options(joinedload(TextDistribution.admin_user))
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def save_signal(self,
                          currency_pair: str,
                          execution_method: str,
                          price: float,
                          admin_user_id: int,
                          tr_1: Optional[str],
                          tr_2: Optional[str],
                          sl: Optional[str]) -> Signal:
        signal = Signal(
            currency_pair=currency_pair,
            execution_method=execution_method,
            price=price,
            tr_1=tr_1,
            tr_2=tr_2,
            sl=sl,
            admin_user_id=admin_user_id
        )

        self._session.add(signal)
        await self._session.commit()
        await self._session.refresh(signal)

        return signal
    
    async def get_all_signals(self) -> List[Signal]:
        stmt = select(Signal)
        result = await self._session.execute(stmt)
        return result.scalars().all()

    def save_mapper_for_signal(self, signal: Signal, chat_message_mapper: dict):
        data = []
        for chat_id, message_id in chat_message_mapper.items():
            data.append({
                'signal_id': signal.id,
                'chat_id': chat_id,
                'message_id': message_id
            })
        with sync_engine.connect() as conn:
            conn.execute(insert(signal_chat_message_mapper_table), data)

    async def get_mapper_for_signal(self, signal_id: int):
        with Session() as session:
            stmt = select(signal_chat_message_mapper_table).where(signal_chat_message_mapper_table.c.signal_id == signal_id)
            return list(session.execute(stmt))
