import json
import sqlite3
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QMessageBox
from app.config import DB_PATH, DOPASOWANIA_OLX_OTOMOTO

class OknoPorownaniaService:
    def __init__(self):
        self.db_path = DB_PATH
        self.dopasowania_path = DOPASOWANIA_OLX_OTOMOTO

    def porownaj_oferty(self, serwis, fraza, kategoria, podkategoria, rodzic=None):
        with open(self.dopasowania_path, encoding="utf-8") as f:
            dopasowania = json.load(f)

        if serwis == "Otomoto":
            znalezione = None
            kategoria_lower = kategoria.strip().lower()
            for dop in dopasowania:
                if dop["kategoria"].strip().lower() == kategoria_lower:
                    znalezione = dop
                    break

            if not znalezione:
                if rodzic:
                    QMessageBox.warning(rodzic, "Brak dopasowania",
                                        f"Nie znaleziono dopasowania dla kategorii: '{kategoria}'.")
                return None

            podkategoria = znalezione["podkategoria"]
        else:  # OLX
            znalezione = None
            for dop in dopasowania:
                if dop["podkategoria"] == podkategoria:
                    znalezione = dop
                    break

            if not znalezione:
                if rodzic:
                    QMessageBox.warning(rodzic, "Brak dopasowania",
                                        f"Nie znaleziono dopasowania dla podkategorii: '{podkategoria}'.")
                return None

            kategoria = znalezione["kategoria"]

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        like_pattern = f"%{fraza}%" if fraza else "%"

        if serwis == "Otomoto":
            cursor.execute("""
                SELECT cena FROM oferty
                WHERE serwis='Otomoto' AND kategoria=? AND tytul LIKE ?
                AND cena IS NOT NULL
            """, (kategoria, like_pattern))
            ceny_baza = [row[0] for row in cursor.fetchall()]

            cursor.execute("""
                SELECT cena FROM oferty
                WHERE serwis='OLX' AND podkategoria=? AND tytul LIKE ?
                AND cena IS NOT NULL
            """, (podkategoria, like_pattern))
            ceny_porownanie = [row[0] for row in cursor.fetchall()]

            nazwy = ['Otomoto', 'OLX']

        else:  # OLX
            cursor.execute("""
                SELECT cena FROM oferty
                WHERE serwis='OLX' AND podkategoria=? AND tytul LIKE ?
                AND cena IS NOT NULL
            """, (podkategoria, like_pattern))
            ceny_baza = [row[0] for row in cursor.fetchall()]

            cursor.execute("""
                SELECT cena FROM oferty
                WHERE serwis='Otomoto' AND LOWER(kategoria)=LOWER(?)
                AND tytul LIKE ?
                AND cena IS NOT NULL
            """, (kategoria, like_pattern))
            ceny_porownanie = [row[0] for row in cursor.fetchall()]

            nazwy = ['OLX', 'Otomoto']

        conn.close()

        if not ceny_baza or not ceny_porownanie:
            if rodzic:
                QMessageBox.warning(rodzic, "Brak danych",
                                    "Brak ofert do porównania dla wybranej kategorii/frazy.")
            return None

        srednia_baza = sum(ceny_baza) / len(ceny_baza)
        srednia_porownanie = sum(ceny_porownanie) / len(ceny_porownanie)

        dane = {
            "nazwy": nazwy,
            "srednie_ceny": [srednia_baza, srednia_porownanie],
            "tytul": f'Porównanie średnich cen: {kategoria} / {podkategoria}\nFraza: "{fraza}"'
        }

        return dane

    def rysuj_wykres(self, dane):
        fig, ax = plt.subplots()
        ax.bar(dane["nazwy"], dane["srednie_ceny"], color=['blue', 'orange'])
        ax.set_title(dane["tytul"])
        ax.set_ylabel('Średnia cena [PLN]')
        plt.show()
