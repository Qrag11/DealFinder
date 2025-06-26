# OLX Deal Finder

Aplikacja desktopowa napisana w Pythonie z użyciem PyQt5 i matplotlib do porównywania ofert z OLX i Otomoto.

## Klasy i Funkcje

###  `dealFinderApp(QMainWindow)`
Główne okno aplikacji do wyszukiwania i porównywania ofert z OLX i Otomoto.

####  Główne funkcje:
- `__init__` – Inicjalizuje UI, ładuje kategorie, dodaje przyciski.
- `zaladuj_styl()` – Ładuje styl z pliku `.qss`.
- `on_kategoria_change(kategoria)` – Uaktualnia podkategorie po zmianie kategorii.
- `on_zrodlo_change(zrodlo)` – Przełącza źródło (OLX/Otomoto), ładuje odpowiednie kategorie.
- `load_kategorie(zrodlo)` – Wczytuje plik JSON z kategoriami.
- `szukaj_ofert()` – Uruchamia scraper z wybranymi parametrami.
- `analizuj_oferty()` – Otwiera okno analizy ofert.
- `porownaj_oferty()` – Otwiera okno porównania OLX vs Otomoto.

###  `dealFinderService`
Serwis odpowiadający za budowę URL-i i uruchamianie scraperów dla OLX i Otomoto.

#### Główne funkcje:
- `__init__(rodzic=None)` – Inicjalizuje serwis.
- `zbuduj_url(kategoria, fraza=None, podkategoria="", zrodlo="OLX")` – Buduje adres URL do wyszukiwania ofert na podstawie kategorii, podkategorii i frazy.
- `formatuj_kategorie(text)` – Formatuje nazwę kategorii/podkategorii do formatu URL (usuwa polskie znaki i znaki specjalne).
- `uruchom_scraper(url, kategoria, podkategoria="", zrodlo="OLX")` – Asynchronicznie uruchamia odpowiedni scraper (`olxScraper` lub `otomotoScraper`) i zwraca znalezione oferty.

### `oknoAnalizy(QMainWindow)`
Okno aplikacji do analizy ofert na podstawie wybranej frazy, kategorii i podkategorii.

#### Główne funkcje:
- `__init__(fraza, kategoria, podkategoria, rodzic=None)` – Inicjalizuje okno analizy i ładuje dane.
- `init_ui()` – Buduje interfejs użytkownika, w tym filtry cenowe i wykresy.
- `_dodaj_wykres_do_layoutu(wykres, layout)` – Dodaje wykres Plotly do layoutu.
- `odswiez_ogloszenia()` – Filtruje i wyświetla listę ofert w określonym zakresie cenowym.
- `closeEvent(zdarzenie)` – Obsługuje zamknięcie okna, przywracając widoczność rodzica.

### `oknoAnalizyService`

Serwis obsługujący przetwarzanie danych i generowanie wykresów dla okna analizy ofert.

#### Główne funkcje:
- `wczytaj_dane()` – Ładuje dane ofert z bazy SQLite.
- `filtruj_oferty(df, fraza, kategoria, podkategoria)` – Filtruje oferty wg frazy, kategorii i podkategorii.
- `oblicz_statystyki(df)` – Oblicza podstawowe statystyki cenowe.
- `generuj_histogram(df, tytul)` – Tworzy histogram cen z ograniczeniem do 95 percentyla.
- `generuj_boxplot(df, tytul)` – Tworzy wykres typu boxplot cen z ograniczeniem do 95 percentyla.

### `oknoPorownania`

Okno porównania ofert OLX i Otomoto z wykresem słupkowym średnich cen.

#### Główne elementy i funkcje:
- `__init__(serwis, fraza, kategoria, podkategoria, rodzic=None)` — inicjalizuje okno.
- `init_ui()` — tworzy interfejs.
- `wykonaj_porownanie()` — pobiera dane porównawcze i rysuje wykres słupkowy średnich.

### `oknoPorownaniaService`

Serwis do porównywania ofert OLX i Otomoto oraz rysowania wykresów.

#### Główne metody:
- `porownaj_oferty(serwis, fraza, kategoria, podkategoria, rodzic=None)` - Pobiera i porównuje ceny z bazy  na podstawie frazy, kategorii i podkategorii. Zwraca słownik z nazwami serwisów, średnimi cenami i tytułem wykresu lub `None` jeśli brak danych/dopasowań. Wyświetla ostrzeżenie w GUI jeśli brak dopasowania lub danych.
- `rysuj_wykres(dane)` Rysuje słupkowy wykres średnich cen za pomocą matplotlib.


### `utworz_baze`  
Tworzy bazę danych SQLite z tabelą `oferty` (jeśli jeszcze nie istnieje) o strukturze:  
- `id` (INTEGER PRIMARY KEY AUTOINCREMENT)  
- `tytul` (TEXT)  
- `cena` (INTEGER)  
- `url` (TEXT UNIQUE)  
- `serwis` (TEXT)  
- `kategoria` (TEXT)  
- `podkategoria` (TEXT)

#### Główne metody:
- `zapisz_oferte(oferta: dict)` - Zapisuje ofertę do bazy danych `oferty.db`. Jeśli oferta z takim samym `url` już istnieje, aktualizuje jej `cena`, `kategoria` i `podkategoria`.

### `bazowyScraper`

Abstrakcyjna klasa bazowa dla scraperów, definiuje metody do pobierania i wyszukiwania danych ze stron.

#### Główne elementy i funkcje:
- `async szukaj(adres: str) -> List[Dict]` — abstrakcyjna metoda do wyszukiwania danych pod wskazanym adresem.
- `async pobierz_strone(sesja, adres: str) -> str` — pobiera stronę HTTP, zwraca zawartość strony jako tekst.

### `olxScraper`

Scraper OLX dziedziczący po `bazowyScraper`, pobiera oferty z kilku stron OLX i zapisuje je do bazy.

#### Główne elementy i funkcje:
- `async szukaj(adres: str, kategoria: str, podkategoria: str = "")` — pobiera i łączy HTML z pierwszych 3 stron wyników, parsuje oferty, wyciąga potrzebne informacje, normalizuje dane i zapisuje oferty do bazy za pomocą `zapisz_oferte`.

### `otomotoScraper`

Scraper dla Otomoto, dziedziczący po `bazowyScraper`. Pobiera i parsuje oferty z kilku stron Otomoto, zapisując je do bazy.

#### Główne elementy i funkcje:
- `async szukaj(adres: str, kategoria: str, podkategoria: str = "")` — pobiera i łączy HTML z pierwszych 3 stron wyników, arsuje oferty, wyciąga potrzebne informacje, normalizuje dane i zapisuje oferty do bazy za pomocą `zapisz_oferte`.

## 🔧 Instalacja

1. **Utwórz środowisko wirtualne:**

```bash
python -m venv venv
```
```bash
source venv/bin/activate  # Linux/macOS
```
```bash
venv\Scripts\activate     # Windows
```
```bash
pip install -r requirements.txt
```
2. **Uruchom program:**
    ```bash
    python .\main.py
    ```
