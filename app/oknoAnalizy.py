from PyQt5.QtWidgets import QHBoxLayout, QMainWindow, QWidget, QVBoxLayout, QComboBox, QPushButton, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtWebEngineWidgets import QWebEngineView
import plotly.io as pio
import tempfile
from PyQt5.QtCore import QUrl

from app.oknoAnalizyService import oknoAnalizyService


class oknoAnalizy(QMainWindow):
    def __init__(self, fraza, kategoria, podkategoria, rodzic=None):
        super().__init__(rodzic)
        self.fraza = fraza
        self.kategoria = kategoria
        self.podkategoria = podkategoria

        # 1) inicjalizacja serwisu ZANIM wywołasz UI
        self.serwis = oknoAnalizyService()

        # 2) ustawienia okna i jeden raz init_ui
        self.setWindowTitle("Analiza ofert")
        self.init_ui()

    def init_ui(self):
        centralny_widget = QWidget()
        glowny_layout = QVBoxLayout(centralny_widget)
        self.setCentralWidget(centralny_widget)

        dane = self.serwis.wczytaj_dane()
        dane_filtrowane = self.serwis.filtruj_oferty(dane, self.fraza, self.kategoria, self.podkategoria)

        if dane_filtrowane.empty:
            glowny_layout.addWidget(QLabel("Brak ogłoszeń dla wybranych kryteriów."))
        else:
            # Utwórz poziomy layout dla wykresów
            layout_wykresow = QHBoxLayout()

            # Histogram
            wykres_histogram, statystyki = self.serwis.generuj_histogram(
                dane_filtrowane,
                tytul=f"Rozkład cen: {self.fraza} / {self.kategoria} / {self.podkategoria}"
            )
            self._dodaj_wykres_do_layoutu(wykres_histogram, layout_wykresow)

            # Box‑plot
            wykres_box = self.serwis.generuj_boxplot(
                dane_filtrowane,
                tytul=f"Box‑plot: {self.fraza} / {self.kategoria} / {self.podkategoria}"
            )
            self._dodaj_wykres_do_layoutu(wykres_box, layout_wykresow)

            # Dodaj poziomy układ wykresów do głównego layoutu
            glowny_layout.addLayout(layout_wykresow)

            # Etykieta ze statystykami
            etykieta_stat = QLabel(
                f"Mediana: {statystyki['mediana']:.0f} zł   •   Q1: {statystyki['q1']:.0f} zł   •   Najlepsza cena ≈ {statystyki['najlepsza']:.0f} zł"
            )
            etykieta_stat.setAlignment(Qt.AlignCenter)
            glowny_layout.addWidget(etykieta_stat)



        # Przycisk powrotu
        self.przycisk_powrotu = QPushButton("🔙 Powrót")
        self.przycisk_powrotu.clicked.connect(self.close)
        glowny_layout.addWidget(self.przycisk_powrotu)

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
