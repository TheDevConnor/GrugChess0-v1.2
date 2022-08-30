from const import *
import pygame as pg

class Game():
    
    def __init__(self):
        pass

    # Show Methouds
    def show_background(self, surface):
        for rown in range(ROWS):
            for coln in range(COLS):
                if (rown + coln) % 2 == 0:
                    color = (234, 235, 200) # light green
                else:
                    color = (119, 154, 88) # dark green

                rect = (coln * SQSIZE, rown * SQSIZE, SQSIZE, SQSIZE)
                pg.draw.rect(surface, color, rect)