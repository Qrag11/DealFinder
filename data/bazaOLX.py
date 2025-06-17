import sqlite3

def utworz_baze():
    def utworz_baze():
        conn = sqlite3.connect("oferty.db")
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS oferty (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tytul TEXT,
                cena INTEGER,
                url TEXT UNIQUE,
                data_dodania TEXT,
                serwis TEXT,
                zdjecie_url TEXT
            )
        """)
        conn.commit()
        conn.close()


def zapisz_oferte(oferta: dict):
    conn = sqlite3.connect("oferty.db")
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT OR IGNORE INTO oferty (tytul, cena, url, data_dodania, serwis, zdjecie_url)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(url) DO UPDATE SET
                cena=excluded.cena,
                data_dodania=excluded.data_dodania
        """, (
            oferta["tytul"],
            oferta["cena"],
            oferta["url"],
            oferta["data_dodania"],
            oferta["serwis"],
            oferta["zdjecie_url"]
        ))
        conn.commit()
    finally:
        conn.close()

