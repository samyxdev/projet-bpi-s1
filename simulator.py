#!/usr/bin/env python
"""Script donnant une approximation de Pi en utilisant la méthode de Monte-Carlo
"""

import sys
import random as rd
import time

def monte_carlo(n_pts):
    """Méthode de Monte-Carlo sur n_pts points retournant une
    valeur approchée de pi"""

    in_circle_counter = 0

    for _ in range(n_pts):
        in_circle_counter += int((rd.uniform(-1, 1)**2 + rd.uniform(-1, 1)**2) <= 1)

    return in_circle_counter/n_pts*4

def monte_carlo_extended(pts, side, n_pts):
    """Détermine une approximation de pi via la méthode de Monte-Carlo
    basée sur n_pts, pour un cercle de diamètre side//2 et dont les points
    sont ajoutés à pts

    Retour: approximation_pi
    Chaque point a pour valeur (0 pour hors cercle, 1 dans cercle, 2 non généré)
    """
    t1 = time.perf_counter()
    in_circle_counter = 0
    radius = side // 2
    radius_sq = radius**2

    # Compteur de pixels réecrits
    deb_rewrite = 0

    # Génération des points
    for _ in range(n_pts):
        ptx, pty = rd.randrange(0, side - 1), rd.randrange(0, side - 1)

        # Si ce point n'a pas encore été généré, on vérifie l'appartenance au cercle
        if pts[ptx][pty] == 2:
            # Plus rapide que la norme euclidienne
            #pts[ptx][pty] = abs(ptx - radius) + abs(pty - radius) <= radius
            pts[ptx][pty] = int(((ptx - radius)**2 + (pty - radius)**2) <= radius_sq)

        # Sinon, on a pas besoin d'y toucher
        else:
            deb_rewrite += 1

        in_circle_counter += pts[ptx][pty]

    print("\tMontecarlo extended dt=" + str(time.perf_counter() - t1))
    print("\tRewritten pixels=" + str(deb_rewrite))

    return in_circle_counter/n_pts*4

if __name__ == "__main__":
    if len(sys.argv) != 2 or not sys.argv[1].isnumeric():
        raise SyntaxError("Mauvais arguments. Usage : ./simulator.py nb_points")

    print(monte_carlo(int(sys.argv[1])))
