from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QComboBox, QPushButton, QLabel
from PyQt5.QtCore import Qt

class oknoAnalizy(QMainWindow):
    def __init__(self, fraza, kategoria, podkategoria, parent=None):
        super().__init__(parent)
        self.fraza = fraza
        self.kategoria = kategoria
        self.podkategoria = podkategoria

        self.setWindowTitle("Analiza ofert")

        self.init_ui()

    def init_ui(self):
        central = QWidget()
        layout = QVBoxLayout()
        central.setLayout(layout)
        self.setCentralWidget(central)

        # Podgląd przesłanych danych (możesz usunąć później)
        layout.addWidget(QLabel(f"Fraza: {self.fraza}"))
        layout.addWidget(QLabel(f"Kategoria: {self.kategoria}"))
        layout.addWidget(QLabel(f"Podkategoria: {self.podkategoria}"))

        # Przycisk powrotu
        self.btn_powrot = QPushButton("🔙 Powrót")
        self.btn_powrot.clicked.connect(self.close)
        layout.addWidget(self.btn_powrot)

    def closeEvent(self, event):
        if self.parent():
            self.parent().show()
        super().closeEvent(event)

