# Part A

def decode(chromosome):
    """
    Converts a 4-bit binary chromosome (list of 0s and 1s) to an integer.
    """
    x = 0
    for i, bit in enumerate(reversed(chromosome)):
        x += bit * (2 ** i)
    return x

# Test decode
chromosomes = [[0,1,1,0], [1,0,0,1], [1,1,0,0], [0,0,1,1]]
for chrom in chromosomes:
    print(f"Chromosome: {chrom} -> Decoded x: {decode(chrom)}")

def fitness(chromosome):
    x = decode(chromosome)
    return -x**2 + 14*x + 5

# Test fitness
for chrom in chromosomes:
    print(f"Chromosome: {chrom} -> Fitness: {fitness(chrom)}")

import random

def roulette_select(population):
    """
    Select one individual from the population using fitness-proportionate selection.
    Population is a list of chromosomes.
    """
    fitness_values = [fitness(chrom) for chrom in population]
    total_fitness = sum(fitness_values)
    spin = random.random() * total_fitness
    cumulative = 0
    for chrom, fit in zip(population, fitness_values):
        cumulative += fit
        if cumulative >= spin:
            return chrom

# Test roulette selection
population = chromosomes
selected = [roulette_select(population) for _ in range(5)]
print("Selected individuals via roulette:", selected)

def single_point_crossover(parent1, parent2, point):
    """
    Performs single-point crossover at the specified point.
    Returns two offspring.
    """
    offspring1 = parent1[:point] + parent2[point:]
    offspring2 = parent2[:point] + parent1[point:]
    return offspring1, offspring2

# Test crossover
p1 = [0,1,1,0]
p2 = [1,0,0,1]
off1, off2 = single_point_crossover(p1, p2, 2)
print(f"Parents: {p1}, {p2} -> Offspring: {off1}, {off2}")


def mutate(chromosome, pm):
    """
    Mutates a chromosome by flipping each bit independently with probability pm.
    """
    mutated = []
    for bit in chromosome:
        if random.random() < pm:
            mutated.append(1 - bit)  # Flip bit
        else:
            mutated.append(bit)
    return mutated

# Test mutation with pm = 0.5
for chrom in chromosomes:
    print(f"Original: {chrom} -> Mutated: {mutate(chrom, 0.5)}")


# part B

import random

def run_ga(pop_size, num_generations, pm, elitism=False):
    # Initialize random population (4-bit chromosomes)
    population = [[random.randint(0,1) for _ in range(4)] for _ in range(pop_size)]
    history = []

    for gen in range(1, num_generations + 1):
        new_population = []

        # Elitism: find the best individual
        if elitism:
            best_individual = max(population, key=fitness)
            new_population.append(best_individual)

        # Generate new population
        while len(new_population) < pop_size:
            # Select parents
            parent1 = roulette_select(population)
            parent2 = roulette_select(population)

            # Random crossover point (1-3, since 0 or 4 wouldn't change anything)
            point = random.randint(1,3)
            off1, off2 = single_point_crossover(parent1, parent2, point)

            # Apply mutation
            off1 = mutate(off1, pm)
            off2 = mutate(off2, pm)

            # Add offspring to new population
            new_population.extend([off1, off2])

        # Trim excess if needed
        population = new_population[:pop_size]

        # Record generation stats
        fitness_vals = [fitness(chrom) for chrom in population]
        decoded_x = [decode(chrom) for chrom in population]
        best_idx = fitness_vals.index(max(fitness_vals))
        best_chrom = population[best_idx]
        best_fit = fitness_vals[best_idx]
        best_x = decoded_x[best_idx]

        history.append((gen, best_fit, best_x))

        # Print generation details
        print(f"\nGeneration {gen}:")
        print("Population Chromosomes:", population)
        print("Decoded x-values:      ", decoded_x)
        print("Fitness values:        ", fitness_vals)
        print(f"Best Individual: {best_chrom} -> x={best_x}, fitness={best_fit}")

    return history

# Parameters as requested
history = run_ga(pop_size=4, num_generations=10, pm=0.1, elitism=False)


# Part C


import random

# Helper functions to replace np.mean
def mean(values):
    return sum(values) / len(values)

