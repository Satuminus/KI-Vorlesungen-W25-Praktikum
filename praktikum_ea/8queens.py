#!/usr/bin/env python3

import csv
import random

# Erzeugt ein zufälliges 8-Queens-Brett (Liste mit 8 Zahlen 1..8)
def make_random_queen_board():
    board = []
    for i in range(8):
        board.append(random.randint(1, 8))
    return board

# Zählt, wie viele Damenpaare sich gegenseitig angreifen
def count_conflicts(board):
    conflicts = 0
    for i in range(8):
        for j in range(i+1, 8):
            # Gleiche Zeile?
            if board[i] == board[j]:
                conflicts += 1
            # Gleiche Diagonale?
            if abs(board[i] - board[j]) == abs(i - j):
                conflicts += 1
    return conflicts

# Höhere Fitness = weniger Konflikte (maximal 28 konfliktfreie Paare)
def fitness(board):
    max_pairs = 28  # 8*7/2 = 28 mögliche Paare
    conflicts = count_conflicts(board)
    return max_pairs - conflicts

# Prüft, ob perfekte Lösung gefunden wurde --> Keine Konfilkte
def is_solution(board):
    return count_conflicts(board) == 0


# Fitnessproportionale Selektion (Roulette Wheel Selektion)
def select_roulette(population):
    # Berechne alle Fitnesswerte
    fitness_values = []
    for board in population:
        fitness_values.append(fitness(board))
    
    # Gesamtfitness
    total_fitness = sum(fitness_values)
    
    # Falls alle schlecht , nehme random
    if total_fitness == 0:
        parent1 = random.choice(population)
        parent2 = random.choice(population)
        return parent1, parent2
    
    # Wähle parent1
    rand = random.random() * total_fitness
    current = 0
    parent1 = population[0]
    for i in range(len(population)):
        current += fitness_values[i]
        if current >= rand:
            parent1 = population[i]
            break
    
    # Wähle parent2
    rand = random.random() * total_fitness
    current = 0
    parent2 = population[0]
    for i in range(len(population)):
        current += fitness_values[i]
        if current >= rand:
            parent2 = population[i]
            break
    
    return parent1, parent2

# Turnierselektion (k Kandidaten, bester gewinnt)
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

# 1-Punkt Crossover
def crossover_one_point(parent1, parent2):
    cut = random.randint(1, 7)
    child = []
    for i in range(8):
        if i < cut:
            child.append(parent1[i])
        else:
            child.append(parent2[i])
    return child

# 2-Punkt Crossover
def crossover_two_point(parent1, parent2):
    cut1 = random.randint(1, 6)
    cut2 = random.randint(cut1+1, 7)
    child = []
    for i in range(8):
        if i < cut1:
            child.append(parent1[i])
        elif i < cut2:
            child.append(parent2[i])
        else:
            child.append(parent1[i])
    return child

# Shuffle
def crossover_shuffle(parent1, parent2):
    cut = random.randint(1, 7)
    child = []
    for i in range(8):
        if i < cut:
            child.append(parent1[i])
        else:
            child.append(parent2[i])
    return child

# Mutiert jedes Gen mit Wahrscheinlichkeit p_mut (setzt Wert neu auf 1 bis8)
def mutate(board, p_mut=0.125):
    new_board = []
    for i in range(8):
        if random.random() < p_mut:
            # Ändere dieses Gen zu einem neuen Wert (1-8)
            new_value = random.randint(1, 8)
            new_board.append(new_value)
        else:
            new_board.append(board[i])
    return new_board


