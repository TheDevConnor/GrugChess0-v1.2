import pygame as pg
from const import *

class Dragger():

    def __init__(self) -> None:
        self.piece = None
        self.dragging = False

        self.mouse_x = 0
        self.mouse_y = 0

        self.initial_row = 0
        self.initial_col = 0

    # Blit methoud
    def update_blit(self, surface) -> None:
        self.piece.set_texture(size=128)
        texture = self.piece.texture
        # Img
        img = pg.image.load(texture)
        #rect
        img_center = (self.mouse_x , self.mouse_y)
        self.piece.texture_rect = img.get_rect(center=img_center)
        # Update blit 
        surface.blit(img, self.piece.texture_rect)

    # Other methouds
    def update_mouse(self, pos) -> None:
        self.mouse_x = pos[0]
        self.mouse_y = pos[1]

    def save_initial(self, pos) -> None:
        self.initial_row = pos[1] // SQSIZE
        self.initial_col = pos[0] // SQSIZE

    def drag_piece(self, piece) -> None:
        self.piece = piece
        self.dragging = True

    def undrag_piece(self) -> None:
        self.piece = None
        self.dragging = False