import sys
import pygame as pg
from scenes import MainScene, SceneManager
from settings import Color, FPS, GAME_RESOLUTION


class Game:

    # region Pygame setup

    pg.display.init()
    pg.font.init()
    pg.display.set_icon(pg.transform.scale(pg.image.load('assets/logo.png'), (90, 90)))

    # endregion

    def __init__(self):
        self.screen = pg.display.set_mode(GAME_RESOLUTION)
        SceneManager().current = MainScene()
        self.__clock = pg.time.Clock()

    # region Private

    def __process_all_draw(self) -> None:
        self.screen.fill(Color.DARK_GREEN)
        SceneManager().current.process_draw(self.screen)
        SceneManager().current.additional_draw(self.screen)
        pg.display.flip()

    @staticmethod
    def __process_all_events() -> None:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit(0)
            SceneManager().current.process_event(event)
            SceneManager().current.additional_event(event)

    @staticmethod
    def __process_all_logic() -> None:
        SceneManager().current.process_logic()
        SceneManager().current.additional_logic()

    # endregion

    # region Public

    def main_loop(self) -> None:
        while True:
            self.__process_all_logic()
            self.__process_all_events()
            self.__process_all_draw()
            self.__clock.tick(FPS)

    # endregion
