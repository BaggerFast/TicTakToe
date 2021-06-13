import pygame as pg

from scenes import MainScene


def main():
    pg.display.init()
    pg.font.init()
    pg.mixer.init()
    MainScene().start()


if __name__ == '__main__':
    main()
