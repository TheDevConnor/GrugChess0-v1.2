import numba
class Square():

    ALPHACOLS = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H'}

    def __init__(self, row, col, piece=None):
        self.row = row
        self.col = col
        self.piece = piece
        self.ALPHACOLS = self.ALPHACOLS[col]

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col

    def has_piece(self):
        return self.piece != None

    def is_empty(self):
        # If you write this line of code on 17 like this:
        # return not self.piece == None()
        # The code will not run properly.
        # The reason is because you are not calling the correct method.
        return not self.has_piece()

    def has_team_piece(self, color):
        return self.has_piece() and self.piece.color == color

    def has_rival_piece(self, color):
        return self.has_piece() and self.piece.color != color

    def isempty_or_isrival(self, color):
        return self.is_empty() or self.has_rival_piece(color)

    @staticmethod
    @numba.jit
    def in_range(*args):
        for arg in args:
            if arg < 0 or arg > 7:
                return False
        return True

    @staticmethod
    @numba.jit
    def get_alphacol(col):
        ALPHACOLS = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H'}
        return ALPHACOLS[col]