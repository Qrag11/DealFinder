import asyncio
import locale
from datetime import datetime
import aiohttp
from bs4 import BeautifulSoup
import re
from typing import List, Dict
import random

from app.data.bazaOLX import zapisz_oferte
from app.scrapers import BazowyScraper

class OlxScraper(BazowyScraper):
    locale.setlocale(locale.LC_TIME, 'Polish_Poland')

    async def szukaj(self, adres: str, kategoria: str, podkategoria: str = ""):
        adresy = [adres] + [f"{adres}?page={nr}" for nr in range(2, 4)]
        naglowki = {"User-Agent": "Mozilla/5.0"}

        async with aiohttp.ClientSession(headers=naglowki) as sesja:
            strony_html = await asyncio.gather(
                *(self.pobierz_strone(sesja, adr) for adr in adresy)
            )

        soup = BeautifulSoup("".join(strony_html), "lxml")
        oferty = soup.select("div[data-cy=l-card]")



        for oferta in oferty:
            tytul_elem = oferta.select_one("h4")
            cena_elem = oferta.select_one("p[data-testid=ad-price]") or oferta.select_one(".price")
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
            if url.startswith("//"):
                url = "https:" + url
            elif url.startswith("/"):
                url = "https://www.olx.pl" + url

            zapisz_oferte({
                "tytul": tytul,
                "cena": cena,
                "url": url,
                "serwis": "OLX",
                "kategoria": kategoria,
                "podkategoria": podkategoria
            })



