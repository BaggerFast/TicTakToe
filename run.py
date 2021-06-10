import sys

import pygame as pg

from main import Game


def main():
    pg.display.init()
    pg.font.init()
    pg.mixer.init()
    pg.display.set_caption("Tic tac toe")
    try:
        Game().start()
    except Exception:
        print(Exception)
    sys.exit(0)


if __name__ == '__main__':
    main()
