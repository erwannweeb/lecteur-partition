import numpy as np
import simpleaudio as sa
from random import *
import turtle as tr

# Dictionnaire :
#Note
Note_freq = {0:38, 1:264, 2:297, 3:330, 4:352, 5:396, 6:440, 7:495}
Num_note = {"Z":0,"DO":1, "RE":2, "MI":3, "FA":4, "SOL":5, "LA":6, "SI":7, "p":8}
Note_num = {0:"Z", 1:"DO", 2:"RE", 3:"MI", 4:"FA", 5:"SOL", 6:"LA", 7:"SI", 8:"p"}
note_data = ["Z","DO","RE","MI","FA","SOL","LA","SI","p"]

#Durée
Durer_dur = {0:125, 1:250, 2:500, 3:1000, 4:187.5, 5:375, 6:750, 7:1500}
Num_durer = {"c":0, "n":1, "b":2, "r":3, "cp":4, "np":5, "bp":6, "rp":7}
Durer_num = {0:"c", 1:"n", 2:"b", 3:"r", 4:"cp", 5:"np", 6:"bp", 7:"rp"}
durer_data = ["c","n","b","r","cp","np","bp","rp"]


def sound(freq, duration):
    sample_rate = 44100
    t = np.linspace(0, duration, int(duration*sample_rate), False)

    freq_tierce_maj = freq * (81 / 64)
    freq_quinte = freq * (3 / 2)
    tone = np.sin(freq * t * (6) * np.pi)
    tone += np.sin(freq_tierce_maj * t * (6) * np.pi)
    tone += np.sin(freq_quinte * t * (6) * np.pi)
    tone *= 8388607 / np.max(np.abs(tone))
    tone = tone.astype(np.int32)

    i = 0
    byte_array = []
    for b in tone.tobytes():
      if i % 4 != 3:
          byte_array.append(b)
      i += 1
    audio = bytearray(byte_array)

    play_obj = sa.play_buffer(audio, 1, 3, sample_rate)
    play_obj.wait_done()
    return



# On transfome une partition en deux tableau distinct les notes et les durée
def Tab_partition_et_durer(VAR):
    # Variable
    Tab = []
    MAJ = []
    note = []
    durer = []
    ct = 0

    # Création MAJ = lettre majuscule ou p et pause = (lettre miniuscule sauf p) soit les pause
    for x in range(0, len(VAR)):
        Tab.append(VAR[x])
        if ((ord(Tab[x]) >= int(ord("A"))) and (ord(Tab[x]) <= int(ord("Z")))) or (ord(Tab[x]) == int(ord("p"))):
            MAJ.append(Tab[x])
        if ((ord(Tab[x]) >= int(ord("a"))) and (ord(Tab[x]) <= int(ord("z")))) and (ord(Tab[x]) != int(ord("p"))):
            durer.append(Tab[x])

    # Création partition = note crée a partir de MAJ
    note = creation_note(MAJ, note)

    # Gestion p -> augmentation des durées en fonction
    partition = Gestion_p(note, durer, ct)
    durer = partition[1]
    note = partition[0]

    return(note, durer)


def creation_note(MAJ, note):
    # Création partition = note crée a partir de MAJ
    for x in range(0, len(MAJ)):
        if (ord(MAJ[x]) == int(ord("D"))) and (ord(MAJ[x + 1]) == int(ord("O"))):
            note.append("DO")
        if (ord(MAJ[x]) == int(ord("R"))) and (ord(MAJ[x + 1]) == int(ord("E"))):
            note.append("RE")
        if (ord(MAJ[x]) == int(ord("M"))) and (ord(MAJ[x + 1]) == int(ord("I"))):
            note.append("MI")
        if (ord(MAJ[x]) == int(ord("F"))) and (ord(MAJ[x + 1]) == int(ord("A"))):
            note.append("FA")
        if (ord(MAJ[x]) == int(ord("S"))) and (ord(MAJ[x + 1]) == int(ord("O"))) and (ord(MAJ[x + 2]) == int(ord("L"))):
            note.append("SOL")
        if x != len(MAJ) - 1:  # eviter erreur
            if (ord(MAJ[x]) == int(ord("L"))) and (ord(MAJ[x + 1]) == int(ord("A"))):
                note.append("LA")
        if (ord(MAJ[x]) == int(ord("S"))) and (ord(MAJ[x + 1]) == int(ord("I"))):
            note.append("SI")
        if (ord(MAJ[x]) == int(ord("Z"))):
            note.append("Z")
        if (ord(MAJ[x]) == int(ord("p"))):
            note.append("p")
    return note


