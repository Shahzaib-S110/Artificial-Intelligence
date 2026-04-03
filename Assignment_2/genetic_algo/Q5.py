# part A

import random

def random_chromosome():
    """Generates a random chromosome for 6 courses."""
    chromosome = []
    for _ in range(6):
        room = random.randint(0, 2)   # 0,1,2 for R1,R2,R3
        slot = random.randint(0, 3)   # 0,1,2,3 for T1-T4
        chromosome.append((room, slot))
    return chromosome

def count_conflicts(chromosome):
    conflicts = 0
    n = len(chromosome)
    for i in range(n):
        for j in range(i + 1, n):
            if chromosome[i] == chromosome[j]:
                conflicts += 1
    return conflicts

def fitness(chromosome):
    return 100 - 10 * count_conflicts(chromosome)

print("{:<20} {:<10} {:<10}".format("Chromosome", "Conflicts", "Fitness"))

for _ in range(5):
    chrom = random_chromosome()
    conf = count_conflicts(chrom)
    fit = fitness(chrom)
    print("{:<20} {:<10} {:<10}".format(str(chrom), conf, fit))


# part B

import random

def crossover(p1, p2, point):
    """
    Single-point crossover: swaps tails of parent chromosomes.
    This may produce conflicts (two courses in same room+slot).
    """
    child1 = p1[:point] + p2[point:]
    child2 = p2[:point] + p1[point:]
    return child1, child2

# Two example parent chromosomes
parent1 = [(0, 0), (1, 1), (2, 0), (0, 2), (1, 2), (2, 1)]
parent2 = [(1, 0), (0, 1), (2, 0), (1, 2), (0, 2), (2, 3)]

# Single-point crossover at point=3
child1, child2 = crossover(parent1, parent2, point=3)

print("Parent1:", parent1)
print("Parent2:", parent2)
print("Child1 :", child1, "Conflicts:", count_conflicts(child1))
print("Child2 :", child2, "Conflicts:", count_conflicts(child2))



def repair(chromosome):
    """
    Repair chromosome by resolving conflicts.
    Conflicting courses are reassigned to a free (room, slot).
    If no free slot exists, assign randomly.
    """
    n_courses = len(chromosome)
    seen = set()  # track occupied (room, slot)
    repaired = []

    for course in chromosome:
        if course not in seen:
            repaired.append(course)
            seen.add(course)
        else:
            # Conflict detected, find free options
            free_slots = [(r, s) for r in range(3) for s in range(4) if (r, s) not in seen]
            if free_slots:
                new_assignment = random.choice(free_slots)
            else:
                # If all slots used, assign randomly
                new_assignment = (random.randint(0, 2), random.randint(0, 3))
            repaired.append(new_assignment)
            seen.add(new_assignment)
    return repaired

# Manually create a conflicting chromosome
conflict_chrom = [(0, 0), (1, 1), (0, 0), (2, 2), (1, 1), (2, 3)]
print("Before repair:", conflict_chrom)
print("Conflicts:", count_conflicts(conflict_chrom))

# Repair the chromosome
repaired_chrom = repair(conflict_chrom)
print("After repair :", repaired_chrom)
print("Conflicts:", count_conflicts(repaired_chrom))


# part C

import random

# Count conflicts
def count_conflicts(chromosome):
    conflicts = 0
    n = len(chromosome)
    for i in range(n):
        for j in range(i+1, n):
            if chromosome[i] == chromosome[j]:
                conflicts += 1
    return conflicts

# Fitness function
def fitness(chromosome):
    return 100 - 10 * count_conflicts(chromosome)

# Random chromosome
def random_chromosome():
    return [(random.randint(0,2), random.randint(0,3)) for _ in range(6)]

# Crossover
def crossover(p1, p2, point):
    child1 = p1[:point] + p2[point:]
    child2 = p2[:point] + p1[point:]
    return child1, child2

# Repair function
def repair(chromosome):
    seen = set()
    repaired = []
    for course in chromosome:
        if course not in seen:
            repaired.append(course)
            seen.add(course)
        else:
            free_slots = [(r,s) for r in range(3) for s in range(4) if (r,s) not in seen]
            if free_slots:
                new_assignment = random.choice(free_slots)
            else:
                new_assignment = (random.randint(0,2), random.randint(0,3))
            repaired.append(new_assignment)
            seen.add(new_assignment)
    return repaired

# Mutation
def mutate(chromosome, pm):
    mutated = chromosome.copy()
    for i in range(len(mutated)):
        if random.random() < pm:
            mutated[i] = (random.randint(0,2), random.randint(0,3))
    return mutated



def tournament_selection(population):
    i1, i2 = random.sample(range(len(population)), 2)
    return population[i1] if fitness(population[i1]) >= fitness(population[i2]) else population[i2]

def run_scheduling_ga(pop_size=20, generations=50, pm=0.1):
    # Initialize population
    population = [random_chromosome() for _ in range(pop_size)]
    best_per_gen = []

    for gen in range(1, generations+1):
        new_population = []

        while len(new_population) < pop_size:
            # Select parents
            p1 = tournament_selection(population)
            p2 = tournament_selection(population)

            # Crossover
            point = random.randint(1, 5)  # crossover point between 1 and 5
            child1, child2 = crossover(p1, p2, point)

            # Repair children
            child1 = repair(child1)
            child2 = repair(child2)

            # Mutation
            child1 = mutate(child1, pm)
            child2 = mutate(child2, pm)

            # Repair again after mutation (optional, safer)
            child1 = repair(child1)
            child2 = repair(child2)

            new_population.extend([child1, child2])

        # Replace old population
        population = new_population[:pop_size]

        # Track best fitness
        best_chrom = max(population, key=fitness)
        best_fit = fitness(best_chrom)
        best_per_gen.append(best_fit)

        # Check for conflict-free solution
        if count_conflicts(best_chrom) == 0:
            print(f"Solution found at generation {gen}: {best_chrom}")
            print(f"Conflicts: {count_conflicts(best_chrom)}")
            return best_chrom, best_fit, best_per_gen

    # If no perfect solution found
    best_chrom = max(population, key=fitness)
    print("No conflict-free solution found.")
    print("Best schedule:", best_chrom)
    print("Conflicts:", count_conflicts(best_chrom))
    return best_chrom, fitness(best_chrom), best_per_gen


best_schedule, best_fit, history = run_scheduling_ga(pop_size=20, generations=50, pm=0.1)

print("\nBest schedule found:")
for idx, (room, slot) in enumerate(best_schedule, 1):
    print(f"C{idx}: Room {room+1}, Time Slot {slot+1}")

print("Best fitness:", best_fit)
print("Conflict count:", count_conflicts(best_schedule))
