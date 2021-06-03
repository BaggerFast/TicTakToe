import sys
import traceback
import pygame as pg
from main import Game


def main():
    pg.display.init()
    pg.font.init()
    pg.mixer.init()
    pg.display.set_caption("Tic tac toe")
    game: Game
    try:
        game = Game()
        game.start()
    except Exception:
        print(traceback.format_exc())
    sys.exit(0)


if __name__ == '__main__':
    main()
