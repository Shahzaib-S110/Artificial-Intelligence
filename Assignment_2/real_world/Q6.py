# Part A

import random

# Demand grid
demands = [
    12,45,23,67,34,19, 56,38,72,15,49,61, 27,83,41,55,30,77,
    64,18,52,39,71,26, 44,91,33,58,22,85,16,69,47,74,31,53
]

supply_penalty = 5
num_drivers = 10
num_zones = 36

def fitness(state, demands):
    """Compute the objective value for a given state (set of 10 zones)."""
    return sum(demands[i] for i in state) - supply_penalty * num_drivers

def random_state():
    """Generate a valid random state with 10 unique zone indices."""
    return set(random.sample(range(num_zones), num_drivers))

def get_neighbours(state):
    """Generate all neighbours by moving one driver to an empty zone."""
    neighbours = []
    current_zones = list(state)
    for i in current_zones:
        for j in range(num_zones):
            if j not in state:
                new_state = state.copy()
                new_state.remove(i)
                new_state.add(j)
                neighbours.append(new_state)
    return neighbours

for _ in range(3):
    state = random_state()
    print("State:", sorted(state))
    print("Fitness:", fitness(state, demands))
    neighbours = get_neighbours(state)
    print("Number of neighbours:", len(neighbours))
    # verify all neighbours have length 10 and unique zones
    assert all(len(n) == 10 for n in neighbours), "Neighbour has wrong size"
    assert all(len(n) == len(set(n)) for n in neighbours), "Neighbour has duplicates"


# part B

def hc_driver(state, demands, variant='first_choice'):
    """
    Perform a single Hill Climbing run.
    variant: 'first_choice' or 'stochastic'
    Returns: (final_state, final_fitness, steps)
    """
    current_state = state.copy()
    current_fitness = fitness(current_state, demands)
    steps = 0

    while True:
        neighbours = get_neighbours(current_state)
        # Compute fitness for all neighbours
        neighbour_fitness = [(n, fitness(n, demands)) for n in neighbours]
        # Filter improving neighbours
        improving = [(n, f) for n, f in neighbour_fitness if f > current_fitness]

        if not improving:
            break  # local optimum reached

        if variant == 'first_choice':
            # pick the first improving neighbour
            next_state, next_fitness = improving[0]
        elif variant == 'stochastic':
            # pick a random improving neighbour
            next_state, next_fitness = random.choice(improving)
        else:
            raise ValueError("Variant must be 'first_choice' or 'stochastic'")

        current_state = next_state
        current_fitness = next_fitness
        steps += 1

    return current_state, current_fitness, steps


def rrhc_driver(num_restarts, demands, variant='first_choice'):
    """
    Perform Random Restart Hill Climbing
    Returns:
        best_state: best state across all restarts
        best_fitness: best fitness
        restart_best_fitness: list of best fitness per restart
    """
    restart_best_fitness = []
    best_state = None
    best_fitness = float('-inf')

    for _ in range(num_restarts):
        init_state = random_state()
        final_state, final_fitness, _ = hc_driver(init_state, demands, variant)
        restart_best_fitness.append(final_fitness)

        if final_fitness > best_fitness:
            best_fitness = final_fitness
            best_state = final_state

    return best_state, best_fitness, restart_best_fitness

# justification = """
# I’ll choose First-Choice HC for RRHC because:

# Each state has 260 neighbors (10 drivers × 26 empty zones), so there are many improving moves possible at each step.
# First-Choice quickly finds an improving neighbor without evaluating all 260, saving computation.
# Stochastic HC is better for extremely flat landscapes, but here the demand differences make many improving moves available, so First-Choice is efficient.


num_restarts = 30
best_state, best_fitness, restart_best_fitness = rrhc_driver(num_restarts, demands, variant='first_choice')

