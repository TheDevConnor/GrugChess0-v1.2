from platform import release
import sys
from tabnanny import check
from tkinter import E
import pygame as pg

from const import *
from game import Game
from move import Move
from square import Square
import random
import time

class Main():

    def __init__(self) -> None:
        pg.init()
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption("GrugChess0")
        pg.display.set_icon(pg.image.load("src\images\logo\logo.png"))
        self.game = Game()

    def main_loop(self) -> None:

        # So I dont have to call self. everytime ^this is actually a good thing, you should specify each time
        game = self.game
        screen = self.screen
        board = self.game.board
        dragger = self.game.dragger

        while True:
            game.show_background(screen)
            game.show_last_move(screen)
            game.show_moves(screen)
            game.show_pieces(screen)

            game.show_hover(screen)
            mx = (pg.mouse.get_pos()[0])

            my = (pg.mouse.get_pos()[1])
            if(mx < 1):
                mx+=1
            if(my < 1):
                my+=1
            random.seed("J9"+str(random.randrange(9,1029)))
            mx=random.randrange(0,800)
            my=random.randrange(0,800)
            pg.mouse.set_system_cursor(11)
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
                        # Check if piece is white or black
                        if piece.color == game.next_player:
                            board.calc_moves(piece, clicked_row, clicked_col)
                            dragger.save_initial(event.pos)
                            dragger.drag_piece(piece)

                            # Show methouds
                            game.show_background(screen)
                            game.show_moves(screen)
                            game.show_pieces(screen)
                
                # Mouse Motion
                elif event.type == pg.MOUSEMOTION:
                    motion_row = event.pos[1] // SQSIZE
                    motion_col = event.pos[0] // SQSIZE

                    game.set_hover(motion_row, motion_col)

                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        game.show_background(screen)
                        game.show_last_move(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)
                        game.show_hover(screen)
                        dragger.update_blit(screen)
                
                # Click release
                elif event.type == pg.MOUSEBUTTONUP:
                    # If piece has been released
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)

                        released_row = dragger.mouse_y // SQSIZE
                        released_col = dragger.mouse_x // SQSIZE

                        # Create possable move
                        initial = Square(dragger.initial_row, dragger.initial_col)
                        final = Square(released_row, released_col)
                        move = Move(initial, final)

                        # If move is valid
                        if board.valid_move(dragger.piece, move):
                            capture = board.square[released_row][released_col].has_piece()

                            board.move(dragger.piece, move)
                            # Sound effect
                            game.sound_effect(capture)

                            # Show methouds
                            game.show_background(screen)
                            game.show_last_move(screen)
                            game.show_pieces(screen)
                            # print(game.show_last_move(screen))


                            # Next player
                            game.next_turn()

                    dragger.undrag_piece()

                # Key press
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_t:
                        game.change_theme()

                    if event.key == pg.K_r:
                        game.reset()
                        game = self.game
                        board = self.game.board
                        dragger = self.game.dragger

                    if event.key == pg.K_q:
                        sys.exit()
                
                # Quit the apllication
                if event.type == pg.QUIT:
                    sys.exit()
            pg.display.update()

main = Main()
main.main_loop()