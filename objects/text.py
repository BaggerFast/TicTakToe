import pygame as pg

from misc import IDrawable
from settings import Color


class Text(IDrawable):

    def __init__(self, text: str, size: int, rect=(0, 0), color=Color.WHITE, font: str = "Arial"):
        self.__pos = rect
        self.__font = pg.font.SysFont(font, size, True)
        self.__surface: pg.Surface = self.__font.render(text, False, color)

    # region Public

    # region Implementation of IDrawable

    def process_draw(self, screen: pg.Surface):
        screen.blit(self.__surface, self.__pos)

    # endregion

    def set_center_pos(self, center_cord):
        self.__pos = self.__surface.get_rect(center=center_cord)

    # endregion
