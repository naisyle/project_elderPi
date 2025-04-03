#!/usr/bin/python

### Modules ###
from sense_hat import SenseHat
import time
import os
import numpy as np
import rhasspy
from crypto import *
from fonctions import *  # Fonctions 

### Programme ###
# Initialisation
s = SenseHat()
s.clear()
s.low_light = True
selection = "T"
count1 = -1
print("Entraînement Rhasspy en cours..")
rhasspy.train_intent_files("/home/pi/sentences.ini")
print("Entraînement réussi!")

# Initiatialisation des fichiers
try:
    fcode = open("fichiercode.txt", "r", encoding='utf-8') # teste si le fichier existe et s'il existe l'ouvre pour le lire
    fmdp = open("fichiermdp.txt", "r", encoding='utf-8')
    fliste = open("listeDeCourses.txt", "r", encoding='utf-8')
    print("fichier ouvert")
    fcode.close()
    fmdp.close()
    fliste.close()
except:
    fcode = open("fichiercode.txt", "w", encoding='utf-8')# Crée le fichier sinon
    fmdp = open("fichiermdp.txt", "w", encoding='utf-8')
    fliste = open("listeDeCourses.txt", "w", encoding='utf-8')
    print("fichier créé")
    fcode.close()
    fmdp.close()
    fliste.close()
    
# Animation de démarrage ElderPi
for i in range(5):
    s.load_image(images4[0])
    time.sleep(0.40)
    s.load_image(images4[1])
    time.sleep(0.40)
s.clear()
s.show_message("ElderPi!", scroll_speed=0.05)
s.show_letter(">")

