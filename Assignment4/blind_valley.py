import sys


def read_input():
    input_file = open(sys.argv[1], 'r')
    lines = input_file.readlines()

    # Take constraints from input file as an integer
    constraints = [[int(num) for num in line.split()] for line in lines[:4]]
    constraints = [elt for elt in constraints if elt]

    # Take tile directions from input file
    valid_directions = {'L', 'R', 'U', 'D'}
    board_template = [[direction for direction in line.split() if direction in valid_directions] for line in lines]
    board_template = [elt for elt in board_template if elt]

    input_file.close()

    return constraints, board_template


def find_match(board, board_template, row, col):  # Find match for current row and column
    if not is_valid_cell(board, row, col):
        return False

    # Find match for left('L')
    if is_valid_cell(board, row, col + 1):
        if board_template[row][col] == 'L' and board_template[row][col + 1] == 'R':
            return (row, col + 1)

    # Find match for right('R')
    if is_valid_cell(board, row + 1, col):
        if board_template[row][col] == 'U' and board_template[row + 1][col] == 'D':
            return (row + 1, col)

    return None


def is_valid_cell(board, row, col):  # Check validity of current cell
    return (0 <= row < len(board)) and (0 <= col < len(board[0]))


def check_neighbours(board, row, col):
    # Check if current cell is same as its neighbors for 'H' and 'B'
    if board[row][col] == 'H':
        if is_valid_cell(board, row + 1, col) and board[row + 1][col] == 'H':
                return False

        if is_valid_cell(board, row, col + 1) and board[row][col + 1] == 'H':
                return False

        if is_valid_cell(board, row - 1, col) and board[row - 1][col] == 'H':
                return False

        if is_valid_cell(board, row, col - 1) and board[row][col - 1] == 'H':
                return False

    if board[row][col] == 'B':
        if is_valid_cell(board, row + 1, col) and board[row + 1][col] == 'B':
                return False

        if is_valid_cell(board, row, col + 1) and board[row][col + 1] == 'B':
                return False

        if is_valid_cell(board, row - 1, col) and board[row - 1][col] == 'B':
                return False

        if is_valid_cell(board, row, col - 1) and board[row][col - 1] == 'B':
                return False

    return True


def check_constraints(board, constraints):  # Check the entire board according to constraints
    # Check for row
    for r, row_constraint in enumerate(constraints[0]):
        if row_constraint != -1 and board[r].count('H') != row_constraint:
            return False

    for r, row_constraint in enumerate(constraints[1]):
        if row_constraint != -1 and board[r].count('B') != row_constraint:
            return False

    # Check for column
    for c, col_constraint in enumerate(constraints[2]):
        if col_constraint != -1 and sum(
                1 for i in range(len(board)) if is_valid_cell(board, i, c) and board[i][c] == 'H') != col_constraint:
            return False

    for c, col_constraint in enumerate(constraints[3]):
        if col_constraint != -1 and sum(
                1 for i in range(len(board)) if is_valid_cell(board, i, c) and board[i][c] == 'B') != col_constraint:
            return False

    return True

def solving_blind_valley(board, constraints, board_template, row=0, col=0):
    # If the board has been completed, check the board according to rules
    if row == len(board) - 1 and col == len(board[0]) - 1:
        if check_constraints(board, constraints):
            return True

    # If current cell is at the end of the row, move to next row
    if col == len(board[0]):
        return solving_blind_valley(board, constraints, board_template, row + 1, 0)

    if row < len(board) and col < len(board[0]):
        # If the cell is already filled, move to next column
        if board[row][col] != ' ' and check_neighbours(board, row, col):
            return solving_blind_valley(board, constraints, board_template, row, col + 1)

        match = find_match(board, board_template, row, col)

        # Place 'H', 'B' and 'N's to the board
        if board[row][col] == ' ' and match is not None:
            for tile in ["H", "B", "N"]:
                board[row][col] = tile
                m_row, m_col = match

                if tile == "H" and check_neighbours(board,row,col):
                    board[m_row][m_col] = "B"
                elif tile == "B" and check_neighbours(board, row, col):
                    board[m_row][m_col] = "H"
                elif tile == 'N' and check_neighbours(board, row, col):
                    board[m_row][m_col] = "N"

                # If board is correct, stop backtracking
                if solving_blind_valley(board, constraints, board_template, row, col + 1):
                    return True

                # Backtracking
                board[row][col] = ' '
                board[m_row][m_col] = ' '

    return False


def create_board(board_template):  # Create an empty board
    board = [[' ' for _ in range(len(board_template[0]))] for _ in range(len(board_template))]
    return board


def is_there_solution(board, constraints, board_template, output_file):
    # If the final board is correct, print the board
    if solving_blind_valley(board, constraints, board_template):
        print_board(board, output_file)
    else:
        output_file.write("No solution!")


def print_board(board, output_file):
    # Print the board with a space between each letter
    for i, row in enumerate(board):
        output_file.write(" ".join(row))
        if i < len(board) - 1:  # Add a newline unless it's the last row
            output_file.write("\n")


def main():
    output_file = open(sys.argv[2], 'w')
    constraints, board_template = read_input()
    board = create_board(board_template)
    is_there_solution(board, constraints, board_template, output_file)
    output_file.flush()
    output_file.close()


if __name__ == '__main__':
    main()