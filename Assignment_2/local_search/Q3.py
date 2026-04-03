#Part A 

import random

def diagnose_hc(landscape, start):
    current = start
    visited = []  # sequence of visited states

    while True:
        neighbors = [s for s in landscape.keys() if abs(s - current) == 1]
        better = [n for n in neighbors if landscape[n] > landscape[current]]
        equal = [n for n in neighbors if landscape[n] == landscape[current]]

        # Local Maximum: no better or equal neighbor
        if not better and not equal:
            print(f"Terminated at state {current} with f={landscape[current]}. Failure mode: local maximum")
            return

        # Plateau: no better neighbors, at least one equal, and all equal neighbors only visited once
        if not better and equal and all(visited.count(n) >= 1 for n in equal):
            print(f"Terminated at state {current} with f={landscape[current]}. Failure mode: plateau")
            return

        # Ridge: revisiting a state with no better neighbor
        if current in visited and not better:
            print(f"Terminated at state {current} with f={landscape[current]}. Failure mode: ridge")
            return

        # Move to next state
        if better:
            current = random.choice(better)
        else:
            current = random.choice(equal)

        visited.append(current)

print("=== Local Maximum Test ===")
diagnose_hc(landscape_local_max, start=2)

print("\n=== Plateau Test ===")
diagnose_hc(landscape_plateau, start=3)

# Part B

def count_conflicts(board):
    """
    Counts the number of attacking pairs of queens on the board.
    Lower is better; 0 means no conflicts.
    board[i] = row of queen in column i
    """
    conflicts = 0
    N = len(board)
    for i in range(N):
        for j in range(i+1, N):
            if board[i] == board[j] or abs(board[i] - board[j]) == abs(i - j):
                conflicts += 1
    return conflicts


import random

def stochastic_hc_nqueens(board, max_iterations=1000):
    """
    Perform Stochastic Hill Climbing on an N-Queens board.
    """
    N = len(board)
    for _ in range(max_iterations):
        current_conflicts = count_conflicts(board)
        # Generate a random pair of columns to swap
        c1, c2 = random.sample(range(N), 2)
        board[c1], board[c2] = board[c2], board[c1]  # swap
        new_conflicts = count_conflicts(board)
        if new_conflicts >= current_conflicts:  # swap not better, revert
            board[c1], board[c2] = board[c2], board[c1]
        if new_conflicts == 0:
            return board, True  # solution found
    return board, False  # no solution in this iteration

def solve_nqueens_rrhc(num_restarts=100):
    N = 8
    for attempt in range(1, num_restarts + 1):
        board = list(range(N))
        random.shuffle(board)  # random initial configuration
        board, solved = stochastic_hc_nqueens(board)
        if solved:
            print(f"Solution found after {attempt} restart(s)!")
            return board, attempt
    print("No solution found after maximum restarts.")
    return None, num_restarts

def print_board(board):
    N = len(board)
    for row in range(N):
        line = ""
        for col in range(N):
            if board[col] == row:
                line += "Q "
            else:
                line += ". "
        print(line)

final_board, restarts_needed = solve_nqueens_rrhc(100)

if final_board:
    print("\nFinal board state (column: row):", final_board)
    print("\nVisual board:")
    print_board(final_board)

print("\n=== Ridge Test ===")
diagnose_hc(landscape_ridge, start=2)
