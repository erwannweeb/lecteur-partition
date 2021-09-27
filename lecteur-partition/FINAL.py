from fonctions import sound, lire, play, Tab_partition_et_durer, partitions_ouvrir, nb_ligne_par, Creation_partition, affiche_nom_morceau, choix_note_et_afficher, ecriture_partition, inversion, chiffre_note, note_chiffre, partition_crea, transposition, ChaineDeMarkov, txt_ouvrir, ecriture_txt, enter_txt, durer_chiffre
import numpy as np
import os
import turtle as tr
import random


# Dictionnaire :
#Note
Note_freq = {0:38, 1:264, 2:297, 3:330, 4:352, 5:396, 6:440, 7:495}
Num_note = {"Z":0,"DO":1, "RE":2, "MI":3, "FA":4, "SOL":5, "LA":6, "SI":7, "p":8}
note_data = ["Z","DO","RE","MI","FA","SOL","LA","SI","p"]

#Durée
Durer_dur = {0:125, 1:250, 2:500, 3:1000, 4:187.5, 5:375, 6:750, 7:1500}
Num_durer = {"c":0, "n":1, "b":2, "r":3, "cp":4, "np":5, "bp":6, "rp":7}
Durer_num = {0:"c", 1:"n", 2:"b", 3:"r", 4:"cp", 5:"np", 6:"bp", 7:"rp"}
durer_data = ["c","n","b","r","cp","np","bp","rp"]

affichagepiano = [ "piano.png","pianor.png", "pianoo.png","pianoj.png", "pianovc.png", "pianovf.png", "pianob.png", "pianov.png"]

