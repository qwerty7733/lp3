# DAA Practical 4: N-Queens with the FIRST queen already placed, rest placed by Backtracking
# Rule: no two queens may share the same row, column or diagonal.


def is_safe(board, row, col):                 # can a queen be put at (row, col)?
    for r in range(len(board)):               # check every row of the board
        c = board[r]                          # column of the queen in row r (-1 means empty row)
        if c == -1 or r == row:               # skip empty rows and the row we are filling
            continue                          # nothing to compare
        if c == col:                          # same column -> queens attack each other
            return False                      # not safe
        if abs(c - col) == abs(r - row):      # same diagonal: row distance == column distance
            return False                      # not safe
    return True                               # no conflict found -> safe


def place(board, row, fixed_row):             # try to fill rows row, row+1, ..., n-1
    n = len(board)                            # board size
    if row == n:                              # all rows are filled
        return True                           # solution found
    if row == fixed_row:                      # this row already has the first (given) queen
        return place(board, row + 1, fixed_row)   # just move on to the next row
    for col in range(n):                      # try every column in this row
        if is_safe(board, row, col):          # only if it is not attacked
            board[row] = col                  # place the queen
            if place(board, row + 1, fixed_row):  # try to place the remaining queens
                return True                   # success, stop searching
            board[row] = -1                   # BACKTRACK: remove the queen and try the next column
    return False                              # no column worked -> go back to the previous row


def n_queens(n, first_row, first_col):        # main function (rows and columns start from 0)
    board = [-1] * n                          # board[r] = column of queen in row r, -1 = empty
    board[first_row] = first_col              # put the first queen where the user asked
    if place(board, 0, first_row):            # backtrack to place the other queens
        return board                          # return the solved board
    return None                               # no solution with this first queen


def show(n, first_row, first_col):            # run and print the matrix
    print(f"\nN = {n}, first queen at row {first_row + 1}, column {first_col + 1}")   # 1-based for humans
    board = n_queens(n, first_row, first_col)   # solve
    if board is None:                         # nothing found
        print("No solution possible with this first queen.")   # tell the user
        return                                # stop here
    for r in range(n):                        # print the n x n matrix
        print(" ".join("1" if board[r] == c else "0" for c in range(n)))   # 1 = queen, 0 = empty


show(4, 0, 1)                                 # 4-Queens, first queen at (1, 2) -> solution exists
show(4, 0, 0)                                 # 4-Queens, first queen at corner (1, 1) -> no solution
show(8, 0, 0)                                 # 8-Queens, first queen at the corner
# Time  = O(N!) in the worst case (backtracking cuts off most branches early)
# Space = O(N)  : the board list + recursion depth of N
