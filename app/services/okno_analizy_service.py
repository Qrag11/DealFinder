import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from app.config import DB_PATH

class OknoAnalizyService:

    def wczytaj_dane(self) -> pd.DataFrame:
        polaczenie = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query("""
            SELECT tytul, cena, url, kategoria, podkategoria
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

        # przycięcie na 95 percentyl
        gorna_granica = np.percentile(ceny, 95)
        ceny_przyciecie = ceny[ceny <= gorna_granica]

        fig, ax = plt.subplots()
        ax.hist(ceny_przyciecie, bins=30, color='skyblue', edgecolor='black')
        ax.set_title(tytul)
        ax.set_xlabel("Cena (zł)")
        ax.set_ylabel("Liczba ogłoszeń")

        statystyki = {
            "mediana": np.median(ceny),
            "q1": np.percentile(ceny, 25),
            "najlepsza": ceny.min()
        }
        return fig, statystyki

    def generuj_boxplot(self, df, tytul="Box‑plot cen"):
        ceny = df['cena']

        # przycięcie na 95 percentyl
        gorna_granica = np.percentile(ceny, 95)
        ceny_przyciecie = ceny[ceny <= gorna_granica]

        fig, ax = plt.subplots()
        ax.boxplot(ceny_przyciecie, vert=True)
        ax.set_title(tytul)
        ax.set_ylabel("Cena (zł)")
        return fig
