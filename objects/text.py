import pygame as pg

from misc.constans import Color


class Text:
    def __init__(self, text, size, rect=(0, 0), color=Color.white, font="Arial"):
        self.pos = rect
        self.font = pg.font.SysFont(font, size, True)
        self.surface = self.font.render(text, False, color)

    def update_position(self, rect=()):
        self.pos = rect

    def update_center_position(self, center_cord):
        self.pos = self.surface.get_rect(center=center_cord)

    def draw(self, screen):
        screen.blit(self.surface, self.pos)