def Gestion_p(note, durer, ct) :
    for x in range(0, len(note)):
        if note[x - ct] == "p":
            note.remove("p")
            ct += 1
            if durer[x - ct] == "c":
                durer[x - ct] = "cp"
            elif durer[x - ct] == "n":
                durer[x - ct] = "np"
            elif durer[x - ct] == "b":
                durer[x - ct] = "bp"
            elif durer[x - ct] == "r":
                durer[x - ct] = "rp"
    return (note, durer)



# Création d'une partition en collaboration avec l'utilisateur
def Creation_partition(nb):
    # Variable
    note = []
    durer = []
    lecture = []
    ct = 0
    no = 0

    # DEBUT

    for x in range(0, nb):

        # Ajout Note
        if ((x == 0) or (no == 1)):
            note.append(input("Donner moi la note n°" + str(x + 1) + " a jouer (Z,DO,RE,MI,FA,SOL,LA,SI): "))
            while ((note[x - ct] not in note_data) or (note[x - ct] == "p")):
                note[x - ct] = input("Donner moi la note n°" + str(x + 1) + " a jouer (Z,DO,RE,MI,FA,SOL,LA,SI): ")
            no = 0
        else:
            note.append(input("Donner moi la note n°" + str(x + 1) + " a jouer (Z,DO,RE,MI,FA,SOL,LA,SI,p): "))
            while note[x - ct] not in note_data:
                note[x - ct] = input("Donner moi la note n°" + str(x + 1) + " a jouer (Z,DO,RE,MI,FA,SOL,LA,SI,p): ")

        # Ajout Durée
        if note[x - ct] != "p":
            durer.append(input("Donner moi la durée de la note n°" + str(x + 1) + "(c,n,b,r): "))
            while durer[x - ct] not in durer_data:
                durer[x - ct] = input("Donner moi la durée de la note n°" + str(x + 1) + "(c,n,b,r): ")

        # Creation lecture
        if note[x - ct] == "p":
            lecture.append(note[x - ct] + " ")
            note.remove("p")
            ct += 1
            no = 1
        else:
            lecture.append(note[x - ct] + durer[x - ct] + " ")

    return(lecture)



#Ouvrir la partition
def partitions_ouvrir():
    file = open("partition.txt", "r", encoding='UTF_8')
    partitions = file.readlines()
    return partitions


#Nb_ligne de la partition
def nb_ligne_par():
    file = open("partition.txt", "r", encoding='UTF_8')
    partitions = file.readlines()
    nb_lignes = len(partitions)
    return nb_lignes


#Ouvrir les fichier .txt
def txt_ouvrir(nom):
    file = open(nom, "r", encoding='UTF_8')
    partitions = file.readlines()
    for ligne in partitions:
        print (ligne)
    return partitions


