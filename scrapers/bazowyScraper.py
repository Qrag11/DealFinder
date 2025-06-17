from abc import ABC, abstractmethod
import asyncio
import aiohttp
import random
import sqlite3
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

    def zapisz_oferte(self, oferta: dict):
        conn = sqlite3.connect("data/oferty.db")
        cursor = conn.cursor()
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS oferty (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tytul TEXT,
                    cena INTEGER,
                    url TEXT UNIQUE,
                    data_dodania TEXT,
                    serwis TEXT,
                    zdjecie_url TEXT
                )
            """)
            cursor.execute("""
                INSERT OR IGNORE INTO oferty (tytul, cena, url, data_dodania, serwis, zdjecie_url)
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(url) DO UPDATE SET
                    cena=excluded.cena,
                    data_dodania=excluded.data_dodania
            """, (
                oferta["tytul"],
                oferta["cena"],
                oferta["url"],
                oferta["data_dodania"],
                oferta["serwis"],
                oferta["zdjecie_url"]
            ))
            conn.commit()
        finally:
            conn.close()