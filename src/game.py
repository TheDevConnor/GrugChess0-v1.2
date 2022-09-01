from const import *

import pygame as pg
from board import Board
from config import Config
from dragger import Dragger
from square import Square

class Game():
    
    def __init__(self):
        self.next_player = 'white'
        self.hovered_square = None
        self.board = Board()
        self.dragger = Dragger()
        self.config = Config()

    # Show Methouds
    def show_background(self, surface):
        theme = self.config.theme

        # Loop the board
        for rown in range(ROWS):
            for coln in range(COLS):
                # Color
                color = theme.bg.light if (rown + coln) % 2 == 0 else theme.bg.dark
                # Rect
                rect = (coln * SQSIZE, rown * SQSIZE, SQSIZE, SQSIZE)
                # Blit or Draw
                pg.draw.rect(surface, color, rect)

                # Row Cordinates
                if coln == 0:
                    # color
                    color = theme.bg.dark if (rown + coln) % 2 == 0 else theme.bg.light
                    # label
                    label = self.config.font.render(str(ROWS - rown), 1, color)
                    lbl_pos = (5, 5 + rown * SQSIZE)
                    # blit
                    surface.blit(label, lbl_pos)
                
                # Column Cordinates
                if rown == 7:
                    # color
                    color = theme.bg.dark if (rown + coln) % 2 == 0 else theme.bg.light
                    # label
                    label = self.config.font.render(Square.get_alphacol(coln), 1, color)
                    lbl_pos = (coln * SQSIZE + SQSIZE - 20, SCREEN_HEIGHT - 20)
                    # blit
                    surface.blit(label, lbl_pos)

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
        theme = self.config.theme

        if self.dragger.dragging:
           piece = self.dragger.piece

           # Loop all valid moves
           for move in piece.moves:
            # Color
            color = theme.moves.light if (move.final.row + move.final.col) % 2 == 0 else theme.moves.dark
            # Rect
            rect = (move.final.col * SQSIZE, move.final.row * SQSIZE, SQSIZE, SQSIZE)
            # Blit or Draw
            pg.draw.rect(surface, color, rect)

    def show_last_move(self, surface):
        theme = self.config.theme

        if self.board.last_move:
            initial = self.board.last_move.initial
            final = self.board.last_move.final

            for pos in [initial, final]:
                # color
                color = theme.trace.light if (pos.row + pos.col) % 2 == 0 else theme.trace.dark
                # rect
                rect = (pos.col * SQSIZE, pos.row * SQSIZE, SQSIZE, SQSIZE)
                # blit
                pg.draw.rect(surface, color, rect)

    def show_hover(self, surface):
        if self.hovered_square:
            # color
            color = (180, 180, 180)
            # rect
            rect = (self.hovered_square.col * SQSIZE, self.hovered_square.row * SQSIZE, SQSIZE, SQSIZE)
            # blit
            pg.draw.rect(surface, color, rect, 3)

    # Other Functions
    def next_turn(self):
        self.next_player = 'white' if self.next_player == 'black' else 'black'

    def set_hover(self, row, col):
        self.hovered_square = self.board.square[row][col]

    def change_theme(self):
        self.config.change_theme()

    def sound_effect(self, captured = False):
        if captured:
            self.config.capture_sound.play()
        else:
            self.config.move_sound.play()