import random

def first_choice_hc(landscape, start):
    current = start
    path = [current]

    while True:
        moved = False

        # check left
        if current > 1:
            left = current - 1
            if landscape[left - 1] > landscape[current - 1]:
                current = left
                path.append(current)
                moved = True

        # check right
        if not moved and current < len(landscape):
            right = current + 1
            if landscape[right - 1] > landscape[current - 1]:
                current = right
                path.append(current)
                moved = True

        if not moved:
            break

    return path, current


def stochastic_hc(landscape, start):
    current = start
    path = [current]

    while True:
        neighbors = []

        if current > 1:
            neighbors.append(current - 1)
        if current < len(landscape):
            neighbors.append(current + 1)

        better = []
        for n in neighbors:
            if landscape[n - 1] > landscape[current - 1]:
                better.append(n)

        if not better:
            break

        current = random.choice(better)
        path.append(current)

    return path, current

    
landscape = [4, 9, 6, 11, 8, 15, 10, 7, 13, 5, 16, 12]


def main():
    # landscape = [4, 9, 6, 11, 8, 15, 10, 7, 13, 5, 16, 12]
    landscape = [4, 9, 6, 11, 15, 15, 15, 7, 13, 5, 16, 12]

    for start in range(1, 13):

        path, terminal = first_choice_hc(landscape, start)
        print("Start:", start, "| First-Choice | Path:", path,
              "| Terminal:", terminal, "| Steps:", len(path)-1)

        path, terminal = stochastic_hc(landscape, start)
        print("Start:", start, "| Stochastic | Path:", path,
              "| Terminal:", terminal, "| Steps:", len(path)-1)

        print("-" * 50)

main()

#Part B

count_11 = 0
count_local = 0

runs = 50

for i in range(runs):
    path, terminal = stochastic_hc(landscape, 4)

    if terminal == 11:
        count_11 += 1
    else:
        count_local += 1

# Print results
print("Total runs:", runs)
print("Reached state 11:", count_11)
print("Reached local maxima:", count_local)

# Percentages
success_percent = (count_11 / runs) * 100
failure_percent = (count_local / runs) * 100

print("Success %:", success_percent)
print("Failure %:", failure_percent)

#Part C

import random

# First-Choice Hill Climbing with Plateau Detection
def first_choice_hc(landscape, start):
    current = start
    path = [current]

    while True:
        neighbors = []
        moved = False

        # Add neighbors
        if current > 1:
            neighbors.append(current - 1)
        if current < len(landscape):
            neighbors.append(current + 1)

        # Find better neighbors
        better = []
        for n in neighbors:
            if landscape[n - 1] > landscape[current - 1]:
                better.append(n)

        # Plateau detection (YOUR CODE)
        equal_neighbors = [n for n in neighbors if landscape[n - 1] == landscape[current - 1]]
        if not better and equal_neighbors:
            print("Plateau detected at state", current)

        # First-choice: check left first
        for n in neighbors:
            if landscape[n - 1] > landscape[current - 1]:
                current = n
                path.append(current)
                moved = True
                break

        if not moved:
            break

    return path, current


# Stochastic Hill Climbing with Plateau Detection
def stochastic_hc(landscape, start):
    current = start
    path = [current]

    while True:
        neighbors = []

        # Add neighbors
        if current > 1:
            neighbors.append(current - 1)
        if current < len(landscape):
            neighbors.append(current + 1)

        # Find better neighbors
        better = []
        for n in neighbors:
            if landscape[n - 1] > landscape[current - 1]:
                better.append(n)

        # Plateau detection (YOUR CODE)
        equal_neighbors = [n for n in neighbors if landscape[n - 1] == landscape[current - 1]]
        if not better and equal_neighbors:
            print("Plateau detected at state", current)

        if not better:
            break

        # Random move
        current = random.choice(better)
        path.append(current)

    return path, current

