# Aufgabe 1

## 8-Queens-Problem

### Kodierung (eine Lösungsmöglichkeit):

[4, 2, 7, 3, 6, 8, 5, 1] —> Index steht für Spalte des Schachbretts, Wert steht für die Zeile
Damit ist schonmal abgedeckt, das jede Zeile und jede Spalte nur einmal belegt ist. 

### Operatoren
#### Crossover (PMX) 
Warum PMX? Bei normalem Crossover (1-Punkt) bekommt man ungültige Nachkommen.

A = [4,2,7,3,6,8,5,1]
B = [3,6,4,2,8,5,1,7]

Crossover-Punkte wählen:
A: [4, 2, (7, 3, 6), 8, 5, 1]
B: [3, 6, (4, 2, 8), 5, 1, 7]

--> [-,-,7,3,6,-,-,-]     [-,-,4,2,8,-,-,-]

7 <-> 4
3 <-> 2
6 <-> 8

- Pos 1: Im A-Crossover-Teil ist 3 schon drin --> Mappingtabelle --> 2
- Pos 2: Wie oben --> 8
- Pos 3-5: A-Teil
- Pos 6: Bleibt 5, nicht im A-Teil
- Pos 7: Bleibt 1, nicht im A-Teil
- Pos 8: 7 ist im A-Teil --> Mapping-Tabelle --> 4
[2,8,7,3,6,5,1,4] 

--> Gültige Permutation
--> Keine gültige Lösung

### Mutation
Swap-Mutation -> Bei der Mutation ist die Permutation immer gültig
[4, 2, (7, 3, 6), 8, 5, 1] 
--> zufällige Positionen tauschen ( Pos 2 und Pos 7)
[4, 5, (7, 3, 6), 8, 2, 1]

--> gültig
### Fitnessfunktion
f(n) = 28 − Anzahl der diagonalen Konflikte zwischen den Damen.

—> Bei 8 Damen gibt es 28 Möglichkeiten, wie sich die Damen gegenseitig angreifen können 

$\binom{8}{2} = 28$

### Simulated Annealing
Es wird eine Kostenfunktion (Anzahl diagonaler Konflikte) benötigt und eine Regel zur Erzeugung von Nachbarzuständen (Vertauschen zweier Damenpostionen). 
Und Temperatur-Parameter/Abkühlungsplan

## Landkarten-Färbeproblem
Regionen A-F --> Index
5 Farben
### Kantenliste/Nachbarn

| Region | Nachbarn |
| ------ | -------- |
| A      | B,C      |
| B      | A,C,D    |
| C      | A,B,D    |
| D      | B,C,E    |
| E      | D        |
| F      | /        |
--> (A,B),(A,C),(B,C),(B,D),(C,D),(D,E)
### Kodierung
[1, 3, 2, 1, 4, 5]
### Operatoren
#### Crossover
Für jede Region entweder von A ode B nehmen
A = [1,3,2,1,4,5]
B = [2,1,3,2,5,4]

--> [2, 3, 3, 1, 5, 4]
--> gültige Kodierung
#### Mutation
Zufällige Region wählen und Farbe ändern.
[1,3,2,1,4,5]
--> 
[1,3,2,5,4,5]

--> gültige Kodierung
#### Fitnessfunktion
f(n)=C−(W×Konflikte+λ×Farben)

C --> Konstante damit Fitness positiv bleibt
W --> Gewicht für Konfilkte
λ --> Gewicht für die Anzahl der verwendeten Farben

Am Beispiel [1,3,2,1,4,5] :
6 Regionen, 5 Farben, kein Konflikt
C = 1000, W = 100, λ = 1
f(n) = 1000 - (100 x 0 + 1 x 5) = 995
#### Simulated Annealing
Es wird eine Kostenfunktion (Anzahl der Kanten + Gewicht für genutzte Farben) benötigt und eine Regel zur Erzeugung von Nachbarzuständen (z. B. Ändern der Farbe einer Region).  Zusätzlich braucht man einen Temperaturparameter mit Abkühlungsplan,  
damit auch schlechtere Zustände mit einer gewissen Wahrscheinlichkeit akzeptiert werden können.

