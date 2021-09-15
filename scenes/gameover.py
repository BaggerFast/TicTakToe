from objects import Text
from scenes.base import Base
import pygame as pg


class GameOverScene(Base):
    def __init__(self, game, main_scene):
        super().__init__(game, 'Game Over')
        self.main_scene = main_scene
        self.texts: list[Text] = self.get_texts()

    def get_texts(self) -> list[Text]:
        victory_text: Text = Text(f'Winner: {self.main_scene.winner}' if self.main_scene.winner else 'Draw', 70)
        victory_text.update_center_position(center_cord=(self.main_scene.resolution[0] // 2,
                                                         self.main_scene.resolution[1] // 2 - 20))

        space_text: Text = Text('Press space to continue', 40)
        space_text.update_center_position(center_cord=(self.main_scene.resolution[0] // 2,
                                                       self.main_scene.resolution[1] // 2 + 30))
        return [victory_text, space_text]

    def event_check(self, event: pg.event) -> None:
        super().event_check(event)
        if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
            self.game.Scenes.main(self.game, cell_count=self.main_scene.cell_count).start()

    def draw_to_screen(self) -> None:
        for text in self.texts:
            text.draw(screen=self.main_scene.screen)