try:
    while True:
        # Menu principal
        for event in s.stick.get_events():
            # Defile vers la droite
            if event.action == "pressed" and event.direction == "right":
                if count1 < 3:
                    count1 += 1
                else:
                    count1 -= 3
                s.load_image(images3[count1 % len(images3)])
            # Defile vers la gauche
            if event.action == "pressed" and event.direction == "left":
                if count1 < 0:
                    count1 += 4
                elif count1 == 0:
                    count1 += 3
                else:
                    count1 -= 1
                s.load_image(images3[count1 % len(images3)])
                    
            # Sub-menu du code secret
            if event.action == "pressed" and event.direction == "middle" and count1 == 0: 
                while True:
                    # Fichier non-existant
                    if os.stat("fichiercode.txt").st_size == 0:
                        s.show_letter("R")
                        rhasspy.text_to_speech("Il n'y a pas de code secret existant, voulez-vous en créer un?")
                        s.show_letter("?")
                        intent = rhasspy.speech_to_intent()
                        if intent["name"] == "Oui":
                            s.show_message("Oui", scroll_speed=0.05)
                            while True:
                                s.show_letter("R")
                                rhasspy.text_to_speech("D'accord, veuillez entrer quatre chiffres, dont un chiffre à la fois")
                                s.show_letter("?")
                                intentC = rhasspy.speech_to_intent() 
                                code = [intentC["name"]]
                                for i in range(3):
                                    intentC2 = rhasspy.speech_to_intent()
                                    code.append(intentC2["name"])
                                    convert(code)
                                s.show_letter("R")
                                rhasspy.text_to_speech("Est-ce bien {} ?".format(code))
                                s.show_letter("?")
                                intent = rhasspy.speech_to_intent()
                                if intent["name"] == "Oui":
                                    s.show_message("Oui", scroll_speed=0.05)
                                    with open("fichiercode.txt", "w", encoding='utf-8') as file:
                                        hashcode = encode("elderPi", str(code))
                                        file.write(hashcode)
                                    while True:
                                        s.show_letter("R")
                                        rhasspy.text_to_speech("Veuillez entrer trois mots de vérification pour chiffrer votre code secret")
                                        s.show_letter("?")
                                        intentMdp = rhasspy.speech_to_intent()
                                        mots = [intentMdp["name"]] 
                                        for i in range(2):
                                            intentMdp2 = rhasspy.speech_to_intent()
                                            mots.append(intentMdp2["name"])
                                        strMots = " ".join([str(nbr) for nbr in mots])
                                        s.show_letter("R")
                                        rhasspy.text_to_speech("Est-ce bien {} ?".format(strMots))
                                        s.show_letter("?")
                                        intent = rhasspy.speech_to_intent()
                                        if intent["name"] == "Oui":
                                            s.show_message("Oui", scroll_speed=0.05)
                                            with open("fichiermdp", "w", encoding='utf-8') as f:
                                                intentMdp = hashing(strMots)
                                                f.write(intentMdp)
                                            break
                                        elif intent ["name"] == "Non":
                                            s.show_message("Non!", scroll_speed=0.05)
                                            continue
                                        elif intent["name"] == "Arret":
                                            break
                                        break
                                elif intent["name"] == "Non":
                                    s.show_message("Non!", scroll_speed=0.05)
                                    continue
                                break
                        elif intent["name"] == "Non":
                            s.show_message("Non!", scroll_speed=0.05)
                            break
                        elif intent["name"] == "Arret":
                            s.show_message("Quitte le menu..", scroll_speed=0.05)
                            break
                        else:
                            continue
                    else:
                        # Fichier existant
                        s.show_letter("R")
                        rhasspy.text_to_speech("Il y a un code secret existant, voulez-vous l'écouter?")
                        s.show_letter("?")
                        intent = rhasspy.speech_to_intent()
                        if intent["name"] == "Oui":
                            s.show_message("Oui", scroll_speed=0.05)
                            while True:
                                s.show_letter("R")
                                rhasspy.text_to_speech("Veuillez entrer les trois mots de vérification")
                                s.show_letter("?")
                                intent = rhasspy.speech_to_intent()
                                motsVerif = [intent["name"]] 
                                for i in range(2):
                                    intentMdp2 = rhasspy.speech_to_intent()
                                    motsVerif.append(intentMdp2["name"])
                                strMotsVerif = " ".join([str(nbr) for nbr in motsVerif])
                                with open("fichiermdp", "r", encoding='utf-8') as f:
                                    hashcode = f.readline().strip()
                                with open("fichiercode", "r", encoding='utf-8') as file:
                                    codeSecret = decode("elderPi", file.readline().strip())
                                    if strMotsVerif == hashcode:
                                        rhasspy.text_to_speech(codeSecret)
                                        s.show_message(codeSecret)
                                        break
                                    else:
                                        rhasspy.text_to_speech("Désolé, c'est le mauvais mots de passe, veuillez réessayer")
                                        continue
                            # Conserver ou détruire code secret
                            s.show_letter("R")
                            rhasspy.text_to_speech("Voulez-vous détruire ou conserver le mot de passe?")
                            s.show_letter("?")
                            intent = rhasspy.speech_to_intent()
                            if intent["name"] == "Detruire":
                                s.show_message("Détruit!", scroll_speed=0.05)
                                with open("fichiermdp", "w", encoding='utf-8') as wipe:
                                    pass
                                break
                            elif intent["name"] == "Conserver":
                                s.show_message("Conservé", scroll_speed=0.05)
                                break
                        elif intent["name"] == "Non":
                            s.show_message("Non!", scroll_speed=0.05)
                            break
                        elif intent["name"] == "Arret":
                            s.show_message("Retourne au menu", scroll_speed=0.05)
                            break 
                                    
            # Sub-menu de la liste de courses
            if event.action == "pressed" and event.direction == "middle" and count1 == 1:  
                while True:
                    if os.stat("listeDeCourses.txt").st_size == 0:
                        s.show_letter("R")
                        rhasspy.text_to_speech("Il n'y a pas de liste existante, voulez-vous en créer une?")
                        s.show_letter("?")
                        intent = rhasspy.speech_to_intent()
                        if intent["name"] == "Oui":
                            s.show_letter("R")
                            rhasspy.text_to_speech("D'accord, veuillez entrer une quantité puis un produit, puis énoncez la commande terminer lorsque vous aurez fini votre liste")
                            while True:
                                produit = []
                                s.show_letter("?")
                                intent = rhasspy.speech_to_intent()
                                produit.append(intent["name"])
                                s.show_letter("?")
                                intent = rhasspy.speech_to_intent()
                                produit.append(intent["name"])
                                strProduit = " ".join([str(i) for i in produit])
                                with open("listeDeCourses.txt", "a", encoding='utf-8') as fileListe:
                                    fileListe.write(strProduit)
                                if intent["name"] == "Terminer":
                                    break
                                elif intent["name"] == "Quitter":
                                    break
                        elif intent["name"] == "Non":
                            s.show_message("Non!", scroll_speed=0.05)
                        elif intent["name"] == "Quitter":
                            s.show_message("Retourne au menu..", scroll_speed=0.05)
                            break
                    else:
                        s.show_letter("R")
                        rhasspy.text_to_speech("Il y a une liste existante, voulez-vous la réécouter?")
                        s.show_letter("?")
                        intent = rhasspy.speech_to_intent()
                        if intent["name"] == "Oui":
                            s.show_message("Oui", scroll_speed=0.05)
                            with open("listeDeCourses.txt", "r", encoding='utf-8') as fileListe:
                                for line in fileListe.readlines():
                                    rhasspy.text_to_speech(line)
                            s.show_letter("R")
                            rhasspy.text_to_speech("Voulez-vous détruire ou conserver la liste")
                            s.show_letter("?")
                            intent = rhasspy.speech_to_intent()
                            if intent["name"] == "Detruire":
                                s.show_message("Détruit!", scroll_speed=0.05)
                                with open("listeDeCourses.txt", "w", encoding='utf-8') as fileListe:
                                    pass
                                break
                            elif intent["name"] == "Conserver":
                                s.show_message("Conservé!", scroll_speed=0.05)
                                break
                            elif intent["name"] == "Quitter":
                                break
                        if intent["name"] == "Non":
                            s.show_message("Non!", scroll_speed=0.05)
                            break
                        
            # Sub-menu de la fonctionnalité supplémentaire
            if event.action == "pressed" and event.direction == "middle" and count1 == 2:  
                while True:
                    display(s, selection)
                    t, p, h = get_data(s)
                    for event in s.stick.get_events():
                        if event.action == "pressed":
                            if event.direction == "middle":
                                if execute(s,t,p,h,readings, selection,images): # Si selection = "Q"
                                    break
                            else:
                                selection = move(selection, event.direction)
                                
            # Eteindre l"ElderPi    
            if event.action == "pressed" and event.direction == "middle" and count1 == 3: 
                s.show_message("shutdown", text_colour=[255, 0, 0], scroll_speed=0.05)
                # Pour la démo : s.clear()
                # break
                os.system("shutdown now -h")
except:
    s.clear()   
