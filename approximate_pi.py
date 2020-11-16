#!/usr/bin/env python

""" Génère N_IMGS images PPM représentant le cercle issue de la
simulation de Monte-Carlo avec l'estimation de pi au centre et
une image animée gif de la succession des images ppm

TODO:
- Ajouter la superposition sur les points déjà existants (pour l'instant
on génère simplement des images différentes à chaque fois)
- Coder la fonction is_pi_text_pixel
- Version gif des ppm
- Optimiser la taille des images : format P6
"""

import simulator as simu
import sys
import subprocess
import time

N_IMGS = 10

# Différentes couleurs possibles : Hors cercle, Dans cercle, Non généré
COLORS_BIN = [bytearray(c) for c in [[0, 0, 255], [255, 0, 0], [255, 255, 255]]]

def is_pi_text_pixel(x, y, side, pi):
    """Renvoie un booléen déterminant si le pixel de coordonnées (x, y)
    est un pixel nécessaire à l'écriture du nombre pi sur l'image
    """
    #print("is_pi_text_pixel NON REDIGEE")

    return False

def generate_ppm_file(name, pts):
    """Génère une image de nom name au format ppm avec les
    points contenus dans pts (Version binaire, illisble mais legère !)

    ECRITURE DU NOMBRE PI A RAJOUTER
    """
    t1 = time.perf_counter()
    side = len(pts)

    with open(name, "wb") as f:
        # En-tête du PPM : P6 pour PPM binaire, Taille image
        f.write(bytes(f"P6 {side} {side} 255 ", encoding='utf8'))

        # Génération des points de l'image
        for pt_y in range(side):
            for pt_x in range(side):
                # Couleur du point en fonction du type
                f.write(COLORS_BIN[pts[pt_y][pt_x]])

    print("\tGenerate ppm file dt=" + str(time.perf_counter() - t1))


if __name__ == "__main__":
    if len(sys.argv) != 4 or not sum(sys.argv[i].isnumeric() for i in range(1, 4)):
        raise SyntaxError("Mauvais arguments. Usage : ./approximate_pi.py " + \
            "taille_cote nb_points precision_pi")

    side, nb_pts, precision = [int(e) for e in sys.argv[1:4]]
    print(f"Taille carré de {side} px pour {nb_pts} pts")

    t_init = time.perf_counter()
    print("Début de la génération...")

    # Tableau 2D qui contiendra les points de l'image initialisés à 2 (non générés)
    pts = [[2 for i in range(side)] for j in range(side)]

    # Génération des dix images
    pts_per_img = int(nb_pts/N_IMGS)
    for i in range(N_IMGS):
        t1 = time.perf_counter()
        approx = simu.monte_carlo_extended(pts, side, pts_per_img)

        # Génération (nom et) fichier
        pi_current_approx = "{}-{}".format(*str(approx).split("."))
        generate_ppm_file(f"img{i}_{pi_current_approx}.ppm", pts)

        print(f"Loop time i={i}, dt={time.perf_counter() - t1}")

    print(f"Fin de la génération en {time.perf_counter() - t_init} s")

    # Convertir en GIF
    cmd = f"convert -delay 4 -loop 1 *.ppm pi_{nb_pts}_{side}.gif"
    #subprocess.call(cmd.split())