# Aufgabe 2
[8queens.py](https://github.com/Satuminus/KI-Vorlesungen-W25-Praktikum/blob/main/praktikum_ea/8queens.py)
[landkarte.py](https://github.com/Satuminus/KI-Vorlesungen-W25-Praktikum/blob/main/praktikum_ea/landkarte.py)
[results 8queens](https://github.com/Satuminus/KI-Vorlesungen-W25-Praktikum/blob/main/results_8queens.csv)
[results landkarte](https://github.com/Satuminus/KI-Vorlesungen-W25-Praktikum/blob/main/results_map.csv) 
## 8-Queens-Problem

| Problem | Einstellung | SR | AES | Durchschnittliche Fitness |
|---------|-------------|-------|--------|---------------------------|
| 8-Queens | Kodierung 50, Turnier k=3, 1-Punkt, genweise Mutation | 0.9700 | 104.08 | 27.970 |
| 8-Queens | Kodierung 50, Fitnessproportional, 1-Punkt, genweise Mutation | 0.3100 | 389.74 | 27.310 |
| 8-Queens | Kodierung 100, Turnier k=3, 2-Punkt, genweise Mutation | 1.0000 | 84.69 | 28.000 |
| 8-Queens | Kodierung 100, Turnier k=3, Shuffle, genweise Mutation | 0.9800 | 56.91 | 27.980 |
| 8-Queens | Kodierung 100, Turnier k=5, 1-Punkt, genweise Mutation | 1.0000 | 93.68 | 28.000 |
| 8-Queens | Kodierung 100, Turnier k=3, 1-Punkt, genweise Mutation, p_cx=0.7 | 1.0000 | 66.27 | 28.000 |
| 8-Queens | Kodierung 100, Turnier k=3, 1-Punkt, genweise Mutation, p_mut=0.2 | 1.0000 | 114.02 | 28.000 |

### Beobachtungen
- Turnier-Selektion (schlechteste SR 0.97) ist der Fitnessproprotionalen Sekektion (SR 0.31) überlegen.
- Mehr Kodierungen --> höhere SR
- Shuffle-Crossover ist am schnellsten (AES 56.91)
- 2-Punkt-Crossover bester Kompromiss aus AES und SR
- 1-Punkt-Crossover langsam aber zuverlässiger
- Weniger Crossover --> bessere AES, SR bleibt erhalten (Weniger Crossover-Wahrscheinlichkeit)
- Erhöhung Mutation verlängert AES deutlich


# Map-Coloring-Problem

| Problem | Einstellung | SR | AES | Durchschnittliche Fitness |
|---------|-------------|-------|--------|---------------------------|
| Map-Coloring | Kodierung 50, Turnier k=3, Uniform, genweise Mutation | 1.0000 | N/A | 996.630 |
| Map-Coloring | Kodierung 50, Fitnessproportional, Uniform, genweise Mutation | 1.0000 | N/A | 996.590 |
| Map-Coloring | Kodierung 100, Turnier k=3, 1-Punkt, genweise Mutation | 1.0000 | N/A | 996.940 |
| Map-Coloring | Kodierung 100, Turnier k=3, 2-Punkt, genweise Mutation | 1.0000 | N/A | 996.950 |
| Map-Coloring | Kodierung 100, Turnier k=5, Uniform, genweise Mutation | 1.0000 | N/A | 996.910 |
| Map-Coloring | Kodierung 100, Turnier k=3, Uniform, genweise Mutation, p_cx=0.7 | 1.0000 | N/A | 996.910 |
| Map-Coloring | Kodierung 100, Turnier k=3, Uniform, genweise Mutation, p_mut=0.3 | 1.0000 | N/A | 996.900 |

Bei AES - N/A --> Startpopulation ist bereits Lösung

## Beobachtungen
- Alle Einstellungen erreichen SR 100%
- Anscheindend einfaches Problem (oder falsche Implementation)
- Fitness ändert sich nur mininal
- Fitnessproportionale Selektion funktioniert gut


# Aufgabe 3

## Here is Waldo
Es wird basierend auf bereits vorhandenen Koodinaten aller "Wheres Waldo" eine Heatmap erstellt, wo Waldo am häufigsten zu finden ist. Es gibt 68 mögliche Koodinaten, in denen Waldo seien könnte. --> Theorie: Liste anlegen, und die kürzeste Distanz finden, in der alle Punkte abgecheckt werden können.
- Problem: Sehr sehr viele Optionen
- Lösung: Genetischer Algorithmus berechnet Pfad --> effizienter Suchpfad


In diesem Code wird die Fitness berechnet:
```python
def compute_fitness(solution):
    solution_fitness = 0.0
    for index in range(1, len(solution)):
        w1 = solution[index]
        w2 = solution[index - 1]
        solution_fitness += calculate_distance(
            waldo_location_map[w1][0], waldo_location_map[w1][1],
            waldo_location_map[w2][0], waldo_location_map[w2][1]
        )
    return solution_fitness

```
Per LLM in eine Mathefunktion:
$ \mathrm{Fitness}(\text{solution})=\sum_{i=1}^{n-1}\sqrt{(x_i-x_{i-1})^2+(y_i-y_{i-1})^2}, $

Es werden Swap und Shuffle genutzt, kein Crossover (Nur Mutationen als Operationen).

## Evolution Simulator
- Kreaturen werden aus Nodes und deren Verbindungen erstellt. Die Verbindungen ziehen sich zusammen und dehnen sich aus, wie Muskeln. In der Welt gibt es Schwerkraft, Reibung. 
- Es werden 1000 zufällige Kreaturen erstellt. Jede wird 15s lang simuliert und die Fitness gemessen (f(n) = distanz nach rechts?)
- Kreaturen werden nach Fitness sortiert und die langsamere Hälfte hat dann eine höhere Wahrscheinlichkeit zu sterben, schnellere überleben wahrscheinlicher
- Überlebende erzeugen Mutationen


### Fitnessfunktion
Die Fitnessfunktion ist die Horizontale Distanz nach 15 Sekunden, ausgehend vom Startpunkt (positiv nach rechts, negativ nach links).

### Kodierung
Eine Kratur ist eine Liste aus Nodes und Muskeln. Diese enthalten jeweils verschiedene Parameter, die Mutieren können.


## American Fuzzy Lop
- Fuzzing --> Automatisiertes Testen von Software mit Zufallsdaten
- Test (Eingaben) werden mutiert, nur Mutanten, die neue Programmpfade eröffnen überleben (irgendwie keine normale Fitnessfunktion?)
- brute force testing?
- Kodierung: Ein Individuum ist eine Eingabe



## Anwendungen von Evolutionären Algorithmen
Recherchieren Sie, in welchen anderen Anwendungen Evolutionäre Algorithmen eingesetzt werden. Erklären Sie kurz, wie und wofür die EA/GA jeweils genutzt werden.

- Ingenieurdesign: Aerodynamik, mit CAD/CAE-Parametern
- Bio- und Chemieinformatik: Proteinstruktur-Heuristik (Vorhersage zur Struktur eines Proteins)
-
