import asyncio
import locale
from datetime import datetime
import aiohttp
from bs4 import BeautifulSoup
import re
from typing import List, Dict
import random
from scrapers.bazowyScraper import bazowyScraper

class olxScraper(bazowyScraper):
    locale.setlocale(locale.LC_TIME, 'Polish_Poland')

    def wyciagnij_date(self, text):
        if "Odświeżono dnia" in text:
            wzor = r"Odświeżono dnia (.+)$"
        elif "Odświeżono Dzisiaj o " in text:
            dzisiaj = datetime.now().strftime("%d %B %Y")
            return dzisiaj
        else:
            wzor = r"- (.+)$"

        match = re.search(wzor, text)
        if match:
            return match.group(1).strip()
        return None

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
                    zdjecie_elem = oferta.select_one("img")
                    data_dodania = oferta.select_one("p[data-testid=location-date]")
                    if not all([tytul_elem, cena_elem, link_elem]):
                        continue



                    zdjecie_url = zdjecie_elem.get("src") or zdjecie_elem.get("data-src") or ""
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
                        "data_dodania": self.wyciagnij_date(data_dodania.get_text(strip=True)) ,
                        "serwis": "OLX",
                        "zdjecie_url": zdjecie_url
                    })

        #########
        print(f"DEBUG: Łącznie ofert: {len(wyniki)}")
       ##########

        return wyniki
