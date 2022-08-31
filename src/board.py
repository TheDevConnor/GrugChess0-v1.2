from urllib.parse import ParseResultBytes
from square import Square
from move import Move

from piece import *
from const import *

class Board():
    def __init__(self) -> None:
        # Createing a 2 dimensional array of squares
        self.square = [[0,0,0,0,0,0,0,0] for col in range(COLS)]

        # Create the squares
        self._create_squares()
        # Add the pieces
        self._add_pieces('white')
        self._add_pieces('black')

    def calc_moves(self, piece, row, col):
        # Calculate the valid moves for the piece

        def knight_moves():
            # Knight moves
            moves = [
                (row-2, col+1),
                (row-1, col+2),
                (row+1, col+2),
                (row+2, col+1),
                (row+2, col-1),
                (row+1, col-2),
                (row-1, col-2),
                (row-2, col-1),]
            
            for move in moves:
                move_row, move_col = move
                if Square.in_range(move_row, move_col):
                    if self.square[move_row][move_col].isempty_or_isrival(piece.color):
                        # Create squares of the new move
                        initial = Square(row, col)
                        final = Square(move_row, move_col)

                        # Create the new move
                        move = Move(initial, final)
                        # Append new valid move 
                        piece.add_moves(move)

        if isinstance(piece, Pawn):
            pass

        elif isinstance(piece, Knight):
            knight_moves()

        elif isinstance(piece, Bishop):
            pass

        elif isinstance(piece, Rook):
            pass

        elif isinstance(piece, Queen):
            pass
        
        elif isinstance(piece, King):
            pass

    def _create_squares(self) -> None:
        # We are now looping through the array
        for row in range(ROWS):
            for col in range(COLS):
                # Replacing the 0 with a square object
                self.square[row][col] = Square(row, col)

    def _add_pieces(self, color):
        for col in range(COLS):
            row_pawn, row_other = (6, 7) if color == 'white' else (1, 0)
            
            # Pawns
            for col in range(COLS):
                self.square[row_pawn][col] = Square(row_pawn, col, Pawn(color))

            # Knights
            self.square[row_other][1] = Square(row_other, 1, Knight(color))
            self.square[row_other][6] = Square(row_other, 6, Knight(color))

            # Bishops
            self.square[row_other][2] = Square(row_other, 2, Bishop(color))
            self.square[row_other][5] = Square(row_other, 5, Bishop(color))

            # Rooks
            self.square[row_other][0] = Square(row_other, 0, Rook(color))
            self.square[row_other][7] = Square(row_other, 7, Rook(color))

            # Queen
            self.square[row_other][3] = Square(row_other, 3, Queen(color))

            # King
            self.square[row_other][4] = Square(row_other, 4, King(color))