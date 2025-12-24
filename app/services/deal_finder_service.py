import re

import unicodedata
from app.scrapers import OlxScraper
from app.scrapers import OtomotoScraper



class DealFinderService:
    def __init__(self, rodzic=None):
        self.rodzic = rodzic

    def zbuduj_url(self, kategoria, fraza=None, podkategoria="", zrodlo="OLX"):
        if zrodlo == "OLX":
            baza_kat = self.rodzic.kategorie if self.rodzic else {}
            url = ""
            if kategoria in baza_kat:
                kat_info = baza_kat[kategoria]
                if isinstance(kat_info, dict) and "url" in kat_info:
                    url = kat_info["url"]
                    if podkategoria and podkategoria != "Brak podkategorii":
                        podkategorie = kat_info.get("podkategorie", {})
                        if podkategoria in podkategorie:
                            url = podkategorie[podkategoria]
                else:
                    url = f"https://www.olx.pl/{self.formatuj_kategorie(kategoria)}/"
            else:
                url = f"https://www.olx.pl/{self.formatuj_kategorie(kategoria)}/"

            if fraza:
                if not url.endswith('/'):
                    url += '/'
                url += f"q-{fraza}/"

            return url


        elif zrodlo == "Otomoto":

            baza_kat = self.rodzic.kategorie if self.rodzic else {}

            url = ""

            if kategoria in baza_kat:

                kat_info = baza_kat[kategoria]
                if isinstance(kat_info, dict) and "url" in kat_info:

                    url = kat_info["url"]

                    if podkategoria and podkategoria != "Brak podkategorii":

                        podkategorie = kat_info.get("podkategorie", {})

                        if podkategoria in podkategorie:
                            url = podkategorie[podkategoria]

                else:

                    url = f"https://www.otomoto.pl/{self.formatuj_kategorie(kategoria)}/"

            else:

                url = f"https://www.otomoto.pl/{self.formatuj_kategorie(kategoria)}/"

            if fraza:

                if not url.endswith('/'):
                    url += '/'

                url += f"q-{fraza}/"

            return url

            return None

    def formatuj_kategorie(self, text):
        text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
        text = re.sub(r'[^a-zA-Z0-9]+', '-', text)
        return text.strip('-').lower()

    async def uruchom_scraper(self, url: str, kategoria: str, podkategoria: str = "", zrodlo="OLX"):
        if zrodlo == "OLX":
            scraper = OlxScraper()
        elif zrodlo == "Otomoto":
            scraper = OtomotoScraper()
        else:
            scraper = OlxScraper()

        oferty = await scraper.szukaj(url, kategoria, podkategoria)
        return oferty


