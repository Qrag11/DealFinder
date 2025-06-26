from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from app.oknoPorownaniaService import oknoPorownaniaService


class oknoPorownania(QMainWindow):
    def __init__(self, serwis, fraza, kategoria, podkategoria, rodzic=None):
        super().__init__(rodzic)
        self.serwis = serwis
        self.fraza = fraza
        self.kategoria = kategoria
        self.podkategoria = podkategoria
        self.rodzic = rodzic

        self.setWindowTitle("Okno Porównania Ofert")
        self.serwis_obj = oknoPorownaniaService()

        self.init_ui()
        self.wykonaj_porownanie()

    def init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        self.layout = QVBoxLayout(central)

        self.przycisk_zamknij = QPushButton("Zamknij")
        self.przycisk_zamknij.clicked.connect(self.close)
        self.layout.addWidget(self.przycisk_zamknij)

    def wykonaj_porownanie(self):
        dane = self.serwis_obj.porownaj_oferty(self.serwis, self.fraza, self.kategoria, self.podkategoria, rodzic=self)
        if dane is None:
            return

        fig, ax = plt.subplots()
        ax.bar(dane["nazwy"], dane["srednie_ceny"], color=['blue', 'orange'])
        ax.set_title(dane["tytul"])
        ax.set_ylabel('Średnia cena [PLN]')

        canvas = FigureCanvas(fig)

        self.layout.insertWidget(0, canvas)
