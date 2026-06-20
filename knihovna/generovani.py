"""
Modul pro generování bludišť.

Generátor vždy začne z nějaké šablony (předdefinovaný tvar zdí) a poté
přidává náhodné zdi. Po každém přidání zkontroluje, že bludiště má pořád
řešení (existuje cesta z rohu do rohu). Pokud by zeď cestu zazdila, vrátí
ji zpět. Výsledné bludiště má proto vždy řešení.
"""

import numpy as np

from . import graf


def sablona_prazdna(rozmer: int) -> np.ndarray:
    """Vrátí prázdné bludiště bez zdí (samé volné buňky)."""
    return np.zeros((rozmer, rozmer), dtype=bool)


def sablona_slalom(rozmer: int) -> np.ndarray:
    """Vrátí bludiště se zdmi, které nutí cestu klikatit se do tvaru S.

    Každý třetí řádek je celý zeď, ale na střídačku se v něm nechá mezera
    jednou vpravo a jednou vlevo. Cesta tak musí stále přebíhat ze strany
    na stranu (slalom).
    """
    mrizka = np.zeros((rozmer, rozmer), dtype=bool)
    poradi = 0
    for radek in range(3, rozmer - 1, 3):
        mrizka[radek, :] = True            # celý řádek udělá zdi
        if poradi % 2 == 0:
            mrizka[radek, -1] = False       # mezera vpravo
        else:
            mrizka[radek, 0] = False        # mezera vlevo
        poradi += 1
    return mrizka


def vygeneruj_bludiste(rozmer: int, sablona: str = "prazdna",
                       hustota_zdi: float = 0.5) -> np.ndarray:
    """Vytvoří náhodné bludiště, které má vždy řešení.

    Parametry:
      - rozmer: počet řádků i sloupců (bludiště je čtvercové),
      - sablona: výchozí tvar, "prazdna" nebo "slalom",
      - hustota_zdi: cílový podíl zdí (0.0 až 1.0), např. 0.5 = zhruba půl zdí.

    Vrací mřížku True/False (True = zeď).
    """
    # 1) Začne zvolenou šablonou.
    if sablona == "slalom":
        mrizka = sablona_slalom(rozmer)
    else:
        mrizka = sablona_prazdna(rozmer)

    generator = np.random.default_rng()
    cilovy_pocet_zdi = int(rozmer * rozmer * hustota_zdi)
    # Pojistka proti nekonečnému cyklu, kdyby už další zeď nešlo přidat.
    maximalni_pokusy = rozmer * rozmer * 10
    pokusy = 0

    # 2) Přidává náhodné zdi, dokud nedosáhne cílového počtu (nebo limitu).
    while mrizka.sum() < cilovy_pocet_zdi and pokusy < maximalni_pokusy:
        pokusy += 1
        radek = generator.integers(0, rozmer)
        sloupec = generator.integers(0, rozmer)

        # Vstup (levý horní roh) a výstup (pravý dolní roh) musí zůstat volné.
        roh_vstup = (radek == 0 and sloupec == 0)
        roh_vystup = (radek == rozmer - 1 and sloupec == rozmer - 1)
        if roh_vstup or roh_vystup or mrizka[radek, sloupec]:
            continue

        # Zkusmo postaví zeď a ověří, že bludiště má pořád řešení.
        mrizka[radek, sloupec] = True
        if graf.najdi_cestu(mrizka) is None:
            mrizka[radek, sloupec] = False     # zeď by cestu zazdila -> zrušíme

    return mrizka
