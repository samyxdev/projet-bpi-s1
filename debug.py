#!/usr/bin/env python3
"""Simple module perso permettant d'implémenter des print de
debug et de pouvoir très rapidement les désactiver
"""

DEBUG = True

def printd(debug_str):
    """Fonction affichant du texte de debug si la
    constante DEBUG est assignée à True
    """
    if DEBUG:
        print(debug_str)