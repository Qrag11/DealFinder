from PyQt5.QtWidgets import (
    QHBoxLayout, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel,
    QScrollArea, QSizePolicy, QSpinBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QUrl

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

from app.services.okno_analizy_service import OknoAnalizyService


class OknoAnalizy(QMainWindow):
    def __init__(self, fraza, kategoria, podkategoria, rodzic=None):
        super().__init__(rodzic)
        self.fraza = fraza
        self.kategoria = kategoria
        self.podkategoria = podkategoria

        self.serwis = OknoAnalizyService()

        self.setWindowTitle("Analiza ofert")
        self.init_ui()

    def init_ui(self):
        centralny_widget = QWidget()
        glowny_layout = QHBoxLayout(centralny_widget)
        self.setCentralWidget(centralny_widget)

        dane = self.serwis.wczytaj_dane()
        self.dane_filtrowane = self.serwis.filtruj_oferty(dane, self.fraza, self.kategoria, self.podkategoria)

        lewa_strona = QWidget()
        self.lewy_layout = QVBoxLayout(lewa_strona)

        # Filtry cenowe
        self.min_cena = QSpinBox()
        self.min_cena.setPrefix("Od: ")
        self.min_cena.setMaximum(1_000_000)
        self.min_cena.setValue(0)

        self.max_cena = QSpinBox()
        self.max_cena.setPrefix("Do: ")
        self.max_cena.setMaximum(1_000_000)
        self.max_cena.setValue(1_000_000)

        self.przycisk_filtruj = QPushButton("Filtruj")
        self.przycisk_filtruj.clicked.connect(self.odswiez_ogloszenia)

        filtr_layout = QHBoxLayout()
        filtr_layout.addWidget(self.min_cena)
        filtr_layout.addWidget(self.max_cena)
        filtr_layout.addWidget(self.przycisk_filtruj)
        self.lewy_layout.addLayout(filtr_layout)

        if self.dane_filtrowane.empty:
            glowny_layout.addWidget(QLabel("Brak ogłoszeń dla wybranych kryteriów."))
            return

        # Wykresy
        layout_wykresow = QHBoxLayout()

        wykres_histogram, statystyki = self.serwis.generuj_histogram(
            self.dane_filtrowane,
            tytul=f"Rozkład cen: {self.fraza} / {self.kategoria} / {self.podkategoria}"
        )
        self._dodaj_wykres_do_layoutu(wykres_histogram, layout_wykresow)

        wykres_box = self.serwis.generuj_boxplot(
            self.dane_filtrowane,
            tytul=f"Box‑plot: {self.fraza} / {self.kategoria} / {self.podkategoria}"
        )
        self._dodaj_wykres_do_layoutu(wykres_box, layout_wykresow)

        self.lewy_layout.addLayout(layout_wykresow)

        etykieta_stat = QLabel(
            f"Mediana: {statystyki['mediana']:.0f} zł   •   Q1: {statystyki['q1']:.0f} zł   •   Najlepsza cena ≈ {statystyki['najlepsza']:.0f} zł"
        )
        etykieta_stat.setAlignment(Qt.AlignCenter)
        self.lewy_layout.addWidget(etykieta_stat)

        self.przycisk_powrotu = QPushButton("🔙 Powrót")
        self.przycisk_powrotu.clicked.connect(self.close)
        self.lewy_layout.addWidget(self.przycisk_powrotu)

        glowny_layout.addWidget(lewa_strona, 3)

        # Lista ogłoszeń
        prawa_strona = QWidget()
        prawa_layout = QVBoxLayout(prawa_strona)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        prawa_lista_widget = QWidget()
        self.prawa_lista_layout = QVBoxLayout(prawa_lista_widget)

        self.odswiez_ogloszenia()

        scroll.setWidget(prawa_lista_widget)
        prawa_layout.addWidget(scroll)

        glowny_layout.addWidget(prawa_strona, 2)

    def closeEvent(self, zdarzenie):
        if self.parent():
            self.parent().show()
        super().closeEvent(zdarzenie)

    def _dodaj_wykres_do_layoutu(self, figura_matplotlib, layout):
        """Dodaje matplotlib Figure do layoutu PyQt"""
        canvas = FigureCanvas(figura_matplotlib)
        layout.addWidget(canvas)

    def odswiez_ogloszenia(self):
        for i in reversed(range(self.prawa_lista_layout.count())):
            widget = self.prawa_lista_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        min_c = self.min_cena.value()
        max_c = self.max_cena.value()

        dane_zakres = self.dane_filtrowane[
            (self.dane_filtrowane['cena'] >= min_c) & (self.dane_filtrowane['cena'] <= max_c)
        ]

        if dane_zakres.empty:
            self.prawa_lista_layout.addWidget(QLabel("Brak ogłoszeń w tym zakresie cenowym."))
        else:
            for _, wiersz in dane_zakres.iterrows():
                ogloszenie = QWidget()
                layout = QHBoxLayout(ogloszenie)

                przycisk = QPushButton(f"{wiersz['tytul']}\nCena: {wiersz['cena']} zł")
                przycisk.setStyleSheet("text-align: left;")
                przycisk.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
                przycisk.clicked.connect(lambda _, url=wiersz['url']: QDesktopServices.openUrl(QUrl(url)))

                layout.addWidget(przycisk)
                self.prawa_lista_layout.addWidget(ogloszenie)
