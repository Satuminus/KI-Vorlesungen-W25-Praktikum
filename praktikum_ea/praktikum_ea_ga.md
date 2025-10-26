# Aufgabe 1

Geben Sie für beide Probleme je eine geeignete Kodierung der Individuen, passende Operatoren (Crossover, Mutation) und eine geeignete Fitnessfunktion an, damit die Probleme mit einem GA gelöst werden können. Begründen Sie Ihre Wahl!

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


# Aufgabe 3
