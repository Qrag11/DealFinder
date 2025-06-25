from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget

class oknoPorownania(QMainWindow):
    def __init__(self, dane_porownania, rodzic=None):
        super().__init__(rodzic)
        self.dane = dane_porownania
        self.setWindowTitle("Porównanie ofert")
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)

        # Przykładowo wyświetlamy dane porównania w etykietach
        for klucz, wartosc in self.dane.items():
            layout.addWidget(QLabel(f"{klucz}: {wartosc}"))

        self.setCentralWidget(central_widget)
