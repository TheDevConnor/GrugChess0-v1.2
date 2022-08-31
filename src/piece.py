import math as m
import os

class Piece():

    def __init__(self, color, value, name, texture=None, texture_rect=None):
        self.name = name
        self.color = color

        self.moves = []
        self.moved = False

        value_sign = 1 if self.color == 'white' else -1
        self.value = value * value_sign

        self.texture = texture
        self.set_texture()
        self.texture_rect = texture_rect

    def set_texture(self, size = 80):
        self.texture = os.path.join(
            f'src\images\pieces\imgs-{size}px\{self.color}_{self.name}.png')

    def add_moves(self, move):
        self.moves.append(move)

    def clear_moves(self):
        self.moves = []

class Pawn(Piece):
    def __init__(self, color):
        # The direction of the piece
        self.dir = -1 if color == 'white' else 1

        # super is calling the Piece constructor and calling the
        # __init__ method of the Piece class
        super().__init__(color, 1.0, 'pawn')

class Knight(Piece):
    def __init__(self, color):
        # super is calling the Piece constructor and calling the
        # __init__ method of the Piece class
        super().__init__(color, 3.0, 'knight')

class Bishop(Piece):
    def __init__(self, color):
        # super is calling the Piece constructor and calling the
        # __init__ method of the Piece class
        super().__init__(color, 3.0, 'bishop')

class Rook(Piece):
    def __init__(self, color):
        # super is calling the Piece constructor and calling the
        # __init__ method of the Piece class
        super().__init__(color, 5.0, 'rook')

class Queen(Piece):
    def __init__(self, color):
        # super is calling the Piece constructor and calling the
        # __init__ method of the Piece class
        super().__init__(color, 9.0, 'queen')

class King(Piece):
    def __init__(self, color):
        # super is calling the Piece constructor and calling the
        # __init__ method of the Piece class
        super().__init__(color, m.inf, 'king')