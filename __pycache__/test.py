import copy
from queue import Queue


# MARBLE SOLITAIRE
# Initial board layout
initial_state = [   # Display of how each element corresponds to board:
    [1],            #         _1                            (_0,_0)
    [1,1],          #       _2_ _3_                     (_1,_0) (_1,_1)
    [1,0,1],        #     _4_ _5_ _6_               (_2,_0) (_2,_1) (_2,_2)
    [1,1,1,1],      #   _7_ _8_ _9_ _10         (_3,_0) (_3,_0) (_3,_0) (_3,_3)
    [1,1,1,1,1],    # _11 _12 _13 _14 _15   (_4,_0) (_4,_1) (_4,_2) (_4,_3) (_4,_4)
]

# 2D array of every possible move
every_possible_move = [
    # Row 1
    [1,2,4],
    [1,3,6],
    
    # Row 2
    [2,4,7],
    [2,5,9],

    [3,5,8],
    [3,6,10],

    # Row 3
    [4,2,1],
    [4,5,6],
    [4,7,11],
    [4,8,13],

    [5,8,12],
    [5,9,14],

    [6,3,1],
    [6,5,4],
    [6,9,13],
    [6,10,15],

    # Row 4
    [7,4,2],
    [7,8,9],

    [8,5,3],
    [8,9,10],

    [9,5,2],
    [9,8,7],

    [10,6,3],
    [10,9,8],

    # Row 5
    [11,7,4],
    [11,12,13],

    [12,8,5],
    [12,13,14],

    [13,8,4],
    [13,12,11],
    [13,9,6],
    [13,14,15],

    [14,9,5],
    [14,13,12],

    [15,10,6],
    [15,14,13],
]

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
        # Print spaces to align elements properly
        print(" " * (len(state) - i - 1), end="")
        # Print each element in the row with a space in between
        for j in range(len(state[i])):
            print(state[i][j], end=" ")
        print()

# Input is board and position, output is row and col to access that element in the board
def find_element_by_pos(state, pos):
    row, col = 0, 0
    for i in range(1, pos):
        if col == len(state[row]) - 1:
            row += 1
            col = 0
        else:
            col += 1
    return row, col


# Returns True if move is valid, False otherwise
def is_valid_move(state, move):
    # move is a list of three integers representing the indices of the marbles involved in the move
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

# Returns a list of valid moves for the current state
def get_valid_moves(state):
    valid_moves = []
    for move in every_possible_move:
        if is_valid_move(state, move):
            valid_moves.append(move)
    return valid_moves

# Function to apply a move to a state and return the new state
def apply_move(state, move):
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

# Breadth First Search function to solve the puzzle
def bfs_solve(initial_state):
    # Create a queue to store states
    queue = Queue()
    
    # Enqueue the initial state
    queue.put(initial_state)
    
    # Dictionary to store previous state of each state
    previous = {}
    previous[tuple(map(tuple, initial_state))] = None
    
    # Perform BFS
    while not queue.empty():
        state = queue.get()
        
        # Check if current state is goal state : Sum of all values in array is 1
        if sum([sum(row) for row in state]) == 1:
            for s in initial_state:
                print(s)
                print(" ")
            return state
        
        # Generate all possible next moves
        moves = get_valid_moves(state)
        for move in moves:
            # Apply the move to create a new state
            new_state = apply_move(state, move)
            
            # Check if the new state has been visited before
            if tuple(map(tuple, new_state)) not in previous:
                previous[tuple(map(tuple, new_state))] = state
                queue.put(new_state)
    
    # No solution found
    return None



# VVV TESTING VVV

# Initialize Current State with the initial values
current_state = copy.deepcopy(initial_state)
print("Board before any move")
#print_state(current_state)
# Solve the puzzle
solution = bfs_solve(current_state)
    
# Print the solution
if solution is not None:
    print("Solution found:")
    print_state(solution)    
else:
    print("No solution found.")

# # Print board
# print("Board before any move")
# print_state(current_state)

# # Make legal move
# move = get_valid_moves(current_state)[1]
# current_state = apply_move(current_state, move)

# # Print board
# print("Board after legal move")
# print_state(current_state)















#print(is_valid_move(current_state, every_possible_move[26]))

#print(get_valid_moves(current_state))

#print(is_valid_move(current_state,every_possible_move[26]))


#testing
#make_move(every_possible_move[27])
#print_state(current_state)


# NOTE:
# # A legal move must be: a move on the move list, first two elements must be 1, last element must be 0
# # If i select a move [A,B,C], C must be a 0 and A and B must be 1 (ensure checks are made before function call)
# # When a move is made, the elements in the move list are toggled. i.e (1 1 0) becomes (0 0 1)

#If i select a move, [A,B,C]
#The following move HAS to end with A or B i.e [X,X,A] OR [X,X,B]