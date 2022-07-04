import os
from abc import ABC
from typing import Final
import pygame as pg

FPS: Final = 15

CELL_COUNT: Final = 3
CELL_SIZE: Final = 250
GRID_THICKNESS: Final = 15

GAME_NAME: Final = 'TicTakToe'
GAME_RESOLUTION: Final = (CELL_SIZE * CELL_COUNT + GRID_THICKNESS * (CELL_COUNT + 1),
                          CELL_SIZE * CELL_COUNT + GRID_THICKNESS * (CELL_COUNT + 1))


class PathCtrl(ABC):
    BASE: Final = os.path.dirname(os.path.abspath(__file__))

    @classmethod
    def get_path(cls, path: str) -> str:
        return os.path.join(cls.BASE, path)


class Color:
    WHITE: Final = pg.Color('white')
    BLACK: Final = pg.Color('black')
    GREEN: Final = (20, 189, 172)
    RED: Final = (255, 36, 0)
    GRAY: Final = (50, 50, 50)
    YELLOW: Final = (255, 186, 0)
    BROWN: Final = (84, 84, 84)
    WHEAT: Final = (242, 235, 211)
    DARK_GREEN: Final = (13, 161, 146)
