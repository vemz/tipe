import csv
from math import *

url = [
    ['A', 'Lignes\mettis a.csv'],
    ['B', 'Lignes\mettis b.csv'],
    ['1', 'Lignes\l1.csv'],
    ['2', 'Lignes\l2.csv'],
    ['3', 'Lignes\l3.csv'],
    ['4', 'Lignes\l4 normal.csv'],
    ['4a', 'Lignes\l4a.csv'],
    ['4b', 'Lignes\l4b.csv'],
    ['5', 'Lignes\l5 normal.csv'],
    ['5e', 'Lignes\l5e.csv'],
    ['5f', 'Lignes\l5f.csv']
]

arrets = []

# Séparation selon la ligne empruntée
def ajoutligne(lignebus):
    f = open(lignebus[1])
    lignecompt = 0
    for ligne in f:
        tempo = []
        if (lignecompt >= 1):
            x = ligne.split(",")
            tempo.append(lignebus[0])
            tempo.append(x[2])
            arrets.append(tempo)
        lignecompt += 1
    f.close()

for k in range(len(url)):
    ajoutligne(url[k])

fic = open('bus_metz_lignes.csv', 'w', newline='')
writer = csv.writer(fic)
writer.writerow(('line', 'station_name1', 'station_name2', 'distance'))
writer = csv.writer(fic, lineterminator='\n', quoting=csv.QUOTE_NONE, quotechar=None)

# Détermination de l'arrêt suivant
def arretsuivant(arrets, i):
    line, arret = arrets[i]
    if (i+1)< len(arrets):
        linesuiv, arretsuiv = arrets[i + 1]
        if line == linesuiv:
            return True, arretsuiv
        else:
            return False, arretsuiv

# Conversion degré / radian
def deg2rad(dd):
    return float(dd)/180*pi

# Calcul de la distance entre 2 arrêts
def distance(arret,arretsuiv):
    fichier = open('bus_metz.csv')
    lignecompteur = 0
    for ligne in fichier:
        x = ligne.split(",")
        if lignecompteur >= 1:
            if x[0] == arret:
                latA = deg2rad(x[1])
                longA = deg2rad(x[2])
            if x[0] == arretsuiv:
                latB = deg2rad(x[1])
                longB = deg2rad(x[2])
        lignecompteur += 1
    RT = 6378137
    S = acos(sin(latA) * sin(latB) + cos(latA) * cos(latB) * cos(abs(longB - longA)))
    # distance entre les 2 points, comptée sur un arc de grand cercle
    fichier.close()
    return int(S * RT)

# Créer la première liste des arêtes
for i in range(len(arrets)):
    line, arret = arrets[i]
    statut, arretsuiv = arretsuivant(arrets, i)
    newarret = arret.replace('"','')
    newarretsuiv = arretsuiv.replace('"', '')
    if statut == True:
        dist = distance(arret, arretsuiv)
        writer.writerow((line , newarret , newarretsuiv,dist))

fic.close()
