from ast import Break
from square import Square
from move import Move
import copy as cp

from piece import *
from const import *

class Board():
    def __init__(self) -> None:
        # Createing a 2 dimensional array of square
        self.square = [[0,0,0,0,0,0,0,0] for col in range(COLS)]

        self.last_move = None

        # Create the square
        self._create_square()
        # Add the pieces
        self._add_pieces('white')
        self._add_pieces('black')

    def move(self, piece, move):
        initial = move.initial
        final = move.final

        # console bord move update
        self.square[initial.row][initial.col].piece = None
        self.square[final.row][final.col].piece = piece

        # Pawn Promotion
        if isinstance(piece, Pawn):
            self.check_promotion(piece, final)

        # KingSide Castling
        if isinstance(piece, King):
            if self.castling(initial, final):
                diff = final.col - initial.col
                rook = piece.left_rook if diff < 0 else piece.right_rook
                self.move(rook, rook.moves[-1])

        # move
        piece.moved = True
        print(self.square[final.row][final.col].piece)

        #clear the valid moves
        piece.clear_moves()

        # Set the last move
        self.last_move = move

    def valid_move(self, piece, move):
        return move in piece.moves

    def check_promotion(self, piece, final):
        if final.row == 0 or final.row == 7:
            self.square[final.row][final.col].piece = Queen(piece.color)

    def castling(self, initial, final):
        return abs(initial.col - final.col) == 2

    def in_check(self, piece, move):
        # Create a copy of the board and the pieces
        # To calculate checks
        temp_piece = cp.deepcopy(piece)
        temp_board = cp.deepcopy(self)
        temp_board.move(temp_piece, move)

        for row in range(ROWS):
            for col in range(COLS):
                # Check if the square has a rival piece
                if temp_board.square[row][col].has_rival_piece(piece.color):
                    p = temp_board.square[row][col].piece
                    # Calculate the possible moves of the rival piece
                    temp_board.calc_moves(p, row, col, bool=False)
                    # Then we loop each move for the rival piece
                    for m in p.moves:
                        # Seeing if the final piece is a king if so then check is
                        # Equal to true
                        if isinstance(m.final.piece, King):
                            return True
        return False

    def calc_moves(self, piece, row, col, bool=True):
        # Calculate the valid moves for the piece

        def pawn_moves():
            # Pawns can move forward 1 or 2 square
            steps = 1 if piece.moved else 2 

            # Vertical moves
            start = row + piece.dir
            end  = row + (piece.dir * (1 + steps))

            # Loop through the vertical moves
            for p_move_row in range(start, end, piece.dir):
                if Square.in_range(p_move_row):
                    if self.square[p_move_row][col].is_empty():
                        # create initial and final move square
                        initial = Square(row, col)
                        final = Square(p_move_row, col)
                        # create a new move
                        move = Move(initial, final)

                        # Check for potional checks
                        if bool:
                            if not self.in_check(piece, move):
                                # add the move to the piece's moves
                                piece.add_moves(move)
                        else:
                            piece.add_moves(move)
                    # blocked
                    else: break
                # not in range
                else: break

            # Diagonal captures
            p_move_row = row + piece.dir
            p_move_cols = [col-1, col+1]
            for p_move_col in p_move_cols:
                if Square.in_range(p_move_row, p_move_col):
                    if self.square[p_move_row][p_move_col].has_rival_piece(piece.color):
                        # create initial and final move square
                        initial = Square(row, col)
                        final_piece = self.square[p_move_row][p_move_col].piece
                        final = Square(p_move_row, p_move_col, final_piece)
                        # create a new move
                        move = Move(initial, final)
                        # Check for potional checks
                        if bool:
                            if not self.in_check(piece, move):
                                # add the move to the piece's moves
                                piece.add_moves(move)
                        else:
                            piece.add_moves(move)

        def knight_moves():
            # Knight moves
            possable_moves = [
                (row-2, col+1),
                (row-1, col+2),
                (row+1, col+2),
                (row+2, col+1),
                (row+2, col-1),
                (row+1, col-2),
                (row-1, col-2),
                (row-2, col-1),]
            
            for move in possable_moves:
                p_move_row, p_move_col = move
                if Square.in_range(p_move_row, p_move_col):
                    if self.square[p_move_row][p_move_col].isempty_or_isrival(piece.color):
                        # Create square of the new move
                        initial = Square(row, col)
                        final_piece = self.square[p_move_row][p_move_col].piece
                        final = Square(p_move_row, p_move_col, final_piece)

                        # Create the new move
                        move = Move(initial, final)

                        # Check for potional checks
                        if bool:
                            if not self.in_check(piece, move):
                                # add the move to the piece's moves
                                piece.add_moves(move)
                            else: break
                        else:
                            # Append new valid move
                            piece.add_moves(move)

        def straight_line_moves(incrs):
            for incr in incrs:
                row_incr, col_incr = incr
                p_move_row = row + row_incr
                p_move_col = col + col_incr

                while True:
                    if Square.in_range(p_move_row, p_move_col):
                        # Create square of the possably new move
                        initial = Square(row, col)
                        final_piece = self.square[p_move_row][p_move_col].piece
                        final = Square(p_move_row, p_move_col, final_piece)
                        # Create a possible move
                        move = Move(initial, final)

                        # Empty
                        if self.square[p_move_row][p_move_col].is_empty():
                            # Check for potional checks
                            if bool:
                                if not self.in_check(piece, move):
                                    # add the move to the piece's moves
                                    piece.add_moves(move)
                            else:
                                piece.add_moves(move)

                        # Has freindly piece
                        elif self.square[p_move_row][p_move_col].has_team_piece(piece.color):
                            break

                        # Has rival piece
                        elif self.square[p_move_row][p_move_col].has_rival_piece(piece.color):
                            # Check for potional checks
                            if bool:
                                if not self.in_check(piece, move):
                                    # add the move to the piece's moves
                                    piece.add_moves(move)
                            else:
                                piece.add_moves(move)
                            break


                    # Blocked
                    else: break

                    # Incrementing the increments
                    p_move_row = p_move_row + row_incr
                    p_move_col = p_move_col + col_incr

        def king_moves():
            # King moves
            possable_moves = [
                (row-1, col+0),
                (row-1, col+1),
                (row+0, col+1),
                (row+1, col+1),
                (row+1, col+0),
                (row+1, col-1),
                (row+0, col-1),
                (row-1, col-1),]
            
            # Normal Moves
            for move in possable_moves:
                p_move_row, p_move_col = move
                if Square.in_range(p_move_row, p_move_col):
                    if self.square[p_move_row][p_move_col].isempty_or_isrival(piece.color):
                        # Create square of the new move
                        initial = Square(row, col)
                        final = Square(p_move_row, p_move_col)

                        # Create the new move
                        move = Move(initial, final)
                        # Check for potional checks
                        if bool:
                            if not self.in_check(piece, move):
                                # add the move to the piece's moves
                                piece.add_moves(move)
                            else: break
                        else:
                            piece.add_moves(move)

            # Castling
            if not piece.moved:
                # Queen Side Castling
                left_rook = self.square[row][0].piece
                if isinstance(left_rook, Rook):
                    if not left_rook.moved:
                        for c in range(1, 4):
                            # Casting is not possable because the squares are not empty
                            if self.square[row][c].has_piece():
                                break

                            if c == 3:
                                # Rook Moves
                                # Adds left rock to the king
                                piece.left_rook = left_rook
                                # Create square of the new move
                                initial = Square(row, 0)
                                final = Square(row, 3)
                                # Create the new move
                                move = Move(initial, final)
                                # Append new valid move
                                left_rook.add_moves(move)

                                # King Moves
                                # Create square of the new move
                                initial = Square(row, col)
                                final = Square(row, 2)
                                # Create the new move
                                move = Move(initial, final)
                                # Append new valid move
                                piece.add_moves(move)
                                # # Rook Moves
                                # # Adds left rock to the king
                                # piece.left_rook = left_rook
                                # # Create square of the new move
                                # initial = Square(row, 0)
                                # final = Square(row, 3)
                                # # Create the new move
                                # move_r = Move(initial, final)

                                # # King Moves
                                # # Create square of the new move
                                # initial = Square(row, col)
                                # final = Square(row, 2)
                                # # Create the new move
                                # move_k = Move(initial, final)

                                # # Check for potional checks
                                # if bool:
                                #     if not self.in_check(piece, move_k) and not self.in_check(left_rook, move_r):
                                #         # add the move to the rook
                                #         left_rook.add_moves(move_r)
                                #         # add the move to the king
                                #         piece.add_moves(move_k)
                                # else:
                                #     # add the move to the rook
                                #     left_rook.add_moves(move_r)
                                #     # add the move to the king
                                #     piece.add_moves(move_k)

                # King Side Castling
                right_rook = self.square[row][7].piece  
                if isinstance(right_rook, Rook):
                    if not right_rook.moved:
                        for c in range(5, 7):
                            # Casting is not possable because the squares are not empty
                            if self.square[row][c].has_piece():
                                break

                            if c == 6:
                                # Adds left rock to the king
                                piece.right_rook = right_rook
                                # Create square of the new move
                                initial = Square(row, 7)
                                final = Square(row, 5)
                                # Create the new move
                                move = Move(initial, final)
                                # Append new valid move
                                right_rook.add_moves(move)

                                # King Moves
                                # Create square of the new move
                                initial = Square(row, col)
                                final = Square(row, 6)
                                # Create the new move
                                move = Move(initial, final)
                                # Append new valid move
                                piece.add_moves(move)
                                # # Rook Moves
                                # # Adds left rock to the king
                                # piece.right_rook = right_rook
                                # # Create square of the new move
                                # initial = Square(row, 7)
                                # final = Square(row, 5)
                                # # Create the new move
                                # move_r = Move(initial, final)

                                # # King Moves
                                # # Create square of the new move
                                # initial = Square(row, col)
                                # final = Square(row, 6)
                                # # Create the new move
                                # move_k = Move(initial, final)

                                # # Check for potional checks
                                # if bool:
                                #     if not self.in_check(piece, move_k) and not self.in_check(right_rook, move_r):
                                #         # add the move to the rook
                                #         right_rook.add_moves(move_r)
                                #         # add the move to the king
                                #         piece.add_moves(move_k)
                                # else:
                                #     # add the move to the rook
                                #     right_rook.add_moves(move_r)
                                #     # add the move to the king
                                #     piece.add_moves(move_k)
                                                                # Rook Moves

        if isinstance(piece, Pawn): pawn_moves()
        if isinstance(piece, Knight): knight_moves()
        if isinstance(piece, Bishop): 
            straight_line_moves([
                (-1,1), # up-right
                (-1,-1), # up-left
                (1,1), # down-right
                (1,-1),  # down-left
            ])
        if isinstance(piece, Rook): 
            straight_line_moves([
                (-1,0), # up
                (0,1), # right
                (1,0), # down
                (0,-1),  # left
            ])
        if isinstance(piece, Queen): 
            straight_line_moves([
                (-1,1), # up-right
                (-1,-1), # up-left
                (1,1), # down-right
                (1,-1), # down-left
                (-1,0), # up
                (0,1), # right
                (1,0), # down
                (0,-1),  # left
            ])
        if isinstance(piece, King): king_moves()

        
    def _create_square(self) -> None:
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