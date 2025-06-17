# main.py

import asyncio

from scrapers.olxScraper import olxScraper


async def main():
    adres = "https://www.olx.pl/elektronika/telefony/smartfony-telefony-komorkowe/q-iphone/q-{fraza}/"
    scraper = olxScraper()
    oferty = await scraper.szukaj(adres)
    for o in oferty:
        print(f"{o['tytul']} – {o['cena']} zł – {o['url']} - {o['data_dodania']}")


if __name__ == "__main__":
    asyncio.run(main())