print("Best fitness overall:", best_fitness)
print("Best state zones (indices):", sorted(best_state))
# Convert indices to (row, col)
best_positions = [(i // 6, i % 6) for i in sorted(best_state)]
print("Best state zones (row, col):", best_positions)
print("Best fitness per restart:", restart_best_fitness)
    print("-" * 40)


# Part C

def ga_fitness(chromosome, demands):
    """Compute fitness of a GA chromosome (list of 10 unique zones)."""
    return sum(demands[i] for i in chromosome) - supply_penalty * num_drivers

def ordered_crossover(p1, p2):
    """Perform Order Crossover (OX) between two parent chromosomes."""
    size = len(p1)
    # Random slice
    start, end = sorted(random.sample(range(size), 2))
    child = [None] * size

    # Copy slice from p1
    child[start:end+1] = p1[start:end+1]

    # Fill remaining positions from p2 in order, skipping duplicates
    p2_index = 0
    for i in range(size):
        if child[i] is None:
            while p2[p2_index] in child:
                p2_index += 1
            child[i] = p2[p2_index]
            p2_index += 1

    return child

def ga_mutate(chromosome, p_m):
    if random.random() < p_m:
        # pick a zone in the chromosome to replace
        to_replace_idx = random.randint(0, len(chromosome)-1)
        current_set = set(chromosome)
        # choose a zone not in chromosome
        new_zone = random.choice(list(set(range(num_zones)) - current_set))
        chromosome[to_replace_idx] = new_zone
        chromosome.sort()  # keep chromosome sorted
    return chromosome

def tournament_selection(population, fitnesses, k=3):
    """Select one parent using tournament selection of size k."""
    selected_idx = random.sample(range(len(population)), k)
    selected = [(fitnesses[i], population[i]) for i in selected_idx]
    selected.sort(reverse=True)  # higher fitness first
    return selected[0][1]  # return chromosome with highest fitness

def run_ga(pop_size=30, generations=100, p_m=0.1):
    # Initialize population
    population = [sorted(random.sample(range(num_zones), num_drivers)) for _ in range(pop_size)]
    
    best_chromosome = None
    best_fitness = float('-inf')

    for gen in range(generations):
        fitnesses = [ga_fitness(c, demands) for c in population]
        
        # Update best solution
        max_idx = fitnesses.index(max(fitnesses))
        if fitnesses[max_idx] > best_fitness:
            best_fitness = fitnesses[max_idx]
            best_chromosome = population[max_idx].copy()
        
        # Create new population
        new_population = []
        while len(new_population) < pop_size:
            # Selection
            parent1 = tournament_selection(population, fitnesses)
            parent2 = tournament_selection(population, fitnesses)
            # Crossover
            child = ordered_crossover(parent1, parent2)
            # Mutation
            child = ga_mutate(child, p_m)
            new_population.append(child)
        
        population = new_population

    # Convert best chromosome to (row, col)
    best_positions = [(i // 6, i % 6) for i in best_chromosome]
    
    print("Best fitness:", best_fitness)
    print("Best chromosome (zone indices):", best_chromosome)
    print("Driver positions (row, col):", best_positions)
    
    return best_chromosome, best_fitness, best_positions

best_chromosome, best_fitness, best_positions = run_ga(pop_size=30, generations=100, p_m=0.1)


# part D


def ga_fitness(chromosome, demands):
    """Compute fitness of a GA chromosome (list of 10 unique zones)."""
    return sum(demands[i] for i in chromosome) - supply_penalty * num_drivers

def ordered_crossover(p1, p2):
    """Perform Order Crossover (OX) between two parent chromosomes."""
    size = len(p1)
    # Random slice
    start, end = sorted(random.sample(range(size), 2))
    child = [None] * size

    # Copy slice from p1
    child[start:end+1] = p1[start:end+1]

    # Fill remaining positions from p2 in order, skipping duplicates
    p2_index = 0
    for i in range(size):
        if child[i] is None:
            while p2[p2_index] in child:
                p2_index += 1
            child[i] = p2[p2_index]
            p2_index += 1

    return child

def ga_mutate(chromosome, p_m):
    if random.random() < p_m:
        # pick a zone in the chromosome to replace
        to_replace_idx = random.randint(0, len(chromosome)-1)
        current_set = set(chromosome)
        # choose a zone not in chromosome
        new_zone = random.choice(list(set(range(num_zones)) - current_set))
        chromosome[to_replace_idx] = new_zone
        chromosome.sort()  # keep chromosome sorted
    return chromosome

def tournament_selection(population, fitnesses, k=3):
    """Select one parent using tournament selection of size k."""
    selected_idx = random.sample(range(len(population)), k)
    selected = [(fitnesses[i], population[i]) for i in selected_idx]
    selected.sort(reverse=True)  # higher fitness first
    return selected[0][1]  # return chromosome with highest fitness

def run_ga(pop_size=30, generations=100, p_m=0.1):
    # Initialize population
    population = [sorted(random.sample(range(num_zones), num_drivers)) for _ in range(pop_size)]
    
    best_chromosome = None
    best_fitness = float('-inf')

    for gen in range(generations):
        fitnesses = [ga_fitness(c, demands) for c in population]
        
        # Update best solution
        max_idx = fitnesses.index(max(fitnesses))
        if fitnesses[max_idx] > best_fitness:
            best_fitness = fitnesses[max_idx]
            best_chromosome = population[max_idx].copy()
        
        # Create new population
        new_population = []
        while len(new_population) < pop_size:
            # Selection
            parent1 = tournament_selection(population, fitnesses)
            parent2 = tournament_selection(population, fitnesses)
            # Crossover
            child = ordered_crossover(parent1, parent2)
            # Mutation
            child = ga_mutate(child, p_m)
            new_population.append(child)
        
        population = new_population

    # Convert best chromosome to (row, col)
    best_positions = [(i // 6, i % 6) for i in best_chromosome]
    
    print("Best fitness:", best_fitness)
    print("Best chromosome (zone indices):", best_chromosome)
    print("Driver positions (row, col):", best_positions)
    
    return best_chromosome, best_fitness, best_positions

best_chromosome, best_fitness, best_positions = run_ga(pop_size=30, generations=100, p_m=0.1)
