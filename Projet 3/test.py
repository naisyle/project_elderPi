#!/usr/bin/python

## Modules
from sense_hat import SenseHat
import time
import os
import numpy as np
import rhasspy

## Fonctions
def display(sense, selection):
    """Affiche la "boîte" de séléction dans le menu
    @pre:
    @post: affiche la boîte de séléction comme matrice
    """
    left, top, right, bottom = {
        "T": (0, 0, 4, 4),
        "P": (4, 0, 8, 4),
        "Q": (4, 4, 8, 8),
        "H": (0, 4, 4, 8),
    }[selection]
    bg = np.zeros((8, 8, 3), dtype=np.uint8)
    bg[top:bottom, left:right, :] = (255, 255, 255)
    # Construct final pixels from bg array with non-transparent elements of
    # the menu array
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

def readings(param, selection, images2):
    """Suivant la selection du user, vérifie si les lectures du SenseHat
    sont conformes aux paramètres décidés
    Paramètres: Temperature : 19 - 25.5 Celsius
    Pression : 1000 - 1027 millibars
    Humidité : 30 - 60%

    @pre: -
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
    if selection == "T":
        sense.load_image(images[0])
        time.sleep(1)
        sense.show_message("T: %.1fC" % t, 0.05, Rd)
        readings(t, selection, images2)
        time.sleep(1)
    elif selection == "P":
        sense.load_image(images[2])
        time.sleep(1)
        sense.show_message("P: %.1fmbar" % p, 0.05, Gn)
        readings(p, selection, images2)
        time.sleep(1)
    elif selection == "H":
        sense.load_image(images[1])
        time.sleep(1)
        sense.show_message("H: %.1f%%" % h, 0.05, Bl)
        readings(h, selection, images2)
        time.sleep(1)
    else:
        return True
    return False


def move(selection, direction):
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
    res = os.popen("vcgencmd measure_temp").readline()
    t = float(res.replace("temp=", "").replace("'C\n", ""))
    return t

def get_data(sense):
    t1 = sense.get_temperature_from_humidity()
    t2 = sense.get_temperature_from_pressure()
    t_cpu = get_cpu_temp()
    # calculates the real temperature compesating CPU heating
    t = (t1 + t2) / 2
    t_corr = (t - ((t_cpu - t) / 1.5))
    p = sense.get_pressure()
    h = sense.get_humidity()
    return t_corr, p, h

## Programme
sense = SenseHat()
sense.clear()

path = os.getcwd() + "/images/"
images = [path + "logo/" + i for i in os.listdir(path + "logo/")]
images2 = [path + "conditions/" + i for i in os.listdir(path + "conditions/")]
images3 = [path + "menu/" + i for i in os.listdir(path + "menu/")]

# Menu
Rd = (255, 0, 0)
Gn = (0, 255, 0)
Bl = (0, 0, 255)
Gy = (128, 128, 128)
__ = (0, 0, 0)

fg = np.array(
    [
        [Rd, Rd, Rd, __, Gn, Gn, __, __],
        [__, Rd, __, __, Gn, __, Gn, __],
        [__, Rd, __, __, Gn, Gn, __, __],
        [__, Rd, __, __, Gn, __, __, __],
        [Bl, __, Bl, __, Gy, Gy, Gy, __],
        [Bl, Bl, Bl, __, Gy, __, Gy, __],
        [Bl, __, Bl, __, Gy, Gy, Gy, __],
        [Bl, __, Bl, __, __, __, Gy, Gy],
    ],
    dtype=np.uint8,
)

mask = np.all(fg == __, axis=2)
selection = "T"
index = 0

try:
    sense.clear()
    sense.load_image(images[0])
    while True: 
        display(sense, selection)
        t, p, h = get_data(sense)
        event = sense.stick.wait_for_event()
        if event.action == "pressed" and event.direction == "middle":
            if execute(sense, t, p, h, readings, selection, images):
                break
        else:
            selection = move(selection, event.direction)
    sense.clear()
except:
    # print("Something went wrong")
    sense.clear()
