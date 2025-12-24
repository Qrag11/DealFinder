import json
import asyncio
from app.config import KATEGORIE_OLX
from app.config import STYLES_DIR

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QWidget, QComboBox, QMessageBox, QProgressDialog
)

from PyQt5.QtCore import Qt

import os

from app.services.deal_finder_service import DealFinderService
from .okno_analizy import OknoAnalizy
from .okno_porownania import OknoPorownania


from .okno_analizy import OknoAnalizy
from .okno_porownania import OknoPorownania
from app.config import DB_PATH

class DealFinderApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.DealFinderService = DealFinderService(self)
        self.setWindowTitle("Deal Finder")
        self.setGeometry(100, 100, 400, 300)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.label_fraza = QLabel("Wpisz frazę:")
        self.fraza_input = QLineEdit()
        self.layout.addWidget(self.label_fraza)
        self.layout.addWidget(self.fraza_input)

        with open(KATEGORIE_OLX, encoding="utf-8") as f:
            self.kategorie = json.load(f)

        self.label_zrodlo = QLabel("Wybierz źródło ofert:")
        self.zrodlo_combo = QComboBox()
        self.zrodlo_combo.addItems(["OLX", "Otomoto"])
        self.layout.addWidget(self.label_zrodlo)
        self.layout.addWidget(self.zrodlo_combo)



        self.zrodlo_combo.currentTextChanged.connect(self.on_zrodlo_change)

        self.label_kategoria = QLabel("Wybierz kategorię:")
        self.kategoria_combo = QComboBox()
        self.kategoria_combo.addItems(self.kategorie.keys())
        self.layout.addWidget(self.label_kategoria)
        self.layout.addWidget(self.kategoria_combo)

        self.label_podkategoria = QLabel("Wybierz podkategorię:")
        self.podkategoria_combo = QComboBox()
        self.layout.addWidget(self.label_podkategoria)
        self.layout.addWidget(self.podkategoria_combo)

        self.kategoria_combo.currentTextChanged.connect(self.on_kategoria_change)
        self.on_kategoria_change(self.kategoria_combo.currentText())

        self.load_kategorie("OLX")

        self.btn_szukaj = QPushButton("🔍 Szukaj ofert")
        self.btn_szukaj.clicked.connect(self.szukaj_ofert)
        self.layout.addWidget(self.btn_szukaj)

        if os.path.exists(DB_PATH):
            self.btn_analiza = QPushButton("📊 Analizuj oferty")
            self.btn_analiza.clicked.connect(self.analizuj_oferty)
            self.layout.addWidget(self.btn_analiza)

        self.btn_porownaj = QPushButton("🔄 Porównaj OLX i Otomoto")
        self.btn_porownaj.clicked.connect(self.porownaj_oferty)
        self.layout.addWidget(self.btn_porownaj)

        self.zaladuj_styl()

    def zaladuj_styl(self):
        with open(STYLES_DIR/"styles.qss") as f:
            styl = f.read()
        self.setStyleSheet(styl)

    def on_kategoria_change(self, kategoria):
        podkategorie = self.kategorie.get(kategoria, {}).get("podkategorie", {})
        self.podkategoria_combo.clear()
        if podkategorie:
            self.podkategoria_combo.addItems(podkategorie.keys())
        else:
            self.podkategoria_combo.addItem("Brak podkategorii")

    def szukaj_ofert(self):
        fraza = self.fraza_input.text().strip()
        kategoria = self.kategoria_combo.currentText()
        podkategoria = self.podkategoria_combo.currentText()
        zrodlo = self.zrodlo_combo.currentText()

        url = self.DealFinderService.zbuduj_url(kategoria, fraza, podkategoria, zrodlo)

        progress = QProgressDialog("Trwa szukanie ofert...", None, 0, 0, self)
        progress.setWindowModality(Qt.WindowModal)
        progress.setCancelButton(None)
        progress.setWindowTitle("Proszę czekać")
        progress.show()

        async def run_scraper():
            try:
                await self.DealFinderService.uruchom_scraper(url, kategoria, podkategoria, zrodlo)
            except Exception as e:
                progress.close()
                QMessageBox.warning(self, "Błąd", f"Błąd podczas pobierania ofert: {e}")
                return
            progress.close()
            QMessageBox.information(self, "Sukces", "Oferty zostały pobrane.")

        asyncio.create_task(run_scraper())

    def analizuj_oferty(self):
        self.hide()

        fraza = self.fraza_input.text()
        kategoria = self.kategoria_combo.currentText()
        podkategoria = self.podkategoria_combo.currentText()

        self.okno = OknoAnalizy(fraza, kategoria, podkategoria, rodzic=self)
        self.okno.show()

    def load_kategorie(self, zrodlo):
        if zrodlo == "OLX":
            sciezka = "app/data/kategorie_olx.json"
        elif zrodlo == "Otomoto":
            sciezka = "app/data/kategorie_otomoto.json"
        else:
            sciezka = "app/data/kategorie_olx.json"

        try:
            with open(sciezka, encoding="utf-8") as f:
                self.kategorie = json.load(f)
        except Exception as e:
            QMessageBox.warning(self, "Błąd", f"Nie można załadować kategorii z {sciezka}: {e}")
            self.kategorie = {}

        self.kategoria_combo.clear()
        self.kategoria_combo.addItems(self.kategorie.keys())

        if self.kategoria_combo.count() > 0:
            self.on_kategoria_change(self.kategoria_combo.currentText())
        else:
            self.podkategoria_combo.clear()
            self.podkategoria_combo.addItem("Brak podkategorii")

    def on_zrodlo_change(self, zrodlo):
        self.load_kategorie(zrodlo)

    def porownaj_oferty(self):
        serwis = self.zrodlo_combo.currentText()
        fraza = self.fraza_input.text().strip()
        kategoria = self.kategoria_combo.currentText()
        podkategoria = self.podkategoria_combo.currentText()

        self.okno_porownania = OknoPorownania(serwis, fraza, kategoria, podkategoria, rodzic=self)
        self.okno_porownania.show()










