import pygame as pg
import traceback
from datetime import datetime

from constans import DEBUG
from scenes import MainScene


def TitTacToe():
    pg.display.init()
    pg.font.init()
    try:
        MainScene().start()
    except Exception:
        print(traceback.format_exc())
        if not DEBUG:
            with open(f"exception-{datetime.now().strftime('%m-%d-%Y-%H-%M-%S')}.log", "w") as file:
                file.write(traceback.format_exc())


if __name__ == '__main__':
    TitTacToe()
