"""
Modul pro práci s grafem a hledání nejkratší cesty v bludišti.

Postup je ve dvou krocích:
  1) bludiště (mřížku) převede na graf = sestaví matici sousednosti,
  2) v tomto grafu najde nejkratší cestu prohledáváním do šířky (BFS).

Matici sousednosti ukládá jako řídkou (sparse) matici ze SciPy.
"""

import numpy as np
from scipy.sparse import coo_matrix
from collections import deque


def sestav_matici_sousednosti(mrizka: np.ndarray) -> tuple:
    """Z mřížky bludiště sestaví matici sousednosti a tabulku čísel buněk.

    Každé volné buňce přidělí pořadové číslo (0, 1, 2, ...). Tato čísla
    jsou vrcholy grafu. Dvě volné buňky, které spolu sousedí přes společnou
    hranu (vlevo/vpravo nebo nahoře/dole), spojí hranou grafu.

    Vrací dvojici:
      - matici sousednosti (řídká matice SciPy ve formátu CSR),
      - tabulku `cisla_bunek` stejného tvaru jako mřížka, kde je u každé
        buňky její číslo vrcholu (u zdi je -1).
    """
    pocet_radku, pocet_sloupcu = mrizka.shape

    # 1) Každé volné buňce přidělí pořadové číslo vrcholu, zdi dostanou -1.
    cisla_bunek = -np.ones(mrizka.shape, dtype=int)
    dalsi_cislo = 0
    for radek in range(pocet_radku):
        for sloupec in range(pocet_sloupcu):
            if not mrizka[radek, sloupec]:          # buňka je volná (není zeď)
                cisla_bunek[radek, sloupec] = dalsi_cislo
                dalsi_cislo += 1

    # 2) Projde všechny volné buňky a vytvoří hrany k sousedovi vpravo
    #    a dolů. Tím pokryje všechny dvojice sousedů bez opakování.
    radky_hran = []
    sloupce_hran = []
    for radek in range(pocet_radku):
        for sloupec in range(pocet_sloupcu):
            if mrizka[radek, sloupec]:              # zeď přeskočí
                continue
            for posun_radku, posun_sloupce in [(0, 1), (1, 0)]:   # vpravo, dolů
                soused_radek = radek + posun_radku
                soused_sloupec = sloupec + posun_sloupce
                # soused musí být uvnitř mřížky a musí být volný
                if soused_radek < pocet_radku and soused_sloupec < pocet_sloupcu:
                    if not mrizka[soused_radek, soused_sloupec]:
                        moje_cislo = cisla_bunek[radek, sloupec]
                        cislo_souseda = cisla_bunek[soused_radek, soused_sloupec]
                        # hranu zapíše oběma směry (graf je neorientovaný)
                        radky_hran += [moje_cislo, cislo_souseda]
                        sloupce_hran += [cislo_souseda, moje_cislo]

    # 3) Z trojic (řádek, sloupec, hodnota) sestaví řídkou matici sousednosti.
    pocet_vrcholu = dalsi_cislo
    jednicky = np.ones(len(radky_hran), dtype=int)
    matice = coo_matrix((jednicky, (radky_hran, sloupce_hran)),
                        shape=(pocet_vrcholu, pocet_vrcholu))
    return matice.tocsr(), cisla_bunek


def nejkratsi_cesta(matice, start: int, cil: int) -> list | None:
    """V grafu najde nejkratší cestu mezi dvěma vrcholy pomocí BFS.

    BFS (prohledávání do šířky) prochází graf po vrstvách, takže první nalezená
    cesta do cíle je zároveň nejkratší. U každého vrcholu si pamatuje, odkud
    do něj přišel (`predchudce`), a z toho na konci cestu zrekonstruuje.

    Vrací seznam čísel vrcholů od startu k cíli, nebo None, pokud cesta není.
    """
    pocet_vrcholu = matice.shape[0]
    navstiveno = np.zeros(pocet_vrcholu, dtype=bool)
    predchudce = -np.ones(pocet_vrcholu, dtype=int)   # -1 = "odnikud" (start)

    fronta = deque()
    fronta.append(start)
    navstiveno[start] = True

    while fronta:
        vrchol = fronta.popleft()
        if vrchol == cil:
            break
        # sousedé vrcholu = čísla sloupců s nenulou v jeho řádku matice
        for soused in matice.getrow(vrchol).indices:
            if not navstiveno[soused]:
                navstiveno[soused] = True
                predchudce[soused] = vrchol
                fronta.append(soused)

    if not navstiveno[cil]:
        return None

    # Cestu zrekonstruuje od cíle pozpátku přes předchůdce a otočíme ji.
    cesta = []
    vrchol = cil
    while vrchol != -1:
        cesta.append(vrchol)
        vrchol = predchudce[vrchol]
    cesta.reverse()
    return cesta


def najdi_cestu(mrizka: np.ndarray) -> list | None:
    """Najde nejkratší cestu z levého horního do pravého dolního rohu.

    Spojuje oba kroky dohromady: sestaví graf a najde v něm cestu. Čísla
    vrcholů na konci převede zpět na souřadnice (řádek, sloupec) v bludišti.

    Vrací seznam souřadnic [(r, s), ...] od vstupu k výstupu, nebo None.
    """
    matice, cisla_bunek = sestav_matici_sousednosti(mrizka)
    pocet_radku, pocet_sloupcu = mrizka.shape

    start = cisla_bunek[0, 0]                       # levý horní roh = vstup
    cil = cisla_bunek[pocet_radku - 1, pocet_sloupcu - 1]   # pravý dolní = výstup
    if start == -1 or cil == -1:                    # vstup nebo výstup je zeď
        return None

    cesta_cisla = nejkratsi_cesta(matice, start, cil)
    if cesta_cisla is None:
        return None

    # Připraví si převod: číslo vrcholu -> souřadnice (řádek, sloupec).
    souradnice_podle_cisla = {}
    for radek in range(pocet_radku):
        for sloupec in range(pocet_sloupcu):
            cislo = cisla_bunek[radek, sloupec]
            if cislo != -1:
                souradnice_podle_cisla[cislo] = (radek, sloupec)

    cesta = []
    for cislo in cesta_cisla:
        cesta.append(souradnice_podle_cisla[cislo])
    return cesta
