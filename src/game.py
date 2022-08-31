from typing import final
from const import *

import pygame as pg
from board import Board
from dragger import Dragger

class Game():
    
    def __init__(self):
        self.board = Board()
        self.dragger = Dragger()

    # Show Methouds
    def show_background(self, surface):
        # Loop the board
        for rown in range(ROWS):
            for coln in range(COLS):
                if (rown + coln) % 2 == 0:
                    color = ('papayawhip') # light squares
                else:
                    color = ('sandybrown') # dark squares

                rect = (coln * SQSIZE, rown * SQSIZE, SQSIZE, SQSIZE)
                pg.draw.rect(surface, color, rect)

    def show_pieces(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                # piece ?
                if self.board.square[row][col].has_piece():
                    piece = self.board.square[row][col].piece
                    
                    # All pieces except dragger are being blited
                    if piece != self.dragger.piece:
                        piece.set_texture(size=80)
                        img = pg.image.load(piece.texture)
                        img_center = col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2
                        piece.texture_rect = img.get_rect(center=img_center)
                        surface.blit(img, piece.texture_rect)

    def show_moves(self, surface):
        if self.dragger.dragging:
           piece = self.dragger.piece

           # Loop all valid moves
           for move in piece.moves:
            # Color
            color = 'lightcoral' if (move.final.row + move.final.col) % 2 == 0 else 'indianred'
            # Rect
            rect = (move.final.col * SQSIZE, move.final.row * SQSIZE, SQSIZE, SQSIZE)
            # Blit or Draw
            pg.draw.rect(surface, color, rect)

    def show_last_move(self, surface):

        if self.board.last_move:
            initial = self.board.last_move.initial
            final = self.board.last_move.final

            for pos in [initial, final]:
                # color
                color = 'lightblue' if (pos.row + pos.col) % 2 == 0 else 'steelblue'
                # rect
                rect = (pos.col * SQSIZE, pos.row * SQSIZE, SQSIZE, SQSIZE)
                # blit
                pg.draw.rect(surface, color, rect)
