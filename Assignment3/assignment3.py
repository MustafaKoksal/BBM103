import sys

def print_output(board):  # Print output to the terminal
    for row in board:
        for val in row:
            print("{} ".format(val), end='')
        print()
    print()

def read_input_file(filename):  # Read input from the text file
    input_file = open(filename, "r")
    lines = input_file.readlines()
    # Converting text file to the list of integers
    board = [[int(num) for num in line.split()] for line in lines]
    input_file.close()
    return board

def is_valid_cell(board, row, col):  # Check validity of cells
    return (0 <= row < len(board)) and (0 <= col < len(board[0]))

def find_neighbors(board, row, col):  # Find nearby neighbors for selected cell
    neighbors = []

    # Check top
    if is_valid_cell(board,row + 1, col):
        neighbors.append((row + 1, col))

    # Check right
    if is_valid_cell(board,row, col + 1):
        neighbors.append((row, col + 1))

    # Check bottom
    if is_valid_cell(board,row - 1, col):
        neighbors.append((row - 1, col))

    # Check left
    if is_valid_cell(board,row, col - 1):
        neighbors.append((row, col - 1))

    return neighbors

def process_board(board, selected_row, selected_col):  # Determine interacting cells with the same value
    global deleted_cells

    value = board[selected_row][selected_col]
    stack = [(selected_row, selected_col)]
    neighbors_found = False
    deleted_cells = []

    while stack:
        # Determine the current row and column then delete them from the stack
        current_row, current_col = stack.pop()

        # Assign value -1 to current cell
        if board[current_row][current_col] == value:
            if neighbors_found:
                board[current_row][current_col] = -1
                deleted_cells.append((current_row,current_col))

            neighbors = find_neighbors(board,current_row, current_col)

            # Append interacting cells with the same value to the stack
            for n_row, n_col in neighbors:
                if board[n_row][n_col] == value and board[n_row][n_col] != -1:
                    stack.append((n_row, n_col))
                    deleted_cells.append((n_row,n_col))
                    neighbors_found = True

        # If has no neighbors with the same value, don't change anything
        if neighbors_found is False:
               print("No movement happened try again\n")


def shifting_board(board):  # Edit cells with a value of -1 then shift the board
    # Convert cells with a value of -1 to empty cells
    for i in range(len(board[0])):
        for j in range(len(board)):
            if board[j][i] == -1:
                board[j][i] = ' '

    # Bring down the cells above that are empty below
    for i in range(len(board)-1):
        for j in range(len(board[0])):
            for k in range(1, len(board)):
                if board[k][j] == ' ':
                    board[k][j] = board[k - 1][j]
                    board[k - 1][j] = ' '

    return board

def check_neighbors(board):  # Check if there are neighbor cells with the same value
    for i in range(len(board)):
        for j in range(len(board[0])):
            value = board[i][j]
            if board[i][j] != ' ':
                neighbors = find_neighbors(board,i,j)
                for row, col in neighbors:
                    if board[row][col] == value:
                        return True

    return False

def remove_empty_column(board,col):  # Remove column if all the elements are empty in column
    for i in range(len(board)):
        del board[i][col]

def remove_empty_row(board,row):  # Remove row if all the elements are empty in row
       del board[row]

def find_empty_columns(board):  # Check all columns to find empty ones if there are
    empty_column_number = None

    for col in range(len(board[0])):
        if all((row[col]) == ' ' for row in board):
            empty_column_number = col
            break

    return empty_column_number

def find_empty_rows(board): # Check all rows to find empty ones if there are
    empty_row_numbers = []

    for row in range(len(board)):
        if all(cell == ' ' for cell in board[row]):
            empty_row_numbers.append(row)
            break

    return empty_row_numbers

def execute_game():  # Call all the functions to execute the game
    # Get input file from the user
    filename = sys.argv[1]
    board = read_input_file(filename)

    print_output(board)

    score = 0

    print("Your score is: {}\n".format(score))

    while check_neighbors(board):
        row, col = map(int, input("Please enter a row and a column number: ").split())
        print()

        # Check current row and column's validity
        if row > len(board) or col > len(board[0]) or row <= 0 or col <= 0:
            print("Please enter a correct size!\n")
            continue

        # Decrease number of row and column for true indexes
        row -= 1; col-= 1

        value = board[row][col]

        process_board(board, row, col)

        # Delete duplicates from deleted cells list
        set_deleted_cells = set(deleted_cells)

        score += len(set_deleted_cells) * value

        shifted_board = shifting_board(board)

        # Delete empty columns
        for i in range(len(board[0])):
            empty_column_number = find_empty_columns(shifted_board)

            if empty_column_number is not None:
                remove_empty_column(shifted_board, empty_column_number)

        # Delete empty rows
        empty_row_numbers = find_empty_rows(shifted_board)
        for empty_row_number in empty_row_numbers:
            remove_empty_row(shifted_board, empty_row_number)

        print_output(shifted_board)

        print("Your score is: {}\n".format(score))
    print("Game over")

execute_game()
