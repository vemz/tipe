import csv
import math
from math import inf
import numpy as np
import random

# Chargement du fichier bus_metz_lignes.csv
with open('bus_metz_lignes2.csv', 'r') as file:
    csv_reader = csv.reader(file)
    lignes = list(csv_reader)[1:]  # Ignorer les en-têtes

# Chargement du fichier bus_metz.csv
with open('bus_metz.csv', 'r') as file:
    csv_reader = csv.reader(file)
    bus = list(csv_reader)[1:]  # Ignorer les en-têtes

# Création d'une liste contenant toutes les stations
stations = []
for ligne in lignes:
    station1 = ligne[1]
    station2 = ligne[2]
    if station1 not in stations:
        stations.append(station1)
    if station2 not in stations:
        stations.append(station2)

# Création d'un dictionnaire pour stocker les distances entre les stations
distances = {}

# Parcours des lignes et mise à jour du dictionnaire des distances
for ligne in lignes:
    station1 = ligne[1]
    station2 = ligne[2]
    distance = int(ligne[3])

    if station1 not in distances:
        distances[station1] = {}
    if station2 not in distances:
        distances[station2] = {}

    distances[station1][station2] = distance
    distances[station2][station1] = distance

# Création de la matrice d'adjacence initialisée
num_stations = len(stations)
A = [[inf] * num_stations for _ in range(num_stations)]
for i in range(len(A)):
    A[i][i]=0

# Remplissage de la matrice d'adjacence à partir du dictionnaire des distances
for i, station1 in enumerate(stations):
    for j, station2 in enumerate(stations):
        if station2 in distances[station1]:
            A[i][j] = distances[station1][station2]

# Fonction pour compter le nombre de coefficients non nuls dans une liste
def non_nul(L):
    return sum(elem is not inf for elem in L)

# Recherche du nombre maximal de coefficients non nuls
max_count = 0
max_indices = []

for i, row in enumerate(A):
    count = non_nul(row)
    if count > max_count:
        max_count = count
        max_indices = [i]
    elif count == max_count:
        max_indices.append(i)

# Récupération des noms des stations correspondantes
station_names = [stations[i] for i in max_indices]

# Affichage des résultats
if max_count > 0:
    print("Stations les plus fréquentées:")
    for name in station_names:
        print(name)
else:
    print("La matrice est vide.")

# Sauvegarde de la matrice d'adjacence dans un fichier CSV
with open('matrice_adjacence.csv', 'w', newline='') as file:
    csv_writer = csv.writer(file)
    for row in A:
        csv_writer.writerow(row)

# Créer des dictionnaires pour mémoriser les indices et les lignes de chaque arrêt
stop_indices = {}
stop_lines = {}

