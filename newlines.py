import csv
from math import *

# Utilisation de trips.csv
fic2 = open('trips.csv')
f2 = csv.reader(fic2)
liste_trip_id = []

for ligne in f2:
    if ligne[3] == 'trip_headsign':
        continue
    if ligne[3] not in liste_trip_id:
        liste_trip_id.append(ligne[3])

fic2.close()

# Conversion degré / radian
def deg2rad(dd):
    return float(dd)/180*pi

# Calcul de la distance entre 2 arrêts
def distance(arret,arretsuiv):

    fichier = open('stops.csv')
    f = csv.reader(fichier)
    next(f)
    for x in f:
        if int(x[0]) == arret:
            print(x)
            latA = deg2rad(x[4])
            longA = deg2rad(x[5])
            nomA = x[2]
        if int(x[0]) == arretsuiv:
            latB = deg2rad(x[4])
            longB = deg2rad(x[5])
            nomB = x[2]

    RT = 6378137
    S = acos(sin(latA) * sin(latB) + cos(latA) * cos(latB) * cos(abs(longB - longA)))
    # distance entre les 2 points, comptée sur un arc de grand cercle
    fichier.close()
    return (int(S * RT),nomA,nomB)

fic = open('bus_metz_lignes2.csv', 'w', newline='')

writer = csv.writer(fic)
writer.writerow(('line', 'station_name1', 'station_name2', 'distance'))
writer = csv.writer(fic, lineterminator='\n',
                    quoting=csv.QUOTE_NONE, quotechar=None)

# Association de la distance au trajet correspondant et création des nouveaux csv
for elt in liste_trip_id:
    fic = open('Lignes2/' + str(elt) + '.csv')
    f = csv.reader(fic)
    next(f) #Ignorer l'en-tête
    liste = list(f)
    print(liste)
    for i in range(0,len(liste)-1):
        stop_id = int(liste[i][0])
        stop_id_suivant = int(liste[i+1][0])
        d, nomA, nomB = distance(stop_id,stop_id_suivant)
        writer.writerow((str(elt) , nomA , nomB, d))
fic.close()

print(liste_trip_id)
