import traceback
from datetime import datetime

import pygame as pg

from scenes import MainScene


def TitTacToe():
    pg.display.init()
    pg.font.init()
    pg.mixer.init()
    try:
        MainScene().start()
    except Exception:
        print(traceback.format_exc())
        with open(f"exception-{datetime.now().strftime('%m-%d-%Y-%H-%M-%S')}.log", "w") as file:
            file.write(traceback.format_exc())


if __name__ == '__main__':
    TitTacToe()