with open('bus_metz.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)  # ignore header
    for i, row in enumerate(reader):
        name = row[0]
        stop_indices[name] = i

with open('bus_metz_lignes2.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)  # ignore header
    for row in reader:
        line, stop1, stop2, _ = row
        if stop1 not in stop_lines:
            stop_lines[stop1] = set()
        if stop2 not in stop_lines:
            stop_lines[stop2] = set()
        stop_lines[stop1].add(line)
        stop_lines[stop2].add(line)

# Créer une matrice d'adjacence
num_stops = len(stop_indices)
A = [[math.inf]*num_stops for _ in range(num_stops)]
for i in range(num_stops):
    A[i][i] = 0

with open('bus_metz_lignes2.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)  # ignore header
    for row in reader:
        _, stop1, stop2, distance = row
        i = stop_indices[stop1]
        j = stop_indices[stop2]
        A[i][j] = int(distance)

# Algorithme de Floyd-Warshall adapté conservant le trajet
def floyd_warshall(matrix):
    n = len(matrix)
    dist = matrix.copy()
    pred = [[None]*n for _ in range(n)]

    for i in range(n):
        for j in range(n):
            if matrix[i][j] != math.inf:
                pred[i][j] = i

    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    pred[i][j] = pred[k][j]

    return dist, pred

# Calcul de la quasi-inverse de la matrice
a_etoile, predecessors = floyd_warshall(A)

# Écrire la matrice dans un fichier CSV
with open('A_etoile.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(a_etoile)

# Reconstituer le chemin effectivement suivi
def reconstituer_chemin(predecessors, start_name, end_name):
    # Convertir les noms d'arrêt en indices
    start = stop_indices[start_name]
    end = stop_indices[end_name]

    # Initialiser le chemin avec l'arrêt de fin
    path = [end]

    # Remonter le chemin depuis la fin jusqu'au début
    while path[-1] != start:
        path.append(predecessors[start][path[-1]])

    # Convertir les indices du chemin en noms d'arrêt
    path = [list(stop_indices.keys())[i] for i in path[::-1]]

    return path

# Demander à l'utilisateur son arrêt de départ et d'arrivée
start_name = input("Entrez le nom de votre arrêt de départ : ")
end_name = input("Entrez le nom de votre arrêt d'arrivée : ")

# Appeler la fonction pour récupérer le chemin le plus court
path = reconstituer_chemin(predecessors, start_name, end_name)

# Afficher la distance du plus court chemin
distance = a_etoile[stop_indices[start_name]][stop_indices[end_name]]
print('La distance du chemin le plus court est : {}'.format(distance))

def assign_weight(line):
    if line.startswith('M'):
        return 1
    elif line.startswith('L'):
        return 2
    elif line.startswith('C'):
        return 3
    elif line.startswith('P'):
        return 4
    elif line.startswith('N'):
        return 5
    else:
        return 6

def get_lines_taken(path):
    # Initialiser une liste pour stocker les lignes prises
    lines_taken = []

    # Parcourir chaque arrêt du chemin
    for i in range(len(path) - 1):
        # Lire le fichier CSV ligne par ligne
        with open('bus_metz_lignes2.csv', 'r') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header

            # Initialiser le poids le plus petit à infini
            smallest_weight = inf
            ligne_a_prendre = None

            for line, station_name1, station_name2, _ in reader:
                # Si une ligne a une liaison directe entre les deux arrêts
                if (station_name1 == path[i] and station_name2 == path[i+1]) or \
                   (station_name1 == path[i+1] and station_name2 == path[i]):
                    # Calculer le poids de la ligne
                    weight = assign_weight(line)

                    # Si le poids est plus petit que le poids actuel le plus petit
                    if weight < smallest_weight:
                        smallest_weight = weight
                        ligne_a_prendre = line

            # Ajouter la ligne avec le poids le plus petit à la liste des lignes prises
            lines_taken.append(ligne_a_prendre)

    return lines_taken

# Appeler la fonction pour récupérer les lignes empruntées
lines_taken = get_lines_taken(path)

# Définir le temps de trajet comme le temps direct + 2 minutes par correspondance
def temps_theorique_minute(start_name,end_name,vitesse):
    t = (((a_etoile[stop_indices[start_name]][stop_indices[end_name]])*(10**(-3))/vitesse)*60)+2*((len(set(get_lines_taken(reconstituer_chemin(predecessors,start_name,end_name)))))-1)
    return t

lines_stops = {}
with open('bus_metz_lignes2.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)  # Skip header

    for line, station_name1, station_name2, _ in reader:
        if line not in lines_stops:
            lines_stops[line] = [station_name1, station_name2]
        else:
            if lines_stops[line][-1] == station_name1:
                lines_stops[line].append(station_name2)
            else:
                lines_stops[line].append(station_name1)

def trajet_direct(start_name, end_name):
    # Vérifier si un trajet direct est possible
    direct_line = stop_lines[start_name].intersection(stop_lines[end_name])

    if direct_line:
        direct_line = direct_line.pop()
        line_stops = lines_stops[direct_line]

        # Trouver les indices des arrêts de départ et d'arrivée
        start_index = line_stops.index(start_name)
        end_index = line_stops.index(end_name)

        # Obtenir l'itinéraire direct
        if start_index < end_index:
            trajet = line_stops[start_index:end_index+1]
        else:
            trajet = line_stops[start_index:end_index-1:-1]

        return True, direct_line, trajet
    else:
        return False, None, None

# Appeler la fonction pour vérifier si un trajet direct est possible
trajet_direct_possible, direct_line, trajet = trajet_direct(start_name, end_name)

if trajet_direct_possible:
    # Si un trajet direct est possible, l'utiliser
    print(f'Un trajet direct est possible avec la ligne : {direct_line}')
    print('Le trajet est le suivant :')
    print(' -> '.join(trajet))
else:
    # Sinon, exécuter l'algorithme de Dijkstra
    print('Un trajet direct n\'est pas possible. Calcul du trajet le plus court...')
    path = reconstituer_chemin(predecessors, start_name, end_name)
    print('Le trajet est le suivant :')
    print(' -> '.join(path))
    for i, line in enumerate(lines_taken):
        print('Entre {} et {} : Ligne {}'.format(path[i], path[i+1], line))

print('Le temps estimé du trajet est de :', temps_theorique_minute(start_name,end_name,18), 'minute(s)')

# Simulation de trajets aléatoire
def selection_arrets(file_name, num_stops):
    with open(file_name, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        all_stops = [row[0] for row in reader]  # Obtenir tous les arrêts

    arrets_aleatoires = random.sample(all_stops, num_stops)  # En sélectionner une partie aléatoirement
    return arrets_aleatoires

def temps_de_trajet(stops):
    travel_times = []
    for i in range(0, len(stops)-1, 2):  # Faire des paires d'arrêts pour créer des trajets
        start_name = stops[i]
        end_name = stops[i+1]
        time = temps_theorique_minute(start_name,end_name,18)
        travel_times.append((start_name, end_name, time))
    return travel_times

def write_to_csv(file_name, data):
    with open(file_name, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Depart", "Arrivee", "Temps"])
        writer.writerows(data)

arrets_aleatoires = selection_arrets('bus_metz.csv', 60)
travel_times = temps_de_trajet(arrets_aleatoires)
write_to_csv('travel_times.csv', travel_times)
