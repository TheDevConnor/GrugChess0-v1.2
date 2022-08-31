import sys
import pygame as pg

from const import *
from game import Game

class Main():

    def __init__(self) -> None:
        pg.init()
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption("GrugChess0")
        pg.display.set_icon(pg.image.load("src\images\logo\logo.png"))
        self.game = Game()

    def main_loop(self) -> None:

        # So I dont have to call self. everytime
        game = self.game
        screen = self.screen
        board = self.game.board
        dragger = self.game.dragger

        while True:
            game.show_background(screen)
            game.show_moves(screen)
            game.show_pieces(screen)

            if dragger.dragging:
                dragger.update_blit(screen)

            for event in pg.event.get():
                # Mouse Click
                if event.type == pg.MOUSEBUTTONDOWN:
                    dragger.update_mouse(event.pos)
                    
                    clicked_row = dragger.mouse_y // SQSIZE
                    clicked_col = dragger.mouse_x // SQSIZE

                    # If piece has been clicked
                    if board.square[clicked_row][clicked_col].has_piece():
                        piece = board.square[clicked_row][clicked_col].piece
                        board.calc_moves(piece, clicked_row, clicked_col)
                        dragger.save_initial(event.pos)
                        dragger.drag_piece(piece)

                        # Show methouds
                        game.show_background(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)
                
                # Mouse Motion
                elif event.type == pg.MOUSEMOTION:
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        game.show_background(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)
                        dragger.update_blit(screen)
                
                # Click release
                elif event.type == pg.MOUSEBUTTONUP:
                    dragger.undrag_piece()
                
                # Quit the apllication
                if event.type == pg.QUIT:
                    sys.exit()
            pg.display.update()

main = Main()
main.main_loop()