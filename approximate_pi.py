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

def generate_ppm_file(pts, size, approx, ind):
    """Génère une image de nom spécifié ci-dessous au format ppm avec les
    points contenus dans pts (Version binaire, illisble mais legère !)

    Arguments:
    pts: Liste des points de l'image
    size: taille côté de l'image (pour placement texte)
    approx: approximation actuelle de pi
    ind: index de l'image (pour le nom)
    """
    t1 = time.perf_counter()
    side = len(pts)

    # Formattage du nom de l'image
    approx_name = "{}-{}".format(*str(approx).split("."))
    name = f"img{ind}_{approx_name}.ppm"

    with open(name + "tmp", "wb") as f:
        # En-tête du PPM : P6 pour PPM binaire, Taille image
        f.write(bytes(f"P6 {side} {side} 255 ", encoding='utf8'))

        # Génération des points de l'image
        for pt_y in range(side):
            for pt_x in range(side):
                # Couleur du point en fonction du type
                f.write(COLORS_BIN[pts[pt_y][pt_x]])

    # Ajouter l'approximation de pi à l'image au centre en noir
    pos_ctr = size // 2
    subprocess.run(f"cat {name}tmp | ppmlabel -x {pos_ctr} -y {pos_ctr} -color black -text \"{approx}\" > {name}")
    subprocess.run(f"rm *.ppmtmp")

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
        generate_ppm_file(pts, side, approx, i)

        print(f"Loop time i={i}, dt={time.perf_counter() - t1}")

    tf_gen = time.perf_counter()
    print(f"Fin de la génération en {tf_gen - t_init} s")

    # Convertir en GIF en ajoutant les approximations de pi à chaque frame
    cmd = f"convert -delay 4 -loop 1 *.ppm pi_{nb_pts}_{side}.gif"
    #subprocess.call(cmd.split())

    print(f"Fin de la conversion en Gif en {time.perf_counter() - tf_gen}s")