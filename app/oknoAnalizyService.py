import sqlite3
import pandas as pd
import plotly.express as px
import numpy as np

class oknoAnalizyService:

    def wczytaj_dane(self) -> pd.DataFrame:
        polaczenie = sqlite3.connect("data/oferty.db")
        df = pd.read_sql_query("""
            SELECT tytul, cena, url, data_dodania, kategoria, podkategoria, zdjecie_url
            FROM oferty
        """, polaczenie)
        polaczenie.close()
        return df

    def filtruj_oferty(self, df: pd.DataFrame, fraza: str, kategoria: str, podkategoria: str) -> pd.DataFrame:
        maska = pd.Series(True, index=df.index)
        if fraza:
            maska &= df['tytul'].str.contains(fraza, case=False, na=False)
        if kategoria:
            maska &= df['kategoria'] == kategoria
        if podkategoria:
            maska &= df['podkategoria'] == podkategoria
        return df[maska].copy()

    def oblicz_statystyki(self, df: pd.DataFrame):
        q1 = df['cena'].quantile(0.25)
        mediana = df['cena'].median()
        najlepsza = df['cena'].min()
        return {'q1': q1, 'mediana': mediana, 'najlepsza': najlepsza}

    def generuj_histogram(self, df, tytul="Rozkład cen"):
        ceny = df['cena']

        # Oblicz wartości statystyczne
        q1 = np.percentile(ceny, 25)
        q3 = np.percentile(ceny, 75)
        mediana = np.median(ceny)
        najlepsza = ceny.min()

        # Przycięcie danych do 95 percentyla
        gorna_granica = np.percentile(ceny, 95)
        ceny_przyciecie = ceny[ceny <= gorna_granica]

        # Histogram tylko z przyciętymi wartościami
        wykres = px.histogram(ceny_przyciecie, nbins=30, title=tytul, labels={"value": "Cena (zł)"})
        wykres.update_layout(bargap=0.1)

        statystyki = {"mediana": mediana, "q1": q1, "najlepsza": najlepsza}
        return wykres, statystyki

    def generuj_boxplot(self, df, tytul="Box‑plot cen"):
        ceny = df['cena']

        gorna_granica = np.percentile(ceny, 95)
        ceny_przyciecie = ceny[ceny <= gorna_granica]

        wykres = px.box(ceny_przyciecie, title=tytul, labels={"value": "Cena (zł)"})
        return wykres
