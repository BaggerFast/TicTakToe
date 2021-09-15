import sys
import pygame as pg


class Base:
    def __init__(self, game, header_name: str):
        pg.display.set_caption(header_name)
        self.game = game
        self.fps: int = 60
        self.scene_active: bool = True
        self.time: pg.time = pg.time.Clock()

    def start(self) -> None:
        while self.scene_active:
            for event in pg.event.get():
                self.event_check(event)
            self.draw_to_screen()
            pg.display.update()
            self.time.tick(self.fps)
        self.finish()

    @staticmethod
    def event_check(event: pg.event) -> None:
        if event.type == pg.QUIT:
            sys.exit(0)

    def finish(self) -> None:
        pass

    def draw_to_screen(self) -> None:
        raise NotImplementedError

