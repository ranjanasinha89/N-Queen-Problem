#!/usr/bin/env python
# a0.py : Solve the N-Rooks/N-queen/N-knight problem!
# Ranjana, 2018
# Updated the code given in class

import sys
from collections import deque
import time

# Count # of pieces in given row
def count_on_row(board, row):
    return sum(board[row])


# Count # of pieces in given column
def count_on_col(board, col):
    return sum([row[col] for row in board])


# Count total # of pieces on board
def count_pieces(board):
    return sum([sum(row) for row in board])


# Return a string with the board rendered in a human-friendly format
def printable_board(board):
    boardstr = ""
    for row in range(N):
        boardstr += "\n"
        for col in range(N):
            if [row+1, col+1] in coordinates:
                boardstr+= "X "
            elif board[row][col] == 1:
                if type == "nknight":
                    boardstr+= "K "
                elif type == "nqueen":
                    boardstr+= "Q "
                elif type == "nrook":
                    boardstr+= "R "
            else:
                boardstr+= "_ "
    return boardstr

# Add a piece to the board at the given position, and return a new board (doesn't change original)
def add_piece(board, row, col):
    return board[0:row] + [board[row][0:col] + [1, ] + board[row][col + 1:]] + board[row + 1:]

def check_diagonals(board, row, col):
    row_ind = row
    col_ind = col

    while(row_ind < N and col_ind < N):
        if board[row_ind][col_ind] == 1:
            return False

        row_ind = row_ind + 1
        col_ind = col_ind + 1

    row_ind = row
    col_ind = col

    while(row_ind >= 0 and col_ind >= 0):
        if board[row_ind][col_ind] == 1:
            return False

        row_ind = row_ind - 1
        col_ind = col_ind - 1

    row_ind = row
    col_ind = col

    while(row_ind >= 0 and col_ind < N):
        if board[row_ind][col_ind] == 1:
            return False

        row_ind = row_ind - 1
        col_ind = col_ind + 1

    row_ind = row
    col_ind = col

    while(row_ind < N and col_ind >= 0):
        if board[row_ind][col_ind] == 1:
            return False

        row_ind = row_ind + 1
        col_ind = col_ind - 1

    return True

def check_attacking_nights(board, r, c):
# For any knight placed at (r,c), it can have maximum of 8 attaking nights at locations (r-2, c-1), (r-2, c+1), (r-1, c-2), (r-1, c+2),
# (r+1,c-2), (r+1,c+2), (r+2,c-1) and (r+2, c+1), if any of these locations have a knight already present this function returns False. Only if all the eight
# locations are empty it returns True.
    if (r - 2) >= 0:
        if (c - 1) >= 0:
            if board[r - 2][c - 1] == 1:
                return False
        if (c + 1) < N:
            if board[r - 2][c + 1] == 1:
                return False
    if (r - 1) >= 0:
        if (c - 2) >= 0:
            if board[r - 1][c - 2] == 1:
                return False
        if (c + 2) < N:
            if board[r - 1][c + 2] == 1:
                return False
    if (r + 1) < N:
        if (c - 2) >= 0:
            if board[r + 1][c - 2] == 1:
                return False
        if (c + 2) < N:
            if board[r + 1][c + 2] == 1:
                return False
    if (r + 2) < N:
        if (c - 1) >= 0:
            if board[r + 2][c - 1] == 1:
                return False
    return True

def successors_rook(board):
    succ_board = []
    # we are going to place rooks to the leftmost empty column
    # number of already placed rooks help us get the column number
    col = count_pieces(board)

    for row in range(0, N):
        # the input coordinates start from 1, not 0 hence r+1, c+1 to match the scale
        if [row+1,col+1] not in coordinates:
            if count_on_row(board, row) == 0:
                temp_board = add_piece(board, row, col)
                succ_board.append(temp_board)

    return succ_board

def successors_queen(board):
    succ_board = []

    # we are going to place queens to the leftmost empty column
    # number of already placed queens help us get the column number
    col = count_pieces(board)

    for row in range(0, N):
        # the input coordinates start from 1, not 0 hence r+1, c+1 to match the scale
        if [row+1,col+1] not in coordinates:
            if count_on_row(board, row) == 0:
                proceed = check_diagonals(board, row, col)
                if proceed:
                    temp_board = add_piece(board, row, col)
                    succ_board.append(temp_board)

    return succ_board

def successors_knight(board):
    succ_board = []

    for c in range(0, N):
        for r in range(0, N):
            # the input coordinates start from 1, not 0 hence r+1, c+1 to match the scale
            if [r+1,c+1] not in coordinates:
                if board[r][c] != 1:
                    proceed = check_attacking_nights(board, r, c)
                    if proceed:
                        temp_board = add_piece(board, r, c)
                        succ_board.append(temp_board)
    return succ_board

# check if board is a goal state
def is_goal(board):
    return count_pieces(board) == N and \
           all([count_on_row(board, r) <= 1 for r in range(0, N)]) and \
           all([count_on_col(board, c) <= 1 for c in range(0, N)])

def is_nknight_goal(board):
    return count_pieces(board) == N

# Solve n-rooks!
def solve(initial_board):
    fringe = [initial_board]

    while len(fringe) > 0:
        if type == "nrook":
            for s in successors_rook(fringe.pop()):
                if is_goal(s):
                    return (s)
                fringe.append(s)
        elif type == "nqueen":
            for s in successors_queen(fringe.pop()):
                if is_goal(s):
                    return (s)
                fringe.append(s)
        elif type == "nknight":
            for s in successors_knight(fringe.pop()):
                if is_nknight_goal(s):
                    return (s)
                fringe.append(s)
    return False

# This is N, the size of the board. It is passed through command line arguments.
num_arg = len(sys.argv)

if num_arg < 2:
    print("Please input type of piece: nrook/nqueen/nknight.")
else:
    type = sys.argv[1]
if num_arg < 3:
    print("Please input the board size.")
else:
    N = int(sys.argv[2])

# time_beg = time.time()

list_coordinates = []
if num_arg >= 4:
    num_coord = int(sys.argv[3])
    if num_coord > 0:
        for arg in sys.argv[4:]:
            # put all the coordinates in the list_coordinates list
            list_coordinates.append(int(arg))

        if len(list_coordinates) != 2*num_coord:
            print("Check the number of cordinates passed")

coordinates = []
# break the coordinates in the x,y format and store them into coordinates
coordinates = [list_coordinates[x:x+2] for x in range(0, len(list_coordinates) - 1, 2)]

# The board is stored as a list-of-lists. Each inner list is a row of the board.
# A zero in a given square indicates no piece, and a 1 indicates a piece.

initial_board = [[0] * N] * N

print("Starting from initial board:\n" + printable_board(initial_board) + "\n\nLooking for solution...\n")
solution = solve(initial_board)

# while using BFS enable the next line
# solution = solveBFS(initial_board)
print(printable_board(solution) if solution else "Sorry, no solution found. :(")
# time_end = time.time()
# time_elapsed = time_end - time_beg
# print("Time taken: ", time_elapsed)
