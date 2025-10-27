#!/usr/bin/env python3

import csv
import random

# Regionen: A=0, B=1, C=2, D=3, E=4, F=5
# Nachbarn als Liste von Paaren (Kanten)
EDGES = [
    (0, 1),  # A-B
    (0, 2),  # A-C
    (1, 2),  # B-C
    (1, 3),  # B-D
    (2, 3),  # C-D
    (3, 4),  # D-E
]

NUM_REGIONS = 6
NUM_COLORS = 5

# zufällige Farben
def make_random_coloring():
    coloring = []
    for i in range(NUM_REGIONS):
        coloring.append(random.randint(1, NUM_COLORS))
    return coloring

# Zählt Nachbar-Paare, die die gleiche Farbe haben
def count_conflicts(coloring):
    conflicts = 0
    for edge in EDGES:
        region1 = edge[0]
        region2 = edge[1]
        if coloring[region1] == coloring[region2]:
            conflicts += 1
    return conflicts

# Zählt, wie viele Farben verwendet werden
def count_used_colors(coloring):
    used = []
    for color in coloring:
        if color not in used:
            used.append(color)
    return len(used)

# Fitnessfunktion
# Formel: C - (W * Konflikte + lam * Anzahl_Farben) -> nie negativ --> lam für lamda :/
def fitness(coloring, C=1000, W=100, lam=1):
    conflicts = count_conflicts(coloring)
    num_colors = count_used_colors(coloring)
    f = C - (W * conflicts + lam * num_colors)
    return max(0, f)

# konfliktfrei?
def is_solution(coloring):
    return count_conflicts(coloring) == 0

# Fitnessproportionale Selektion (Roulette Wheel Selection)
def select_roulette(population):
    # Alle Fitnesswerte berechnen
    fitness_values = []
    for coloring in population:
        fitness_values.append(fitness(coloring))
    
    total_fitness = sum(fitness_values)
    
    # Falls Gesamtfitness 0 ist, wähle zufällig
    if total_fitness == 0:
        parent1 = random.choice(population)
        parent2 = random.choice(population)
        return parent1, parent2
    
    # parent1
    rand = random.random() * total_fitness
    current = 0
    parent1 = population[0]
    for i in range(len(population)):
        current += fitness_values[i]
        if current >= rand:
            parent1 = population[i]
            break
    
    # parent2
    rand = random.random() * total_fitness
    current = 0
    parent2 = population[0]
    for i in range(len(population)):
        current += fitness_values[i]
        if current >= rand:
            parent2 = population[i]
            break
    
    return parent1, parent2

# Turnierselektion: k zufällige Kandidaten, bestes Individuum gewinnt
def select_tournament(population, k=3):
    # Turnier 1
    candidates = []
    for i in range(k):
        candidates.append(random.choice(population))
    best1 = candidates[0]
    for c in candidates:
        if fitness(c) > fitness(best1):
            best1 = c
    
    # Turnier 2
    candidates = []
    for i in range(k):
        candidates.append(random.choice(population))
    best2 = candidates[0]
    for c in candidates:
        if fitness(c) > fitness(best2):
            best2 = c
    
    return best1, best2

# Crossover: für jede Region zufällig Parent1 oder Parent2
def crossover_uniform(parent1, parent2): #Heißt anscheinend uniform-crossover
    child = []
    for i in range(NUM_REGIONS):
        if random.random() < 0.5:
            child.append(parent1[i])
        else:
            child.append(parent2[i])
    return child

# 1-Punkt Crossover
def crossover_one_point(parent1, parent2):
    cut = random.randint(1, NUM_REGIONS - 1)
    child = []
    for i in range(NUM_REGIONS):
        if i < cut:
            child.append(parent1[i])
        else:
            child.append(parent2[i])
    return child