# ecrire dans fichier partition.txt nom+partition importer
def ecriture_txt(nouveau, nb_lignes, nb):
    file = open("partition.txt", "a", encoding='UTF_8')
    if nb == 0:
        file.write("\n")
    if (nb/2) == (nb//2):
        file.write("#" + str(round(nb_lignes / 2) + 1) + " " + nouveau)
    else:
        file.write(nouveau)
    file.close()

#Affichage des nom des morceaux
def affiche_nom_morceau(nb_lignes, partitions):
    nb_lignes = nb_lignes - (nb_lignes % 2)
    ligne = 0
    while ligne < nb_lignes:
        print(partitions[ligne])
        ligne = ligne + 2

# Choix partition + affichage de cette partition et de son nom
def choix_note_et_afficher(partitions, choix):
    VAR = partitions[choix * 2 - 1]
    print(partitions[choix * 2 - 2])
    print(VAR)
    return VAR


#lire fichier partition.txt
def lire():
    file = open("partition.txt", "r", encoding='UTF_8')
    partitions = file.readlines()
    for ligne in partitions:
        print (ligne)

# Lecture son + affichage graphique
affichagepiano = ["pianor.png", "pianoo.png","pianoj.png", "pianovc.png", "pianovf.png", "pianob.png", "pianov.png", "piano.png"]
def play(note, durer):
    for x in range(1, len(note)):
        tr.bgpic(affichagepiano[Num_note[note[x]]-1])
        sound((Note_freq[Num_note[note[x-1]]]), (Durer_dur[Num_durer[durer[x-1]]]) / 1000)
        tr.hideturtle()
    tr.exitonclick()


# ecrire dans fichier partition.txt nom +partition
def ecriture_partition(lecture, nom, nb_lignes):
    file = open("partition.txt", "a", encoding='UTF_8')
    file.write("\n")
    file.write("#"+ str(round(nb_lignes/2)+1)+ " "+ nom)
    file.write("\n")
    for ligne in lecture:
        file.write(ligne)
    file.close()


# Crée des chose entrable dans partition.txt à parti d'autre .txt
def enter_txt(nouveau, nb):
    VAR = nouveau[nb]
    return VAR



#Tranformation durer -> chiffre
def chiffre_durer(durer):
    for x in range(0, len(durer)):
        durer[x] = Num_durer[durer[x]]
    return(durer)

#Tranformation chiffre -> durer
def durer_chiffre(durer):
    for x in range(0, len(durer)):
        durer[x] = Durer_num[durer[x]]
    return(durer)


#Tranformation note -> chiffre
def chiffre_note(note):
    for x in range(0, len(note)):
        note[x] = Num_note[note[x]]
    return(note)

#Tranformation chiffre -> note
def note_chiffre(note):
    for x in range(0, len(note)):
        note[x] = Note_num[note[x]]
    return(note)


#Inversion
def inversion(Partition, maxi):
    PartINV = Partition
    maxi = maxi + 1

    for x in range(len(Partition)):
        PartINV[x] = (maxi - Partition[x])
        while PartINV[x] >= maxi : #modulo hauteur de la partition
            PartINV[x] -= maxi
    return PartINV



#Transposition
def transposition(Partition, k = 5): #Fonction qui permet de rajouter une valeur k à toute la partition
    PartTNSP = Partition
    maxi = max(Partition) + 1

    for x in range(len(Partition)): #Parcours l'ensemble de la partition
        PartTNSP[x] =  Partition[x] + k #Transposition
        while PartTNSP[x] >= maxi: #modulo hauteur de la partition
            PartTNSP[x] = PartTNSP[x] - maxi

    return PartTNSP



#Utilisation chaine

def ChaineDeMarkov(ListePartition, LengthPart): #Fonction qui permet de créer une nouvelle partition grâce à la méthode de la chaine de Markov
    succ, PartMarkov = 8*[0], []
    LongPartition = []

    TabMarkov = np.zeros((8,8)) #création d'un tableau 2d 8x8
    for x in range(len(ListePartition)-1) : #analyse chaque note
        TabMarkov[ListePartition[x], ListePartition[x+1]] += 1
    #print(TabMarkov)

    for x in range(8): #chercher la premiere note de la partition
        for y in range(8): #additionne le nombre d'occurrences de chaque ligne
            succ[x] += TabMarkov[x,y]
    PartMarkov.append(succ.index(max(succ))) #cherche l'index de la valeur max de la somme des occurrences
    #print(PartMarkov)

    N, succ = PartMarkov[0], []
    for y in range(LengthPart-1): #créer une liste d'une taille aléatoire entre la plus petite partition et la plus grande
        for x in range(8) : #chercher la proba des valeurs suivantes
            if TabMarkov[N,x] == 0 :
                pass #enlève les valeurs 0 dans les proba d'apparaitre
            else :
                succ.extend(int(TabMarkov[N,x])*[x]) #ajoute x fois la note dans une liste
        N = choice(succ) #choisit valeur au hasard dans la liste
        PartMarkov.append(N) #l'ajoute à la partition

    return PartMarkov



#Partition a partir de note + pause (pour la chaine de markov + transposition + inversion)
def partition_crea(note, durer):
    # Variable
    lecture = []

    # Creation lecture
    for x in range(0, len(note)):
        if "p" in durer[x]:
            #Remplace dans pause x 'p' par rien -> efface le charactère
            durer[x] = durer[x].translate({ord('p'): None})
            lecture.append(note[x] + durer[x] + " ")
            lecture.append("p" + " ")
        else:
            lecture.append(note[x] + durer[x] + " ")


    return(lecture)