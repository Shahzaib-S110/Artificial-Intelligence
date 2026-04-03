# Part A

import random

# Q2 Landscape
landscape = [5, 8, 6, 12, 9, 7, 17, 14, 10, 6, 19, 15, 11, 8]

def find_local_maxima(landscape):
    """Return all positions whose f-value exceeds both neighbors."""
    maxima = []
    n = len(landscape)
    for i in range(n):
        left = landscape[i-1] if i > 0 else float('-inf')
        right = landscape[i+1] if i < n-1 else float('-inf')
        if landscape[i] > left and landscape[i] > right:
            maxima.append(i)
    return maxima

def hill_climb(landscape, start, variant='first choice'):
    """Perform a single hill climbing run starting at 'start'."""
    path = [start]
    current = start
    n = len(landscape)

    while True:
        neighbors = []
        if current > 0:
            neighbors.append(current - 1)
        if current < n - 1:
            neighbors.append(current + 1)

        # Evaluate neighbor values
        neighbor_values = [landscape[i] for i in neighbors]
        current_value = landscape[current]

        if variant == 'first choice':
            moved = False
            for i, val in zip(neighbors, neighbor_values):
                if val > current_value:
                    current = i
                    path.append(current)
                    moved = True
                    break
            if not moved:
                break  # Local max reached

        elif variant == 'stochastic':
            better_neighbors = [i for i, val in zip(neighbors, neighbor_values) if val > current_value]
            if better_neighbors:
                current = random.choice(better_neighbors)
                path.append(current)
            else:
                break  # Local max reached
        else:
            raise ValueError("variant must be 'first choice' or 'stochastic'")

    return current, landscape[current], path

def random_restart_hc(landscape, num_restarts, variant='first choice'):
    """Random Restart Hill Climbing"""
    all_results = []
    best_state, best_value = None, float('-inf')

    for r in range(num_restarts):
        start = random.randint(0, len(landscape)-1)
        terminal, value, path = hill_climb(landscape, start, variant)
        all_results.append((start, terminal, path))
        if value > best_value:
            best_state, best_value = terminal, value

    return best_state, best_value, all_results

def main():
    num_restarts = 20
    global_max = max(landscape)
    print("Local maxima positions:", find_local_maxima(landscape))
    print("\nRandom Restart Hill Climbing (First Choice):")
    best_state, best_value, results = random_restart_hc(landscape, num_restarts, 'first choice')
    print("Restart | Start | Terminal | f-value | Global Max?")
    for i, (start, terminal, path) in enumerate(results, 1):
        print(f"{i:7} | {start:5} | {terminal:8} | {landscape[terminal]:7} | {'Yes' if landscape[terminal]==global_max else 'No'}")

    print("\nRandom Restart Hill Climbing (Stochastic):")
    best_state, best_value, results = random_restart_hc(landscape, num_restarts, 'stochastic')
    print("Restart | Start | Terminal | f-value | Global Max?")
    for i, (start, terminal, path) in enumerate(results, 1):
        print(f"{i:7} | {start:5} | {terminal:8} | {landscape[terminal]:7} | {'Yes' if landscape[terminal]==global_max else 'No'}")

if __name__ == "__main__":
    main()

# Part B

# Step 1: Compute fraction p
global_max_state = 10  # 0-indexed: state 11
reachable_from = []

for start in range(len(landscape)):
    terminal, value, path = hill_climb(landscape, start, variant='first choice')
    if terminal == global_max_state:
        reachable_from.append(start)

p = len(reachable_from) / len(landscape)
print("Starting states that reach global max:", reachable_from)
print(f"Fraction p = {p:.3f}")

import numpy as np

restart_counts = [1, 3, 5, 10, 20]
trials = 100

empirical_probs = []

for n in restart_counts:
    successes = 0
    for _ in range(trials):
        best_state, best_value, results = random_restart_hc(landscape, n, variant='first choice')
        if best_state == global_max_state:
            successes += 1
    empirical_probs.append(successes / trials)

# Print table
print("\nEmpirical probabilities of finding global max:")
print("Restarts | Empirical P")
for n, p_emp in zip(restart_counts, empirical_probs):
    print(f"{n:8} | {p_emp:.3f}")

# Theoretical probabilities
theoretical_probs = [1 - (1 - p)**n for n in restart_counts]

print("\nTheoretical probabilities of finding global max:")
print("Restarts | Theoretical P")
for n, p_theo in zip(restart_counts, theoretical_probs):
    print(f"{n:8} | {p_theo:.3f}")

# Part C

# Original landscape
landscape_plateau = landscape.copy()
landscape_plateau[6] = 17  # state 7 (0-indexed)
landscape_plateau[7] = 17  # state 8 (0-indexed)

def random_restart_hc_plateau(landscape, num_restarts, variant='first choice', plateau_states=[6,7]):
    all_results = []
    best_state, best_value = None, float('-inf')
    plateau_count = 0

    for _ in range(num_restarts):
        start = random.randint(0, len(landscape)-1)
        terminal, value, path = hill_climb(landscape, start, variant)
        all_results.append((start, terminal, path))
        if terminal in plateau_states:
            plateau_count += 1
        if value > best_value:
            best_state, best_value = terminal, value

    return best_state, best_value, all_results, plateau_count

num_restarts = 20
global_max_state = 10  # state 11, f=19

# Before plateau modification
best_state_orig, best_value_orig, results_orig, plateau_count_orig = random_restart_hc_plateau(
    landscape, num_restarts, 'first choice', plateau_states=[]
)

# After plateau modification
best_state_plateau, best_value_plateau, results_plateau, plateau_count_plateau = random_restart_hc_plateau(
    landscape_plateau, num_restarts, 'first choice', plateau_states=[6,7]
)

# Count how many restarts found the global maximum
global_max_found_orig = sum(1 for start, term, path in results_orig if term == global_max_state)
global_max_found_plateau = sum(1 for start, term, path in results_plateau if term == global_max_state)

# Print table
print("\nGlobal Maximum Discovery Rate (20 restarts):")
print("Landscape       | Global Max Found | Plateau Count")
print(f"Original        | {global_max_found_orig}/20        | {plateau_count_orig}")
print(f"With Plateau    | {global_max_found_plateau}/20        | {plateau_count_plateau}")
