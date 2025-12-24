import asyncio
import sys
from PyQt5.QtWidgets import QApplication
from qasync import QEventLoop
from app.gui import DealFinderApp
from app.data.baza import utworz_baze


async def main():
    pass

if __name__ == "__main__":
    utworz_baze()
    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    window = DealFinderApp()
    window.show()

    with loop:
        loop.run_forever()