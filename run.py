import pygame as pg
from game import Game

if __name__ == '__main__':
    pg.display.init()
    pg.font.init()
    Game().main_loop()
    