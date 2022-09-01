from sound import Sound
from theme import Theme

import pygame as pg
import os

class Config():

    def __init__(self):
        self.themes = []
        self._add_theme()
        self.index = 0
        self.theme = self.themes[self.index]

        self.move_sound = Sound(os.path.join('src/audio/PieceMoved.mp3'))
        self.capture_sound = Sound(os.path.join('src/audio/PieceCaptured.wav'))
        self.check_sound = Sound(os.path.join('src/audio/InCheck.mp3'))

    def change_theme(self):
        self.index += 1
        self.index %= len(self.themes)
        self.theme = self.themes[self.index]

    def _add_theme(self):
        default = Theme(('papayawhip'), ('sandybrown'), ('lightsteelblue'), ('slategray'), ('lightcoral'), ('indianred'))
        light = Theme(('azure'), ('turquoise'), ('lightsteelblue'), ('slategray'), ('lightcoral'), ('indianred'))
        dark = Theme((120, 119, 118), (86, 85, 84), (99, 126, 143), (82, 102, 128), ('lightcoral'), ('indianred'))
        green = Theme((234, 235, 200), (119, 154, 88), (244, 247, 116), (172, 195, 51), '#C86464', '#C84646')

        self.themes = [dark, light, green, default]