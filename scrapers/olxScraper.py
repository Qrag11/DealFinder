import asyncio
import aiohttp
from bs4 import BeautifulSoup
from typing import List, Dict
import random
import datetime
from scrapers.bazowyScraper import bazowyScraper

class olxScraper(bazowyScraper):
    async def szukaj(self, adres: str) -> List[Dict]:


        adresy = [
            adres,
            *(f"{adres}?page={nr}" for nr in (2, 3))
        ]

        naglowki = {"User-Agent": "Mozilla/5.0"}
        async with aiohttp.ClientSession(headers=naglowki) as sesja:
            strony = await asyncio.gather(
                *(self.pobierz_strone(sesja, adr) for adr in adresy)
            )


        wyniki: List[Dict] = []
        for idx, html in enumerate(strony, start=1):
            soup = BeautifulSoup(html, "lxml")
            oferty_na_stronie = soup.select("div[data-cy=l-card]")

            #########
            print(f"DEBUG: Strona {idx} - znaleziono ofert: {len(oferty_na_stronie)}")
            ########

            for oferta in oferty_na_stronie:
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

                wyniki.append({
                    "tytul": tytul,
                    "cena": cena,
                    "url": url,
                    "znacznik_czasu": datetime.datetime.now().isoformat(),
                    "serwis": "OLX"
                })

        #########
        print(f"DEBUG: Łącznie ofert: {len(wyniki)}")
       ##########

        return wyniki
