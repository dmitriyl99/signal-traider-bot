from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.data.models.signal import Signal


class SignalsRepository:
    _session: AsyncSession

    def __init__(self, session: AsyncSession):
        self._session = session

    async def save_signal(self,
                          currency_pair: str,
                          execution_method: str,
                          price: int,
                          tr_1: str,
                          tr_2: str,
                          sl: str) -> Signal:
        signal = Signal(
            currency_pair=currency_pair,
            execution_method=execution_method,
            price=price,
            tr_1=tr_1,
            tr_2=tr_2,
            sl=sl
        )

        self._session.add(signal)
        await self._session.commit()
        await self._session.refresh(signal)

        return signal
    
    async def get_all_signals(self) -> List[Signal]:
        stmt = select(Signal)
        result = await self._session.execute(stmt)
        return result.scalars().all()
