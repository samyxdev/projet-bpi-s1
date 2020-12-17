#!/usr/bin/env python3

""" Génère N_IMGS images PPM représentant le cercle issue de la
simulation de Monte-Carlo avec l'estimation de pi au centre et
une image animée gif de la succession des images ppm

Stats d'occupation en mémoire
/usr/bin/time -v ./approximate_pi.py 800 1000000 5

"""

import sys
import subprocess
import time
import simulator as simu

from debug import printd

N_IMGS = 10

# Différentes couleurs possibles : Hors cercle, Dans cercle, Non généré
COLORS_BIN = [bytearray(c) for c in [[0, 0, 255], [255, 0, 0], [255, 255, 255]]]

def generate_ppm_file(pts_list, approx_value, ind):
    """Génère une image de nom spécifié ci-dessous au format ppm avec les
    points contenus dans pts_list (Version binaire, illisble mais legère !)
    Renvoie également le nom du fichier crée

    Arguments:
    pts_list: Liste des points de l'image
    size: taille côté de l'image (pour placement texte)
    approx: approximation actuelle de pi
    ind: index de l'image (pour le nom)
    """
    ti_generate = time.perf_counter()

    # Formattage du nom de l'image
    approx_name = "{}-{}".format(*str(approx_value).split("."))
    name = f"img{ind}_{approx_name}.ppm"

    # Pour que la position du texte soit bien adaptée à la taille de l'image
    pos_ctr = side // 2
    proc = subprocess.Popen(f"ppmlabel -x {pos_ctr - 150} -y {pos_ctr + 15} " + \
        f"-color \"black\" -size 50 -text {approx_value} > {name}",
    shell=True, stdin=subprocess.PIPE)

    printd("Communicating file stream to ppmlabel...")
    proc.stdin.write(bytes(f"P6\n{side} {side}\n 255\n", encoding='utf8'))

    for pt_y in range(side):
        for pt_x in range(side):
            # Couleur du point en fonction du type
            proc.stdin.write(COLORS_BIN[pts_list[pt_y][pt_x]])

    # "Vide" le tampon d'entrée standard qu'on a rempli avec l'image
    proc.stdin.flush()

    printd("\tGenerate ppm file dt=" + str(time.perf_counter() - ti_generate))

    return name


if __name__ == "__main__":
    if len(sys.argv) != 4 or not sum(sys.argv[i].isnumeric() for i in range(1, 4)):
        raise SyntaxError("Mauvais arguments. Usage : ./approximate_pi.py " + \
            "taille_cote nb_points precision_pi")

    side, nb_pts, precision = [int(e) for e in sys.argv[1:4]]
    printd(f"Taille carré de {side} px pour {nb_pts} pts")

    t_init = time.perf_counter()
    printd("Début de la génération...")

    # Tableau 2D qui contiendra les points de l'image initialisés à 2 (non générés)
    pts = [[2 for i in range(side)] for j in range(side)]

    # Génération des dix images
    img_filename_list = [] # Liste des fichiers crées
    pts_per_img = int(nb_pts/N_IMGS)
    for i in range(N_IMGS):
        t1 = time.perf_counter()
        approx = simu.monte_carlo_extended(pts, side, pts_per_img)

        printd("\tApprox " + str(approx))

        # Génération (nom et) fichier
        img_filename_list.append(generate_ppm_file(pts, approx, i))

        printd(f"Loop time i={i}, dt={time.perf_counter() - t1}")

    tf_gen = time.perf_counter()
    printd(f"Fin de la génération en {tf_gen - t_init} s")

    #Conversion en GIF des fichiers générés pendant cette exécution
    cmd = f"convert -delay 50 -loop 1 {' '.join(img_filename_list)} pi_{nb_pts}_{side}.gif"
    subprocess.call(cmd, shell=True)

    printd(f"Fin de la conversion en Gif en {time.perf_counter() - tf_gen}s")
    print(f"Temps total d'exécution : {time.perf_counter() - t_init}s")
