import copy
from queue import Queue

# Initial board layout
initial_state = [   # Display of how each element corresponds to board:
    [1],            #         _1                            (_0,_0)
    [1,1],          #       _2_ _3_                     (_1,_0) (_1,_1)
    [1,0,1],        #     _4_ _5_ _6_               (_2,_0) (_2,_1) (_2,_2)
    [1,1,1,1],      #   _7_ _8_ _9_ _10         (_3,_0) (_3,_0) (_3,_0) (_3,_3)
    [1,1,1,1,1],    # _11 _12 _13 _14 _15   (_4,_0) (_4,_1) (_4,_2) (_4,_3) (_4,_4)
]

def get_all_possible_moves(initial_state):
    # Initialize an empty list to store all possible moves
    every_possible_move = []
    # Iterate over each element in the board
    for row_counter, row in enumerate(initial_state):
        for col_counter, col in enumerate(row):
            # Check for possible y=x moves
            if row_counter >= 2 and col_counter <= len(initial_state[row_counter-2])-1:
                every_possible_move.append([
                    find_position_by_element(initial_state, row_counter, col_counter),
                    find_position_by_element(initial_state, row_counter-1, col_counter),
                    find_position_by_element(initial_state, row_counter-2, col_counter)
                ])
                every_possible_move.append([
                    find_position_by_element(initial_state, row_counter-2, col_counter),
                    find_position_by_element(initial_state, row_counter-1, col_counter),
                    find_position_by_element(initial_state, row_counter, col_counter)
                ])
            # Check for x=c moves
            if col_counter + 2 <= len(initial_state[row_counter])-1:
                every_possible_move.append([
                    find_position_by_element(initial_state, row_counter, col_counter),
                    find_position_by_element(initial_state, row_counter, col_counter+1),
                    find_position_by_element(initial_state, row_counter, col_counter+2)
                ])
                every_possible_move.append([
                    find_position_by_element(initial_state, row_counter, col_counter+2),
                    find_position_by_element(initial_state, row_counter, col_counter+1),
                    find_position_by_element(initial_state, row_counter, col_counter)
                ])
            # Check for y=-x moves
            if row_counter + 2 <= len(initial_state)-1 and col_counter + 2 <= len(initial_state[row_counter+2])-1:
                every_possible_move.append([
                    find_position_by_element(initial_state, row_counter, col_counter),
                    find_position_by_element(initial_state, row_counter+1, col_counter+1),
                    find_position_by_element(initial_state, row_counter+2, col_counter+2)
                ])
                every_possible_move.append([
                    find_position_by_element(initial_state, row_counter+2, col_counter+2),
                    find_position_by_element(initial_state, row_counter+1, col_counter+1),
                    find_position_by_element(initial_state, row_counter, col_counter)
                ])
    return every_possible_move


def print_state(state):
    """
    Prints board nicely in this format:
             _1_
           _2_ _3_
         _4_ _5_ _6_
       _7_ _8_ _9_ _10
     _11 _12 _13 _14 _15

    Args:
    - state: current state of the board

    Returns:
    - Void
    """
    for i in range(len(state)):
        print(" " * (len(state) - i - 1), end="")
        for j in range(len(state[i])):
            print(state[i][j], end=" ")
        print()

def find_element_by_pos(state, pos):
    """
    Finds element row and col values by number:
    [1],                    _1_
    [1,1],                _2_ _3_
    [1,0,1],     ->     _4_ _5_ _6_
    [1,1,1,1],        _7_ _8_ _9_ _10
    [1,1,1,1,1],    _11 _12 _13 _14 _15

    Args:
    - state: current state of the board
    - pos: value of element to obtain

    Returns:
    - row: row of 2D array
    - col: col of 2D array
    """
    row, col = 0, 0
    for i in range(1, pos):
        if col == len(state[row]) - 1:
            row += 1
            col = 0
        else:
            col += 1
    return row, col

def find_position_by_element(state, row, col):
    """
    Finds the position of an element in a two-dimensional array
    by its row and column indices:
    [1],                               (_0,_0)
    [1,1],                         (_1,_0) (_1,_1)
    [1,0,1],      ->           (_2,_0) (_2,_1) (_2,_2)
    [1,1,1,1],             (_3,_0) (_3,_0) (_3,_0) (_3,_3)
    [1,1,1,1,1],       (_4,_0) (_4,_1) (_4,_2) (_4,_3) (_4,_4)

    Args:
    - state: current state of the board
    - row: row of 2D array
    - col: col of 2D array

    Returns:
    - pos: value of element at given row and col
    """
    pos = 1
    for i in range(row):
        pos += len(state[i])
    pos += col
    return pos

