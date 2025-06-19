import re

import unicodedata
from scrapers.olxScraper import olxScraper
from PyQt5.QtWidgets import QMessageBox


class dealFinderService:
    def __init__(self, rodzic=None):
        self.rodzic = rodzic


    def zbuduj_url(self, kategoria, fraza=None):
        kategoria_sformatowana = self.formatuj_kategorie(kategoria)
        if fraza:
            return f"https://www.olx.pl/{kategoria_sformatowana}/q-{fraza}/"
        return f"https://www.olx.pl/{kategoria_sformatowana}/"

    def formatuj_kategorie(self, text):
        text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
        text = re.sub(r'[^a-zA-Z0-9]+', '-', text)
        return text.strip('-').lower()

    async def uruchom_scraper(self, url):
        scraper = olxScraper()
        oferty = await scraper.szukaj(url)
        return oferty

