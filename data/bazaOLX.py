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
            INSERT OR IGNORE INTO oferty (tytul, cena, url, serwis, kategoria, podkategoria)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(url) DO UPDATE SET
                cena=excluded.cena,
                kategoria=excluded.kategoria,
                podkategoria=excluded.podkategoria
        """, (
            oferta["tytul"],
            oferta["cena"],
            oferta["url"],
            oferta["serwis"],
            oferta.get("kategoria", None),
            oferta.get("podkategoria", None)
        ))
        conn.commit()
    finally:
        conn.close()