# Returns True if move is valid, False otherwise
def is_valid_move(state, move):
    """
    Determines if move is a valid move. A valid move is one whose values are in this order: [1 1 0]

    Args:
    - state: current state of the board
    - move: 1D array of move

    Returns:
    - True if move is valid
    - False if move is invalid
    """
    jumping, jumped_over, jumped_to = move

    # Check if start position is valid
    row,col = find_element_by_pos(state,jumping)
    if state[row][col] != 1:
        return False
    
    # Check if jumped over marble is valid
    row,col = find_element_by_pos(state, jumped_over)
    if state[row][col] != 1:
        return False
    
    # Check if end position is valid
    row,col = find_element_by_pos(state, jumped_to)
    if state[row][col] != 0:
        return False
    return True

def get_valid_moves(state):
    """
    Finds all possible valid moves from given state

    Args:
    - state: current state of the board

    Returns:
    - valid_moves: 2D array containing all valid moves
    """
    valid_moves = []
    for move in every_possible_move:
        if is_valid_move(state, move):
            valid_moves.append(move)
    return valid_moves

# Function to apply a move to a state and return the new state
def apply_move(state, move):
    """
    Makes changes to the board based on the move. Making a move toggles the values of the positions in the move i.e 1 1 0 -> 0 0 1

    Args:
    - state: current state of the board
    - move: 1D array of move

    Returns:
    - new_state: updated board
    """
    # move is a list of three integers representing the indices of the marbles involved in the move
    jumping, jumped_over, jumped_to = move
    
    # Create a new state as a copy of the original state
    new_state = copy.deepcopy(state)
    
    # Update the new state to reflect the move
    row, col = find_element_by_pos(new_state, jumping)
    new_state[row][col] = 0
    
    row, col = find_element_by_pos(new_state, jumped_over)
    new_state[row][col] = 0
    
    row, col = find_element_by_pos(new_state, jumped_to)
    new_state[row][col] = 1
    
    return new_state

def bfs_solve(initial_state):
    """
    Breadth First Search to solve puzzle. Will print every step to get to solution

    Args:
    - initial_state: state of the board before solve

    Returns:
    - final_state: solved board
    """

    # Initialize Open and closed states
    unvisited = Queue()
    unvisited.put((initial_state, [initial_state]))
    
    visited = {}
    visited[tuple(map(tuple, initial_state))] = None

    # Perform BFS
    while not unvisited.empty():
        final_state, path = unvisited.get()
        # Check if goal found (Sum of all values in board is 1)
        if sum([sum(row) for row in final_state]) == 1:
            # Print steps 
            step_count = 0
            for step in path:
                step_count += 1
                print("Step " + str(step_count) +":")
                print_state(step)
                print(" ")
            return final_state
        
        # Generate all possible next moves
        moves = get_valid_moves(final_state)
        for move in moves:
            # Apply the move
            new_state = apply_move(final_state, move)
            # Check if the new state has been visited before
            if tuple(map(tuple, new_state)) not in visited:
                visited[tuple(map(tuple, new_state))] = final_state
                unvisited.put((new_state, path + [new_state]))
    
    return None


def dfs_solve(initial_state):
    """
    Depth First Search to solve puzzle. Will print every step to get to solution

    Args:
    - initial_state: state of the board before solve

    Returns:
    - final_state: solved board
    """

    # Initialize Open and closed states
    unvisited = [(initial_state, [initial_state])]
    
    visited = {}
    visited[tuple(map(tuple, initial_state))] = None

    # Perform DFS
    while unvisited:
        final_state, path = unvisited.pop()
        # Check if goal found (Sum of all values in board is 1)
        if sum([sum(row) for row in final_state]) == 1:
            # Print steps 
            step_count = 0
            for step in path:
                step_count += 1
                print("Step " + str(step_count) +":")
                print_state(step)
                print(" ")
            return final_state
        # Generate all possible next moves
        moves = get_valid_moves(final_state)
        for move in moves:
            # Apply the move
            new_state = apply_move(final_state, move)
            # Check if the new state has been visited before
            if tuple(map(tuple, new_state)) not in visited:
                visited[tuple(map(tuple, new_state))] = final_state
                unvisited.append((new_state, path + [new_state]))
    
    return None

every_possible_move = get_all_possible_moves(initial_state)

# Main Program
current_state = copy.deepcopy(initial_state)

print("BFS finder: ")
solution = bfs_solve(current_state)
    
if solution is not None:
    print("BFS Solution found:")
    print_state(solution)    
else:
    print("No solution!")
print()

print("DFS finder: ")
solution = dfs_solve(current_state)
    
if solution is not None:
    print("DFS Solution found:")
    print_state(solution)    
else:
    print("No solution!")