# Führt einen GA-Lauf durch und gibt beste Lösung, Generation und Fitness zurück
def run_ga(pop_size=50, max_gen=1000, p_crossover=0.9, p_mut=0.125,
           selection="tournament", tournament_k=3, crossover="one_point"):
    # 1. Erstelle Startpopulation
    population = []
    for i in range(pop_size):
        population.append(make_random_queen_board())
    
    # 2. Finde bestes Individuum am Anfang
    best = population[0]
    best_fitness = fitness(best)
    for board in population:
        f = fitness(board)
        if f > best_fitness:
            best = board
            best_fitness = f
    
    # Falls fertig
    if is_solution(best):
        return best, 0, best_fitness
    
    # 3. Evolutionsschleife
    for generation in range(1, max_gen + 1):
        new_population = []
        
        # Erstelle neue Population
        for i in range(pop_size):
            # Selektion
            if selection == "tournament":
                parent1, parent2 = select_tournament(population, tournament_k)
            else:
                parent1, parent2 = select_roulette(population)
            
            # Crossover
            if random.random() < p_crossover:
                if crossover == "one_point":
                    child = crossover_one_point(parent1, parent2)
                elif crossover == "two_point":
                    child = crossover_two_point(parent1, parent2)
                else:  # shuffle
                    child = crossover_shuffle(parent1, parent2)
            else:
                # Kein Crossover -> Kind = Kopie von parent1
                child = parent1[:]
            
            # Mutation
            child = mutate(child, p_mut)
            
            new_population.append(child)
        
        # Ersetze alte Population
        population = new_population
        
        # Finde beste Fitness
        for board in population:
            f = fitness(board)
            if f > best_fitness:
                best = board
                best_fitness = f
        
        # falls Lösung
        if is_solution(best):
            return best, generation, best_fitness
    
    # Keine Lösung gefunden
    return best, max_gen, best_fitness


# Führt versch. Einstellungen aus schreibt Ergebnisse als CSV
def run_experiments():
    
    experiments = [
        {"name": "Kodierung 50, Turnier k=3, 1-Punkt, genweise Mutation", 
         "pop_size": 50, "selection": "tournament", 
         "tournament_k": 3, "crossover": "one_point", "p_crossover": 0.9, "p_mut": 0.125},
        
        {"name": "Kodierung 50, Fitnessproportional, 1-Punkt, genweise Mutation", 
         "pop_size": 50, "selection": "roulette", 
         "tournament_k": 3, "crossover": "one_point", "p_crossover": 0.9, "p_mut": 0.125},
        
        {"name": "Kodierung 100, Turnier k=3, 2-Punkt, genweise Mutation", 
         "pop_size": 100, "selection": "tournament", 
         "tournament_k": 3, "crossover": "two_point", "p_crossover": 0.9, "p_mut": 0.125},
        
        {"name": "Kodierung 100, Turnier k=3, Shuffle, genweise Mutation", 
         "pop_size": 100, "selection": "tournament", 
         "tournament_k": 3, "crossover": "shuffle", "p_crossover": 0.9, "p_mut": 0.125},
        
        {"name": "Kodierung 100, Turnier k=5, 1-Punkt, genweise Mutation", 
         "pop_size": 100, "selection": "tournament", 
         "tournament_k": 5, "crossover": "one_point", "p_crossover": 0.9, "p_mut": 0.125},
        
        {"name": "Kodierung 100, Turnier k=3, 1-Punkt, genweise Mutation, p_cx=0.7", 
         "pop_size": 100, "selection": "tournament", 
         "tournament_k": 3, "crossover": "one_point", "p_crossover": 0.7, "p_mut": 0.125},
        
        {"name": "Kodierung 100, Turnier k=3, 1-Punkt, genweise Mutation, p_mut=0.2", 
         "pop_size": 100, "selection": "tournament", 
         "tournament_k": 3, "crossover": "one_point", "p_crossover": 0.9, "p_mut": 0.2},
    ]
    
    runs_per_experiment = 100
    
    
    summary_data = [] # Daten sammeln
    
    # CSV-Datei öffnen
    with open("results_8queens.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["experiment", "run", "generation", "success", "best_fitness"])
        
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
                
                writer.writerow([exp["name"], run, gen, success, best_fit])
                
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
                "problem": "8-Queens",
                "einstellung": exp["name"],
                "sr": sr,
                "aes": aes,
                "avg_fitness": avg_fitness
            })
            
            print(f"  SR = {sr:.4f}")
            print(f"  AES = {aes:.2f}" if aes > 0 else "  AES = keine Lösung gefunden")
            print(f"  Durchschnittliche Fitness = {avg_fitness:.3f}")
        
        # Summary-Tabelle in CSV schreiben
        writer.writerow([])
        writer.writerow(["=== SUMMARY ==="])
        writer.writerow(["Problem", "Einstellung", "SR", "AES", "Durchschnittliche Fitness"])
        
        for data in summary_data:
            writer.writerow([
                data["problem"],
                data["einstellung"],
                f"{data['sr']:.4f}",
                f"{data['aes']:.2f}" if data['aes'] > 0 else "N/A", # Falls direkt in Evolution 0 fertig
                f"{data['avg_fitness']:.3f}"
            ])
    
    
    print(f"\n Fertig! Ergebnisse in results_8queen.csv")

if __name__ == "__main__":
    run_experiments()