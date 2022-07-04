import pygame as pg

from objects import Text
from settings import GAME_RESOLUTION, Color, GAME_NAME
from .base import Scene, SceneManager


class GameOverScene(Scene):

    def __init__(self, sign: str):
        self.winner = sign
        pg.display.set_caption(GAME_NAME)
        super().__init__()

    # region Private

    # region Implementation Scene

    def _create_objects(self) -> None:
        victory_text = Text(f'Winner: {self.winner.upper()}', 90, color=Color.BLACK)
        victory_text.set_center_pos(center_cord=(GAME_RESOLUTION[0] // 2, GAME_RESOLUTION[1] // 2 - 50))

        space_text: Text = Text('Press space to continue', 70, color=Color.BLACK)
        space_text.set_center_pos(center_cord=(GAME_RESOLUTION[0] // 2, GAME_RESOLUTION[1] // 2 + 30))
        self._objects.append(victory_text, space_text)

    # endregion

    # endregion

    # region Public

    # region Implementation Scene

    def process_draw(self, screen: pg.Surface) -> None:
        SceneManager().last.process_draw(screen)
        SceneManager().last.additional_draw(screen)
        super().process_draw(screen)

    def additional_event(self, event: pg.event.Event) -> None:
        if event.type == pg.KEYDOWN and event.key in (pg.K_SPACE, pg.K_ESCAPE):
            from scenes import MainScene
            SceneManager().current = MainScene()

    # endregion

    # endregion
