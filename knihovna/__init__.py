"""Balíček bludiste: hledání nejkratší cesty v bludišti a generování bludišť.

Po importu balíčku jsou rovnou k dispozici tři hlavní věci, které uživatel
potřebuje: třída Bludiste, funkce nacti_bludiste a funkce vygeneruj_bludiste.
"""

from .bludiste import Bludiste, nacti_bludiste
from .generovani import vygeneruj_bludiste

__all__ = ["Bludiste", "nacti_bludiste", "vygeneruj_bludiste"]