#Demander a l'utilisateur se qu'il veut faire
while 1:
    choix = input("\nBonjour, que souhaitez vous faire ? : \n1) Lire une partition\n2) Créer une nouvelle partition\n3) Ajouter une nouvelle partition\n4) Appliquer une transposition ou une inversion\n5) Créer une nouvelle partition de façon procédural\n")
    while choix != "1" and choix != "2" and choix != "3" and choix != "4" and choix != "5":
        choix = input("Je n'ai pas compris votre requête, que souhaitez vous faire ? : \n1) Lire une partition\n2) Créer une nouvelle partition\n3) Ajouter une nouvelle partition\n4) Appliquer une transposition ou une inversion\n5) Créer une nouvelle partition de façon procédural\n")

    # Chargés les partitions (le fichier partition.txt)
    partitions = partitions_ouvrir()
    nb_lignes = nb_ligne_par()


    if choix == "1":
        # DEBUT

        # Afficher le nom des morceaux
        affiche_nom_morceau(nb_lignes, partitions)

        # Setup pour l'affichage graphique
        tr.setup(860, 536)
        tr.title("Affichage piano")
        tr.bgpic("piano.png")
        tr.hideturtle()

        # Demander a l'utilisateur se qu'il veut faire
        choix_2 = int(tr.numinput("Choix Partition", "Veuillez choisir le numéro de la partition à jouer"))
        while (choix_2 > (int(nb_lignes) / 2) or choix_2 < 0):
            choix_2 = int(tr.numinput("Choix Partition", "Je n'ai pas compris, la quelle souhaitez vous jouer ? :"))

        # On recupère la partition et on l'affiche avec son nom
        VAR = choix_note_et_afficher(partitions, choix_2)

        # On transforme la partition en deux tableau distinct les notes et les durée
        partition = Tab_partition_et_durer(VAR)
        durer = partition[1]
        note = partition[0]

        # On joue le morceau
        play(note, durer)

        # FIN


    elif choix == "2":
        # DEBUT

        # Nombre de note de la partition
        nb = int(input("Combien de notes dans votre partition ? : "))
        while nb < 1:
            nb = int(input("Combien de notes dans votre partition ? : "))

        # Création de la partition
        lecture = Creation_partition(nb)

        # On nomme la partition et on l'ecrit dans le .txt
        nom = input("Donner un nom à votre partition : ")
        ecriture_partition(lecture, nom, nb_lignes)

        # On affiche le .txt
        lire()

        # FIN


    elif choix == "3":
        #DEBUT

        # Demander a l'utilisateur se quelle fichier il veut importer
        nom = input("Quel est le nom du fichier .txt que vous voulez ajouter a la base de données ? (Vérifiez que le fichier .txt soit bien au même endroit que le fichier python):\n")

        #Recupérer l'endroit ou est le fichier .txt a importer
        OS = os.getcwd()
        nom_complet = OS + '\\' + nom

        # Chargés les partitions
        nouveau = txt_ouvrir(nom_complet)

        # Ecriture du txt dans partition.txt
        for nb in range(0, len(nouveau)):
            nb_lignes = nb_ligne_par()
            ligne = enter_txt(nouveau, nb)
            ecriture_txt(ligne, nb_lignes, nb)

        # On affiche le .txt
        lire()

        #FIN


    elif choix == "4":
        #DEBUT

        # Afficher le nom des morceaux
        affiche_nom_morceau(nb_lignes, partitions)

        # Demander a l'utilisateur se qu'il veut faire
        choix_2 = int(input("Quel est le numéro de la partition que vous voulez modifier ? : "))
        while (choix_2 > (int(nb_lignes) / 2) or choix_2 < 1):
            choix_2 = int(input("Je n'ai pas compris, laquelle souhaitez-vous modifier ? :"))

        # On recupère la partition et on l'affiche avec son nom
        VAR = choix_note_et_afficher(partitions, choix_2)

        # Demander a l'utilisateur se qu'il veut faire
        choix_3 = int(input("Comment voulez-vous modifier la modifier ? :\n1) Inversion\n2) Transposition\n"))
        while ((choix_3 != 1) and (choix_3 != 2)):
            choix_3 = int(input("Je n'ai pas compris, comment voulez-vous modifier la modifier ? :\n1) Inversion\n2) Transposition\n"))

        # On transfome la partition en deux tableau distinct les notes et les durée
        partition = Tab_partition_et_durer(VAR)
        durer = partition[1]
        note = partition[0]

        # On transfome les notes en chiffre
        note = chiffre_note(note)

        if choix_3 == 1:
            #DEBUT

            # On inverse les chiffres
            note = inversion(note, max(note))

            # FIN

        if choix_3 == 2:
            # DEBUT

            nb = int(input("De combien voulez-vous transposer ? :\n"))
            note = transposition(note, nb)

            # FIN

        # On transfome chiffre en note
        note = note_chiffre(note)

        # On crée une partition a partir de note et durer
        lecture = partition_crea(note, durer)

        # On nomme la partition et on l'ecrit dans le .txt
        nom = input("Donnez un nom à votre partition : ")
        ecriture_partition(lecture, nom, nb_lignes)

        # On affiche le .txt
        lire()


        #FIN


    elif choix == "5":
        #DEBUT

        Partitions_T, NbrPartition, LengthPart = [], 0, 0

        while LengthPart <= 0:
            LengthPart = int(input("Veuillez saisir une longueur de partition supérieur à 0 : "))
        while NbrPartition <= 0:
            NbrPartition = int(input("Combien de partitions voulez-vous ajouter ? : "))

            # Afficher le nom des morceaux
            affiche_nom_morceau(nb_lignes, partitions)

            if NbrPartition == 1:
                choix_2 = int(input("Veuillez saisir le numéro de la partition : "))

                # CHERCHER LA PARTITION ET CONVERTIR SES NOTES
                VAR = choix_note_et_afficher(partitions, choix_2)
                partition = Tab_partition_et_durer(VAR)
                pause = partition[1]
                note = partition[0]
                note = chiffre_partition(note)

                Partitions_T.extend(note)  # AJOUTER TOUTES LES NOTES

            elif NbrPartition >= 1:
                for x in range(NbrPartition):
                    choix_2 = int(input("Veuillez saisir le numéro d'une partition : "))

                    # CHERCHER LA PARTITION ET CONVERTIR SES NOTES
                    VAR = choix_note_et_afficher(partitions, choix_2)
                    partition = Tab_partition_et_durer(VAR)
                    pause = partition[1]
                    note = partition[0]
                    note = chiffre_partition(note)

                    Partitions_T.extend(note)  # AJOUTER TOUTES LES NOTES

            else:
                print("Erreur dans votre demande")

        #Chaine de Markov
        note = ChaineDeMarkov(Partitions_T, LengthPart)

        # Création d'un tableau de durer randomiser de la meme longeur que le tableau note
        durer = []
        for x in range(0, LengthPart):
            durer.append(random.randint(0,7))

        # Transformation chiffre -> note/ durer
        durer = durer_chiffre(durer)
        note = partition_chiffre(note)

        # On crée une partition a partir de note et durer
        lecture = partition_crea(note, durer)

        # On nomme la partition et on l'ecrit dans le .txt
        nom = input("Donnez un nom à votre partition : ")
        ecriture_partition(lecture, nom, nb_lignes)

        # On affiche le .txt
        lire()

         #FIN