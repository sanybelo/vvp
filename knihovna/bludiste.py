"""
Hlavní modul balíčku: třída Bludiste a pomocné funkce pro načtení
bludiště ze souboru a pro jeho vykreslení do obrázku.
"""

import os

import numpy as np
import matplotlib.pyplot as plt

from . import graf


def nacti_bludiste(cesta_k_souboru: str) -> np.ndarray:
    """Načte bludiště z CSV souboru a vrátí mřížku True/False.

    CSV obsahuje čísla oddělená čárkami: 1 = zeď, 0 = volno. Funkce čísla
    načte a převede na mřížku logických hodnot, kde True znamená zeď
    (neprůchozí buňka) a False znamená volnou buňku.
    """
    cisla = np.loadtxt(cesta_k_souboru, delimiter=",", dtype=int)
    mrizka = (cisla == 1)
    return mrizka


def vykresli_bludiste(mrizka: np.ndarray, cesta, cesta_k_souboru: str) -> None:
    """Uloží obrázek bludiště do souboru.

    Barvy odpovídají zadání: zeď je černá, volná buňka bílá a nejkratší
    cesta (pokud je zadaná) je červená. Cesta je seznam souřadnic, nebo None.
    """
    pocet_radku, pocet_sloupcu = mrizka.shape

    # Začíná s celým obrázkem bílým (hodnota [1, 1, 1] = bílá v RGB).
    obrazek = np.ones((pocet_radku, pocet_sloupcu, 3))
    obrazek[mrizka] = [0, 0, 0]                 # zdi obarvíme černě
    if cesta is not None:
        for radek, sloupec in cesta:
            obrazek[radek, sloupec] = [1, 0, 0]  # cestu obarvíme červeně

    # Pokud cílová složka ještě neexistuje, vytvoří ji (jinak by uložení spadlo).
    slozka = os.path.dirname(cesta_k_souboru)
    if slozka:
        os.makedirs(slozka, exist_ok=True)

    plt.imshow(obrazek)
    plt.savefig(cesta_k_souboru)
    plt.close()


class Bludiste:
    """Bludiště jako čtvercová mřížka, které umí najít a vykreslit cestu.

    Bludiště je samotný objekt a funkce, které s ním pracují, jsou jeho
    metody. Uvnitř si drží mřížku
    True/False (True = zeď).
    """

    def __init__(self, mrizka: np.ndarray) -> None:
        """Vytvoří bludiště z hotové mřížky (True = zeď, False = volno)."""
        self.mrizka: np.ndarray = mrizka

    def rozmer(self) -> int:
        """Vrátí počet řádků (a zároveň sloupců) bludiště."""
        return self.mrizka.shape[0]

    def najdi_cestu(self) -> list | None:
        """Najde nejkratší cestu jako seznam souřadnic, nebo None."""
        return graf.najdi_cestu(self.mrizka)

    def existuje_cesta(self) -> bool:
        """Zjistí, zda v bludišti existuje cesta od vstupu k výstupu."""
        return self.najdi_cestu() is not None

    def uloz_obrazek(self, cesta_k_souboru: str, cesta=None) -> None:
        """Uloží obrázek bludiště (a volitelně cesty) do souboru."""
        vykresli_bludiste(self.mrizka, cesta, cesta_k_souboru)

    def __str__(self) -> str:
        """Krátký textový popis bludiště (použije se např. ve funkci print)."""
        return f"Bludiště {self.rozmer()}x{self.rozmer()}"
