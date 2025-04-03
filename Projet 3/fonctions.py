#!/usr/bin/python3
# fichier fonctions.py comprenant les fonctions utilisés 

from sense_hat import SenseHat
import time
import os
import numpy as np


# transformation lettres -> numéro 
number_dict = {
    'un': '1',
    'deux': '2',
    'trois': '3',
    'quatre': '4',
    'cinq': '5',
    'six': '6',
    'sept': '7',
    'huit': '8',
    'neuf': '9',
    'zero': '0'
}

def convert(liste):
    """Retourne la conversion d'une liste de numéro écrit en lettre en une liste de numéro (int)
    @pre: liste de string
    @post: liste de int
    """
    x = " ".join([str(nbr) for nbr in liste])
    conv = "".join(number_dict[nbr] for nbr in x.split())
    return conv

def display(sense, selection):
    """Affiche la matrice qui affiche les mesures ambiantes (Temperature, Pression, Humidité)
    et Quitter 
    @pre: selection
    @post: affiche une matrice affichant les mesures ambiantes et le bouton Quitter 
    """
    left, top, right, bottom = {
        "T": (0, 0, 4, 4),
        "P": (4, 0, 8, 4),
        "Q": (4, 4, 8, 8),
        "H": (0, 4, 4, 8),
    }[selection]
    bg = np.zeros((8, 8, 3), dtype=np.uint8)
    bg[top:bottom, left:right, :] = (255, 255, 255)
    # Construit une matrices avec la matrice de l'arriere-plan, le masque et l'avant-plan
    sense.set_pixels(
        [
            bg_pix if mask_pix else fg_pix
            for (bg_pix, mask_pix, fg_pix) in zip(
                (p for row in bg for p in row),
                (p for row in mask for p in row),
                (p for row in fg for p in row),
            )
        ]
    )

def readings(sense, param, selection, images2):
    """Suivant la selection du user, vérifie si les lectures du SenseHat
    sont conformes aux paramètres décidés
    Paramètres: Temperature : 19 - 25.5 Celsius
    Pression : 1000 - 1027 millibars
    Humidité : 30 - 60%
    @pre: dossier images se trouve dans le même dossier
    @post: Utilise la matrice LED pour afficher la conformité aux paramètres
    """
    if selection == "T":
        if param < 19 or param > 25.5:
            sense.load_image(images2[0])
        else:
            sense.load_image(images2[1])
    elif selection == "P":
        if param < 1000 or param > 1027:
            sense.load_image(images2[0])
        else:
            sense.load_image(images2[1])
    elif selection == "H":
        if param < 30 or param > 60:
            sense.load_image(images2[0])
        else:
            sense.load_image(images2[1])

def execute(sense, t, p, h, readings, selection, images):
    """Suivant la selection du user, affiche les mesures nécessaires et 
    retourne Faux pour rester dans le menu, retourne Vrai pour quitter
    @pre: dossier images se trouve dans le même dossier 
    @post: affiche avec la matrice LED les infos suivant la selection avec le joystick 
    et retourne Vrai ou Faux suivant la selection
    """
    if selection == "T":
        sense.load_image(images[0])
        time.sleep(1)
        sense.show_message("T: %.1fC" % t, 0.05, Rd)
        readings(sense, t, selection, images2)
        time.sleep(1)
    elif selection == "P":
        sense.load_image(images[2])
        time.sleep(1)
        sense.show_message("P: %.1fmbar" % p, 0.05, Gn)
        readings(sense, p, selection, images2)
        time.sleep(1)
    elif selection == "H":
        sense.load_image(images[1])
        time.sleep(1)
        sense.show_message("H: %.1f%%" % h, 0.05, Bl)
        readings(sense, h, selection, images2)
        time.sleep(1)
    elif selection == "Q":
        return True     # selection = Q : quit
    return False        # stay

def move(selection, direction):
    """Defini la manière de bouger avec le joystick suivant la selection
    du user, retourne unn dictionnaire avec les directions assignées 
    @pre: -
    @post: retourne un dictionnaire avec les directions assignées 
    """
    return {
        ("T", "right"): "P",
        ("T", "down"): "H",
        ("P", "left"): "T",
        ("P", "down"): "Q",
        ("Q", "up"): "P",
        ("Q", "left"): "H",
        ("H", "right"): "Q",
        ("H", "up"): "T",
    }.get((selection, direction), selection)

def get_cpu_temp():
    """Retourne la température du CPU du Raspberry Pi
    @pre: -
    @post: Retourne la température du CPU du Raspberry Pi
    """
    res = os.popen("vcgencmd measure_temp").readline()
    t = float(res.replace("temp=", "").replace("'C\n", ""))
    return t

def get_data(sense):
    """Prend les mesures grâce aux capteurs du SenseHat et effectue 
    des calculs pour assurer des mesures précises
    @pre: -
    @retourne la température correct, la pression et l'humidité 
    """
    t1 = sense.get_temperature_from_humidity()
    t2 = sense.get_temperature_from_pressure()
    t_cpu = get_cpu_temp()
    # calculates the real temperature compesating CPU heating
    t = (t1 + t2) / 2
    t_corr = (t - ((t_cpu - t) / 1.5)) - 5
    p = sense.get_pressure()
    h = sense.get_humidity()
    return t_corr, p, h

# Définie le chemin des images dans l'os Raspberry Pi
path = os.getcwd() + "/images/"
images = [path + "logo/" + i for i in os.listdir(path + "logo/")]
images2 = [path + "conditions/" + i for i in os.listdir(path + "conditions/")]
images3 = [path + "menu/" + i for i in os.listdir(path + "menu/")]
images4 = [path + "start/" + i for i in os.listdir(path + "start/")]
images5 = [path + "ques/" + i for i in os.listdir(path + "ques/")]
s = SenseHat()

# Couleurs de base du menu
Rd = (255, 0, 0)
Gn = (0, 255, 0)
Bl = (0, 0, 255)
Yl = (255, 255, 0)
__ = (0, 0, 0)

# Avant-plan du menu avec une matrice numpy 
fg = np.array(
    [
        [Rd, Rd, Rd, __, Gn, Gn, __, __],
        [__, Rd, __, __, Gn, __, Gn, __],
        [__, Rd, __, __, Gn, Gn, __, __],
        [__, Rd, __, __, Gn, __, __, __],
        [Bl, __, Bl, __, Yl, Yl, Yl, __],
        [Bl, Bl, Bl, __, Yl, __, Yl, __],
        [Bl, __, Bl, __, Yl, Yl, Yl, __],
        [Bl, __, Bl, __, __, __, Yl, Yl],
    ],
    dtype=np.uint8,)

# défini le masque qui est une matrice numpy 
mask = np.all(fg == __, axis=2)