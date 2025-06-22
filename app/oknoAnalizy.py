from PyQt5.QtWidgets import (
    QHBoxLayout, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel,
    QScrollArea, QSizePolicy
)
from PyQt5.QtCore import Qt
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QPixmap
import plotly.io as pio
import tempfile
from PyQt5.QtCore import QUrl
import requests
from io import BytesIO

from app.oknoAnalizyService import oknoAnalizyService


class oknoAnalizy(QMainWindow):
    def __init__(self, fraza, kategoria, podkategoria, rodzic=None):
        super().__init__(rodzic)
        self.fraza = fraza
        self.kategoria = kategoria
        self.podkategoria = podkategoria

        self.serwis = oknoAnalizyService()

        self.setWindowTitle("Analiza ofert")
        self.init_ui()

    def init_ui(self):
        centralny_widget = QWidget()
        glowny_layout = QHBoxLayout(centralny_widget)  # Główny layout poziomy
        self.setCentralWidget(centralny_widget)

        dane = self.serwis.wczytaj_dane()
        dane_filtrowane = self.serwis.filtruj_oferty(dane, self.fraza, self.kategoria, self.podkategoria)

        if dane_filtrowane.empty:
            glowny_layout.addWidget(QLabel("Brak ogłoszeń dla wybranych kryteriów."))
            return

        # LEWA STRONA: wykresy + przycisk w pionie
        lewa_strona = QWidget()
        lewy_layout = QVBoxLayout(lewa_strona)

        # Layout poziomy dla wykresów
        layout_wykresow = QHBoxLayout()

        wykres_histogram, statystyki = self.serwis.generuj_histogram(
            dane_filtrowane,
            tytul=f"Rozkład cen: {self.fraza} / {self.kategoria} / {self.podkategoria}"
        )
        self._dodaj_wykres_do_layoutu(wykres_histogram, layout_wykresow)

        wykres_box = self.serwis.generuj_boxplot(
            dane_filtrowane,
            tytul=f"Box‑plot: {self.fraza} / {self.kategoria} / {self.podkategoria}"
        )
        self._dodaj_wykres_do_layoutu(wykres_box, layout_wykresow)

        lewy_layout.addLayout(layout_wykresow)

        etykieta_stat = QLabel(
            f"Mediana: {statystyki['mediana']:.0f} zł   •   Q1: {statystyki['q1']:.0f} zł   •   Najlepsza cena ≈ {statystyki['najlepsza']:.0f} zł"
        )
        etykieta_stat.setAlignment(Qt.AlignCenter)
        lewy_layout.addWidget(etykieta_stat)

        self.przycisk_powrotu = QPushButton("🔙 Powrót")
        self.przycisk_powrotu.clicked.connect(self.close)
        lewy_layout.addWidget(self.przycisk_powrotu)

        glowny_layout.addWidget(lewa_strona, 3)  # 3/4 szerokości okna

        # PRAWA STRONA: przewijalna lista ogłoszeń
        prawa_strona = QWidget()
        prawa_layout = QVBoxLayout(prawa_strona)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        prawa_lista_widget = QWidget()
        prawa_lista_layout = QVBoxLayout(prawa_lista_widget)

        # Dodaj ogłoszenia - zdjęcie + tytuł + cena
        for idx, wiersz in dane_filtrowane.iterrows():
            ogloszenie = QWidget()
            ogloszenie_layout = QHBoxLayout(ogloszenie)

            # Ładuj zdjęcie z URL
            obrazek = QLabel()
            obrazek.setFixedSize(120, 90)  # ustalony rozmiar miniatury

            try:
                response = requests.get(wiersz['zdjecie_url'])
                pixmap = QPixmap()
                pixmap.loadFromData(response.content)
                pixmap = pixmap.scaled(120, 90, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                obrazek.setPixmap(pixmap)
            except Exception:
                obrazek.setText("Brak zdjęcia")

            ogloszenie_layout.addWidget(obrazek)

            # Info tekstowe - tytuł i cena
            info = QLabel(f"<b>{wiersz['tytul']}</b><br>Cena: {wiersz['cena']} zł")
            info.setWordWrap(True)
            ogloszenie_layout.addWidget(info)

            prawa_lista_layout.addWidget(ogloszenie)

        prawa_lista_layout.addStretch()
        scroll.setWidget(prawa_lista_widget)
        prawa_layout.addWidget(scroll)

        glowny_layout.addWidget(prawa_strona, 2)  # 2/5 szerokości okna (proporcja)

    def closeEvent(self, zdarzenie):
        if self.parent():
            self.parent().show()
        super().closeEvent(zdarzenie)

    def _dodaj_wykres_do_layoutu(self, wykres, layout):
        html = pio.to_html(wykres, full_html=False)
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".html")
        tmp.write(html.encode('utf-8'))
        tmp.flush()
        podglad = QWebEngineView()
        podglad.load(QUrl.fromLocalFile(tmp.name))
        layout.addWidget(podglad)
