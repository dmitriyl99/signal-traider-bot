from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.data.models.currency_pair import CurrencyPair


class CurrencyPairRepository:
    _session: AsyncSession

    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_currency_pairs(self) -> List[CurrencyPair]:
        stmt = select(CurrencyPair)
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def add_currency_pair(self, pair_name: str) -> CurrencyPair:
        currency_pair = CurrencyPair(pair=pair_name)
        self._session.add(currency_pair)
        await self._session.commit()
        await self._session.refresh(currency_pair)

        return currency_pair

    async def remove_currency_pair(self, currency_pair_id: int) -> None:
        currency_pair = await self._session.get(CurrencyPair, currency_pair_id)
        await self._session.delete(currency_pair)
