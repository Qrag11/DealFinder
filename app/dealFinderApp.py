import json
import asyncio
import re
from contextlib import nullcontext

import unicodedata
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QWidget, QComboBox, QMessageBox
)
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt
import sys
import os

from app.dealFinderService import dealFinderService
from scrapers.olxScraper import olxScraper


class dealFinderApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.dealFinderService = dealFinderService(self)
        self.setWindowTitle("OLX Deal Finder")
        self.setGeometry(100, 100, 400, 300)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.label_fraza = QLabel("Wpisz frazę:")
        self.fraza_input = QLineEdit()
        self.layout.addWidget(self.label_fraza)
        self.layout.addWidget(self.fraza_input)

        with open("data/kategorie_olx.json", encoding="utf-8") as f:
            self.kategorie = json.load(f)

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

        self.btn_szukaj = QPushButton("🔍 Szukaj ofert")
        self.btn_szukaj.clicked.connect(self.szukaj_ofert)
        self.layout.addWidget(self.btn_szukaj)

        if os.path.exists("data/oferty.db"):
            self.btn_analiza = QPushButton("📊 Analizuj oferty")
            self.btn_analiza.clicked.connect(self.analizuj_oferty)
            self.layout.addWidget(self.btn_analiza)

            self.btn_pomoc = QPushButton("🤖 Pomoc w wyborze")
            self.btn_pomoc.clicked.connect(self.pomoc_wyboru)
            self.layout.addWidget(self.btn_pomoc)

        self.stylizuj()

    def stylizuj(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #2b2b2b;
                color: #ffffff;
                font-size: 14px;
            }

            QLineEdit, QComboBox {
                padding: 6px;
                border: 1px solid #555;
                border-radius: 6px;
                background-color: #3c3f41;
            }

            QPushButton {
                padding: 10px;
                border: 1px solid #888;
                border-radius: 8px;
                background-color: #5a5a5a;
            }

            QPushButton:hover {
                background-color: #777;
            }
        """)



    def szukaj_ofert(self):
        fraza = self.fraza_input.text()
        kategoria = self.kategoria_combo.currentText()

        adres = self.dealFinderService.zbuduj_url(kategoria, fraza)

        asyncio.create_task(self.dealFinderService.uruchom_scraper(adres))




    def analizuj_oferty(self):
        QMessageBox.information(self, "Analiza", "Tu będzie analiza ofert.")

    def pomoc_wyboru(self):
        QMessageBox.information(self, "Pomoc", "Tu będzie inteligentna pomoc w wyborze.")

    def on_kategoria_change(self, kategoria):
        podkategorie = self.kategorie.get(kategoria, {}).get("podkategorie", {})
        self.podkategoria_combo.clear()
        if podkategorie:
            self.podkategoria_combo.addItems(podkategorie.keys())
        else:
            self.podkategoria_combo.addItem("Brak podkategorii")


