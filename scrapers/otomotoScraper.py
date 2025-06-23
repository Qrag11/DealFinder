import asyncio
from datetime import datetime, timedelta
import aiohttp
from bs4 import BeautifulSoup
from typing import List, Dict
import re

from data.bazaOLX import zapisz_oferte  # Możesz mieć osobną bazę lub ten sam zapis
from scrapers.bazowyScraper import bazowyScraper


class otomotoScraper(bazowyScraper):
    async def szukaj(self, adres: str, kategoria: str, podkategoria: str = ""):
        adresy = [adres] + [f"{adres}?page={nr}" for nr in range(2, 4)]

        naglowki = {"User-Agent": "Mozilla/5.0"}

        async with aiohttp.ClientSession(headers=naglowki) as sesja:
            strony_html = await asyncio.gather(
                *(self.pobierz_strone(sesja, adr) for adr in adresy)
            )

        # Łączymy wszystkie strony w jeden soup – szybciej, jeden parsing
        soup = BeautifulSoup("".join(strony_html), "lxml")
        oferty = soup.select("article[data-id]")

        print(f"DEBUG: Łącznie znaleziono {len(oferty)} ofert")

        for oferta in oferty:
            tytul_elem = oferta.select_one("h2")
            cena_elem = oferta.select_one("h3")
            link_elem = oferta.select_one("a[href]")

            if not all([tytul_elem, cena_elem, link_elem]):
                continue

            tytul = tytul_elem.get_text(strip=True)
            cena_txt = cena_elem.get_text(strip=True).replace(" ", "").replace("zł", "").replace(",", "")
            try:
                cena = int(cena_txt)
            except ValueError:
                continue

            url = link_elem["href"]
            if url.startswith("/"):
                url = "https://www.otomoto.pl" + url

            zapisz_oferte({
                "tytul": tytul,
                "cena": cena,
                "url": url,
                "serwis": "Otomoto",
                "kategoria": kategoria,
                "podkategoria": podkategoria
            })

