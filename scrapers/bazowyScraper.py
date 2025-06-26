from abc import ABC, abstractmethod
import asyncio
import aiohttp
import random

from typing import List, Dict


class bazowyScraper(ABC):
    @abstractmethod
    async def szukaj(self, adres: str) -> List[Dict]:
        pass

    async def pobierz_strone(self, sesja: aiohttp.ClientSession, adres: str) -> str:
        await asyncio.sleep(random.uniform(1, 2))
        async with sesja.get(adres) as odpowiedz:
            odpowiedz.raise_for_status()
            return await odpowiedz.text()