def main():
    landscape = [4, 9, 6, 11, 15, 15, 15, 7, 13, 5, 16, 12]

    for start in range(1, 13):

        path, terminal = first_choice_hc(landscape, start)
        print("Start:", start, "| First-Choice | Path:", path,
              "| Terminal:", terminal, "| Steps:", len(path)-1)

        path, terminal = stochastic_hc(landscape, start)
        print("Start:", start, "| Stochastic | Path:", path,
              "| Terminal:", terminal, "| Steps:", len(path)-1)

        print("-" * 50)

main()


import random

# First-Choice Hill Climbing with Sideways Moves
def first_choice_hc_sideways(landscape, start, max_sideways=10):
    current = start
    path = [current]
    sideways = 0

    while True:
        neighbors = []
        moved = False

        if current > 1:
            neighbors.append(current - 1)
        if current < len(landscape):
            neighbors.append(current + 1)

        better = [n for n in neighbors if landscape[n - 1] > landscape[current - 1]]
        equal = [n for n in neighbors if landscape[n - 1] == landscape[current - 1]]

        # Move to better neighbor
        for n in neighbors:
            if landscape[n - 1] > landscape[current - 1]:
                current = n
                path.append(current)
                sideways = 0
                moved = True
                break

        # Sideways move if no better neighbor
        if not moved and equal and sideways < max_sideways:
            current = random.choice(equal)
            path.append(current)
            sideways += 1
            moved = True

        if not moved:
            break

    return path, current

# Stochastic Hill Climbing with Sideways Moves
def stochastic_hc_sideways(landscape, start, max_sideways=10):
    current = start
    path = [current]
    sideways = 0

    while True:
        neighbors = []
        if current > 1:
            neighbors.append(current - 1)
        if current < len(landscape):
            neighbors.append(current + 1)

        better = [n for n in neighbors if landscape[n - 1] > landscape[current - 1]]
        equal = [n for n in neighbors if landscape[n - 1] == landscape[current - 1]]

        if better:
            current = random.choice(better)
            path.append(current)
            sideways = 0
        elif equal and sideways < max_sideways:
            current = random.choice(equal)
            path.append(current)
            sideways += 1
        else:
            break

    return path, current

# Main function to test all starting states
def main():
    # Plateau landscape: states 5,6,7 all = 15
    landscape = [4, 9, 6, 11, 15, 15, 15, 7, 13, 5, 16, 12]

    print("=== First-Choice HC with Sideways Moves ===")
    for start in range(1, 13):
        path, terminal = first_choice_hc_sideways(landscape, start)
        print(f"Start: {start}, Path: {path}, Terminal: {terminal}, Steps: {len(path)-1}")
    print("\n=== Stochastic HC with Sideways Moves ===")
    for start in range(1, 13):
        path, terminal = stochastic_hc_sideways(landscape, start)
        print(f"Start: {start}, Path: {path}, Terminal: {terminal}, Steps: {len(path)-1}")

main()


def compare_success(landscape, runs=1):
    print("=== Without Sideways Moves ===")
    fc_success = 0
    st_success = 0
    for start in range(1, 13):
        for _ in range(runs):
            _, t = first_choice_hc(landscape, start)
            if t == 11: fc_success += 1
            _, t = stochastic_hc(landscape, start)
            if t == 11: st_success += 1
    print("First-Choice reached 11:", fc_success)
    print("Stochastic reached 11:", st_success)

    print("\n=== With Sideways Moves (max 10) ===")
    fc_success = 0
    st_success = 0
    for start in range(1, 13):
        for _ in range(runs):
            _, t = first_choice_hc_sideways(landscape, start)
            if t == 11: fc_success += 1
            _, t = stochastic_hc_sideways(landscape, start)
            if t == 11: st_success += 1
    print("First-Choice reached 11:", fc_success)
    print("Stochastic reached 11:", st_success)

compare_success(landscape, runs=10)
