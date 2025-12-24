from pathlib import Path

# katalog app/
APP_DIR = Path(__file__).resolve().parent

# zasoby
DATA_DIR = APP_DIR / "data"
DB_DIR = APP_DIR / "data"
STYLES_DIR = APP_DIR / "gui"

# pliki
KATEGORIE_OLX = DATA_DIR / "kategorie_olx.json"
KATEGORIE_OTOMOTO = DATA_DIR / "kategorie_otomoto.json"
DOPASOWANIA_OLX_OTOMOTO = DATA_DIR / "kat_olx_otomoto.json"

DB_PATH = DB_DIR / "oferty.db"