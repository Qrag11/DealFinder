import sqlite3

def utworz_baze():
    conn = sqlite3.connect("data/oferty.db")
    cursor = conn.cursor()
    cursor.execute("""
                CREATE TABLE IF NOT EXISTS oferty (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tytul TEXT,
                    cena INTEGER,
                    url TEXT UNIQUE,
                    data_dodania TEXT,
                    serwis TEXT,
                    kategoria TEXT,
                    podkategoria TEXT
                )
            """)
    conn.commit()
    conn.close()


def zapisz_oferte(oferta: dict):
    conn = sqlite3.connect("data/oferty.db")
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT OR IGNORE INTO oferty (tytul, cena, url, data_dodania, serwis, kategoria, podkategoria)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(url) DO UPDATE SET
                cena=excluded.cena,
                data_dodania=excluded.data_dodania,
                kategoria=excluded.kategoria,
                podkategoria=excluded.podkategoria
        """, (
            oferta["tytul"],
            oferta["cena"],
            oferta["url"],
            oferta["data_dodania"],
            oferta["serwis"],
            oferta.get("kategoria", None),
            oferta.get("podkategoria", None)
        ))
        conn.commit()
    finally:
        conn.close()