# Example fitness and decode functions (replace with your actual functions)
def fitness(chrom):
    # Dummy placeholder
    return sum(chrom) * 10  

def decode(chrom):
    # Dummy placeholder
    return sum(chrom)

# Example GA operators (replace with your actual implementations)
def roulette_select(pop):
    return random.choice(pop)

def single_point_crossover(p1, p2, point):
    off1 = p1[:point] + p2[point:]
    off2 = p2[:point] + p1[point:]
    return off1, off2

def mutate(chrom, pm):
    if random.random() < pm:
        idx = random.randint(0, len(chrom)-1)
        chrom[idx] = 1 - chrom[idx]
    return chrom

# Controlled experiment without NumPy
def controlled_experiment_elitism(trials=30, pop_size=4, num_generations=20, pm=0.1):
    results = {"Elitism": [], "NoElitism": []}

    for elitism in [True, False]:
        best_fitnesses = []
        found_optimum_counts = 0
        generations_to_50_list = []

        for t in range(trials):
            population = [[random.randint(0,1) for _ in range(4)] for _ in range(pop_size)]
            first_reach_50 = None

            for gen in range(1, num_generations+1):
                # New population
                new_population = []
                if elitism:
                    best_individual = max(population, key=fitness)
                    new_population.append(best_individual)

                while len(new_population) < pop_size:
                    parent1 = roulette_select(population)
                    parent2 = roulette_select(population)
                    point = random.randint(1,3)
                    off1, off2 = single_point_crossover(parent1, parent2, point)
                    off1 = mutate(off1, pm)
                    off2 = mutate(off2, pm)
                    new_population.extend([off1, off2])

                population = new_population[:pop_size]

                # Track best fitness
                fitness_vals = [fitness(chrom) for chrom in population]
                decoded_x = [decode(chrom) for chrom in population]
                best_idx = fitness_vals.index(max(fitness_vals))
                best_fit = fitness_vals[best_idx]
                best_x = decoded_x[best_idx]

                if first_reach_50 is None and best_fit >= 50:
                    first_reach_50 = gen

            best_fitnesses.append(best_fit)
            if best_x == 7:
                found_optimum_counts += 1
            generations_to_50_list.append(first_reach_50 if first_reach_50 is not None else num_generations)

        results["Elitism" if elitism else "NoElitism"] = {
            "avg_best_fitness": mean(best_fitnesses),
            "num_found_optimum": found_optimum_counts,
            "avg_gen_to_50": mean(generations_to_50_list)
        }

    return results

# Run the experiment
elitism_results = controlled_experiment_elitism()
print("Elitism Experiment Results (30 trials):")
for key, val in elitism_results.items():
    print(f"{key}: Avg Best Fitness={val['avg_best_fitness']:.2f}, "
          f"Runs found x=7={val['num_found_optimum']}, "
          f"Avg Gen to f≥50={val['avg_gen_to_50']:.2f}")


def controlled_experiment_mutation(mutation_rates=[0.01,0.1,0.3,0.5], trials=30):
    table = []
    for pm in mutation_rates:
        best_fitnesses = []
        for t in range(trials):
            population = [[random.randint(0,1) for _ in range(4)] for _ in range(4)]
            for gen in range(1,21):
                new_population = []
                while len(new_population) < 4:
                    p1 = roulette_select(population)
                    p2 = roulette_select(population)
                    point = random.randint(1,3)
                    off1, off2 = single_point_crossover(p1,p2,point)
                    off1 = mutate(off1, pm)
                    off2 = mutate(off2, pm)
                    new_population.extend([off1, off2])
                population = new_population[:4]

            fitness_vals = [fitness(chrom) for chrom in population]
            best_fitnesses.append(max(fitness_vals))
        avg_best = np.mean(best_fitnesses)
        table.append((pm, avg_best))
    return table

# Run mutation rate experiment
mutation_results = controlled_experiment_mutation()
print("\nAverage Best Fitness per Mutation Rate (30 trials):")
print("pm\tAvg Best Fitness")
for pm, avg_best in mutation_results:
    print(f"{pm:.2f}\t{avg_best:.2f}")
