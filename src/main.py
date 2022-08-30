import pygame as pg
import sys

from const import *
from game import Game

class Main():

    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption("GrugChess0")
        self.game = Game()

    def main_loop(self):

        # So I dont have to call self. everytime
        game = self.game
        screen = self.screen

        while True:
            game.show_background(screen)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    sys.exit()
            pg.display.update()

main = Main()
main.main_loop()