# 2-Punkt Crossover
def crossover_two_point(parent1, parent2):
    cut1 = random.randint(1, NUM_REGIONS - 2)
    cut2 = random.randint(cut1 + 1, NUM_REGIONS - 1)
    child = []
    for i in range(NUM_REGIONS):
        if i < cut1:
            child.append(parent1[i])
        elif i < cut2:
            child.append(parent2[i])
        else:
            child.append(parent1[i])
    return child

# Mutiert jede Region mit Wahrscheinlichkeit p_mut (setzt Farbe neu 1..5)
def mutate(coloring, p_mut=0.167):
    new_coloring = []
    for i in range(NUM_REGIONS):
        if random.random() < p_mut:
            new_color = random.randint(1, NUM_COLORS)
            new_coloring.append(new_color)
        else:
            new_coloring.append(coloring[i])
    return new_coloring


# Führt einen GA-Lauf aus; gibt beste Lösung, Generation und Fitness zurück
def run_ga(pop_size=50, max_gen=1000, p_crossover=0.9, p_mut=0.167,
           selection="tournament", tournament_k=3, crossover="uniform"):
    # 1) Startpopulation
    population = []
    for i in range(pop_size):
        population.append(make_random_coloring())
    
    # 2) Bestes Individuum zu Beginn bestimmen
    best = population[0]
    best_fitness = fitness(best)
    for coloring in population:
        f = fitness(coloring)
        if f > best_fitness:
            best = coloring
            best_fitness = f
    
    # Beende, falls schon Lösung
    if is_solution(best):
        return best, 0, best_fitness
    
    # 3) Evolution 
    for generation in range(1, max_gen + 1):
        new_population = []
        
        # Neue Population erzeugen
        for i in range(pop_size):
            # Selektion
            if selection == "tournament":
                parent1, parent2 = select_tournament(population, tournament_k)
            else:
                parent1, parent2 = select_roulette(population)
            
            # Crossover
            if random.random() < p_crossover:
                if crossover == "uniform":
                    child = crossover_uniform(parent1, parent2)
                elif crossover == "one_point":
                    child = crossover_one_point(parent1, parent2)
                elif crossover == "two_point":
                    child = crossover_two_point(parent1, parent2)
                else:
                    child = crossover_uniform(parent1, parent2)
            else:
                # Kein Crossover -> Kind = Kopie von parent1
                child = parent1[:]
            
            # Mutation
            child = mutate(child, p_mut)
            new_population.append(child)
        
        # Alte Population ersetzen
        population = new_population
        
        # Beste aktualisieren
        for coloring in population:
            f = fitness(coloring)
            if f > best_fitness:
                best = coloring
                best_fitness = f
        
        # Lösung gefunden?
        if is_solution(best):
            return best, generation, best_fitness
    
    # falls keine perfekte Lösung gefunden
    return best, max_gen, best_fitness

