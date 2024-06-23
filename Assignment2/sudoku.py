import sys

# Checks current row, column and grid(3x3) for valid value
def valid_check(sudoku, row, col, val):
    for i in range(9):  # Checks current column
        if sudoku[i][col] == val:
            return False

    for i in range(9):  # Checks current row
        if sudoku[row][i] == val:
            return False

    row_start = (row // 3) * 3
    col_start = (col // 3) * 3
    for i in range(3):  # Checks current grid(3x3)
        for j in range(3):
            if sudoku[row_start + i][col_start + j] == val:
                return False

    return True

# Find cells that has one possibility
def find_one_possibility(sudoku, row, col):
    possibilities = [num for num in range(1, 10) if valid_check(sudoku, row, col, num)]
    return possibilities[0] if len(possibilities) == 1 else None

# Solves sudoku and prints step by step
def solution_for_sudoku(sudoku_board, output_file):
    step_counter = 1

    # Find cells with value zero
    zero_cells = [(i, j) for i in range(9) for j in range(9) if sudoku_board[i][j] == 0]

    while True:
        found = False
        cell = None
        index = 0

        for candidate in zero_cells:  # Determine candidates to fill
            i, j = candidate
            if sudoku_board[i][j] == 0 and find_one_possibility(sudoku_board, i, j):
                cell = (i, j)
                found = True
                break
            index += 1

        if not found:
            break

        zero_cells.pop(index)  # Remove filled empty cells

        row, col = cell
        val = find_one_possibility(sudoku_board, row, col)  # Value to be placed in empty cell

        output_file.write("-" * 18 + "\n")
        output_file.write("Step {} - {} @ R{}C{}\n".format(step_counter, val, row + 1, col + 1))
        output_file.write("-" * 18 + "\n")

        sudoku_board[row][col] = val  # Place value into empty cell

        print_sudoku_to_file(sudoku_board, output_file)
        step_counter += 1

    step_counter = 1

    while True:
        empty_rows = [i for i in range(9) if 0 in sudoku_board[i]]  # Row of empty cells
        empty_columns = [j for j in range(9) if any(sudoku_board[i][j] == 0 for i in range(9))]  # Column of empty cells

        if not (empty_rows or empty_columns):
            break

        for row in empty_rows:
            for val in range(1, 10):
                if val not in sudoku_board[row]:
                    col = sudoku_board[row].index(0)  # Find index of zero cells to find out which column it is in

                    output_file.write("-" * 18 + "\n")
                    output_file.write("Step {} - {} @ R{}C{}\n".format(step_counter, val, row + 1, col + 1))
                    output_file.write("-" * 18 + "\n")

                    sudoku_board[row][col] = val  # Place value into empty cell

                    print_sudoku_to_file(sudoku_board, output_file)
                    step_counter += 1

        for col in empty_columns:
            for val in range(1, 10):
                found = False
                # Check if any element in the column is equal to value
                for i in range(9):
                    if sudoku_board[i][col] == val:
                        found = True
                        break

                if not found:
                    # Find the index of the first empty cell in the column
                    row = -1
                    for i in range(9):
                        if sudoku_board[i][col] == 0:
                            row = i
                            break

                    if row != -1:
                        # Update the Sudoku board and print the step information
                        output_file.write("-" * 18 + "\n")
                        output_file.write("Step {} - {} @ R{}C{}\n".format(step_counter, val, row + 1, col + 1))
                        output_file.write("-" * 18 + "\n")
                        sudoku_board[row][col] = val
                        print_sudoku_to_file(sudoku_board, output_file)
                        step_counter += 1

# Converts input file to 2D array with integers
def read_board_from_file(input_file):
    lines = input_file.readlines()
    board = [[int(num) for num in line.split()] for line in lines]
    return board

# Prints sudoku to output file step by step
def print_sudoku_to_file(sudoku, file):
    for row in sudoku:
        for val in row:
            file.write("{} ".format(val))
        file.write("\n")

# Call all the functions for result
def main():
    input_file = open(sys.argv[1],"r")
    output_file = open(sys.argv[2], "w")

    sudoku_board = read_board_from_file(input_file)

    solution_for_sudoku(sudoku_board,output_file)

    output_file.write("-"*18)

    input_file.close()
    output_file.flush()
    output_file.close()

if __name__ == "__main__":
    main()