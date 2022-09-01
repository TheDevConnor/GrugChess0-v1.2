import pygame as pg

class Sound():

    def __init__(self, path) -> None:
        self.path = path
        self.sound = pg.mixer.Sound(self.path)

    def play(self):
        pg.mixer.Sound.play(self.sound)