def run_experiments():
    # Einstellungen für die Experimente
    experiments = [
        {"name": "Kodierung 50, Turnier k=3, Uniform, genweise Mutation", 
         "pop_size": 50, "selection": "tournament", 
         "tournament_k": 3, "crossover": "uniform", "p_crossover": 0.9, "p_mut": 0.167},
        
        {"name": "Kodierung 50, Fitnessproportional, Uniform, genweise Mutation", 
         "pop_size": 50, "selection": "roulette", 
         "tournament_k": 3, "crossover": "uniform", "p_crossover": 0.9, "p_mut": 0.167},
        
        {"name": "Kodierung 100, Turnier k=3, 1-Punkt, genweise Mutation", 
         "pop_size": 100, "selection": "tournament", 
         "tournament_k": 3, "crossover": "one_point", "p_crossover": 0.9, "p_mut": 0.167},
        
        {"name": "Kodierung 100, Turnier k=3, 2-Punkt, genweise Mutation", 
         "pop_size": 100, "selection": "tournament", 
         "tournament_k": 3, "crossover": "two_point", "p_crossover": 0.9, "p_mut": 0.167},
        
        {"name": "Kodierung 100, Turnier k=5, Uniform, genweise Mutation", 
         "pop_size": 100, "selection": "tournament", 
         "tournament_k": 5, "crossover": "uniform", "p_crossover": 0.9, "p_mut": 0.167},
        
        {"name": "Kodierung 100, Turnier k=3, Uniform, genweise Mutation, p_cx=0.7", 
         "pop_size": 100, "selection": "tournament", 
         "tournament_k": 3, "crossover": "uniform", "p_crossover": 0.7, "p_mut": 0.167},
        
        {"name": "Kodierung 100, Turnier k=3, Uniform, genweise Mutation, p_mut=0.3", 
         "pop_size": 100, "selection": "tournament", 
         "tournament_k": 3, "crossover": "uniform", "p_crossover": 0.9, "p_mut": 0.3},
    ]
    
    runs_per_experiment = 100
    
    # Sammle Summary-Daten
    summary_data = []
    
    # CSV-Datei öffnen
    with open("results_map.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["experiment", "run", "generation", "success", "best_fitness", 
                        "conflicts", "num_colors"])
        
        # Für jedes Experiment
        for exp in experiments:
            print(f"\n Starte Experiment: {exp['name']}")
            
            success_count = 0
            success_generations = []
            all_fitness = []
            
            # 100 Läufe
            for run in range(1, runs_per_experiment + 1):
                best, gen, best_fit = run_ga(
                    pop_size=exp["pop_size"],
                    max_gen=1000,
                    p_crossover=exp["p_crossover"],
                    p_mut=exp["p_mut"],
                    selection=exp["selection"],
                    tournament_k=exp["tournament_k"],
                    crossover=exp["crossover"]
                )
                
                success = 1 if is_solution(best) else 0
                conflicts = count_conflicts(best)
                num_colors = count_used_colors(best)
                
                writer.writerow([exp["name"], run, gen, success, best_fit, 
                               conflicts, num_colors])
                
                all_fitness.append(best_fit)
                if success:
                    success_count += 1
                    success_generations.append(gen)
                
                if run % 10 == 0:
                    print(f"  Run {run}/{runs_per_experiment} fertig")
            
            # Statistiken berechnen
            sr = success_count / runs_per_experiment
            if success_count > 0:
                aes = sum(success_generations) / len(success_generations)
            else:
                aes = 0.0
            avg_fitness = sum(all_fitness) / len(all_fitness)
            
            # Für Summary speichern
            summary_data.append({
                "problem": "Map-Coloring",
                "einstellung": exp["name"],
                "sr": sr,
                "aes": aes,
                "avg_fitness": avg_fitness
            })
            
            print(f"  SR = {sr:.4f}")
            print(f"  AES = {aes:.2f}" if aes > 0 else "  AES = keine Lösung gefunden")
            print(f"  Durchschnittliche Fitness = {avg_fitness:.3f}")
        
        # Summary-Tabelle in CSV schreiben (mit Überschrift)
        writer.writerow([])
        writer.writerow(["=== SUMMARY ==="])
        writer.writerow(["Problem", "Einstellung", "SR", "AES", "Durchschnittliche Fitness"])
        
        for data in summary_data:
            writer.writerow([
                data["problem"],
                data["einstellung"],
                f"{data['sr']:.4f}",
                f"{data['aes']:.2f}" if data['aes'] > 0 else "N/A",
                f"{data['avg_fitness']:.3f}"
            ])
    
    # Konsole: Zusammenfassung drucken
    print("ZUSAMMENFASSUNG - MAP-COLORING")
    print(f"{'Problem':<15} {'Einstellung':<60} {'SR':<8} {'AES':<8} {'Avg Fitness':<15}")
    
    for data in summary_data:
        aes_str = f"{data['aes']:.2f}" if data['aes'] > 0 else "N/A"
        print(f"{data['problem']:<15} {data['einstellung']:<60} {data['sr']:<8.4f} {aes_str:<8} {data['avg_fitness']:<15.3f}")
    
    print(f" Fertig! Ergebnisse in results_map.csv")


if __name__ == "__main__":
    run_experiments()