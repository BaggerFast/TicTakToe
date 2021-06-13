import sys

import pygame as pg

from constans import Sign, Color
from text import Text


class BaseScene:
    def __init__(self, header_name):
        pg.display.set_caption(header_name)
        self.fps = 60
        self.scene_active: bool = True
        self.time = pg.time.Clock()

    def start(self) -> None:
        while self.scene_active:
            for event in pg.event.get():
                self.event_check(event)
            self.draw_to_screen()
            pg.display.update()
            self.time.tick(self.fps)
        self.finish()

    @staticmethod
    def event_check(event) -> None:
        if event.type == pg.QUIT:
            sys.exit(0)

    def finish(self) -> None:
        pass

    def draw_to_screen(self) -> None:
        raise NotImplementedError


class MainScene(BaseScene):
    def __init__(self, cell_count=3):
        super().__init__('Tic Tac Toe')
        # graphics
        self.size_block: int = 150
        self.retreat: int = 2
        self.cell_count: int = cell_count
        self.resolution: tuple = tuple([self.size_block * self.cell_count + self.retreat * (self.cell_count + 1)] * 2)
        self.screen = pg.display.set_mode(self.resolution)

        # logic
        self.move: int = 1
        self.winner: str = ''
        self.pole: list[list[str]] = [[Sign.empty] * self.cell_count for _ in range(self.cell_count)]

    def finish(self) -> None:
        GameOverScene(self).start()

    def event_check(self, event) -> None:
        super().event_check(event)
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            self.click_event()

    def click_event(self) -> None:
        cursor_pos = pg.mouse.get_pos()
        for row in range(self.cell_count):
            row_cord = self.get_cord_for_rect(row)
            for col in range(self.cell_count):
                col_cord = self.get_cord_for_rect(col)
                if self.pole[row][col] == Sign.empty and self.collision_with_rect(cursor_pos,
                                                                                  self.get_rect(row_cord, col_cord)):
                    sign = Sign.x if self.move % 2 else Sign.o
                    self.pole[row][col] = sign
                    if self.check_win_status(sign):
                        self.winner = sign
                        self.scene_active = False
                    elif self.move == self.cell_count ** 2:
                        self.scene_active = False
                    self.move += 1

    def check_win_status(self, move) -> bool:
        for i in range(self.cell_count):
            lines = [[self.pole[j][i] for j in range(self.cell_count)], self.pole[i]]
            for line in lines:
                if line.count(move) == self.cell_count:
                    return True

        diagonals = [[self.pole[i][i] for i in range(self.cell_count)],
                     [self.pole[x][abs(self.cell_count - x - 1)] for x in range(self.cell_count)]]

        for line in diagonals:
            if line.count(move) == self.cell_count:
                return True
        return False

    def draw_to_screen(self) -> None:
        context = {
            Sign.x: self.draw_cross,
            Sign.o: self.draw_circle
        }
        self.screen.fill(Color.white)
        for row in range(self.cell_count):
            row_cord = self.get_cord_for_rect(row)
            for col in range(self.cell_count):
                rect = self.get_rect(row_cord, self.get_cord_for_rect(col))
                pg.draw.rect(self.screen, Color.black, rect)
                if self.pole[row][col] in context:
                    context[self.pole[row][col]](rect=rect)

    def draw_cross(self, rect: pg.Rect) -> None:
        pg.draw.line(self.screen, Color.red, rect.topright, rect.bottomleft, 5)
        pg.draw.line(self.screen, Color.red, rect.topleft, rect.bottomright, 5)

    def draw_circle(self, rect: pg.Rect) -> None:
        pg.draw.circle(self.screen, Color.green, rect.center, self.size_block // 2, 5)

    @staticmethod
    def collision_with_rect(cursor_pos, rect=pg.Rect) -> bool:
        cord_x, cord_y = cursor_pos
        return rect.left <= cord_x <= rect.right and rect.top <= cord_y <= rect.bottom

    def get_cord_for_rect(self, i) -> int:
        return self.size_block * i + (i + 1) * self.retreat

    def get_rect(self, row_cord, col_cord) -> pg.Rect:
        return pg.Rect(row_cord, col_cord, self.size_block, self.size_block)


class GameOverScene(BaseScene):
    def __init__(self, main_scene):
        super().__init__('Game Over')
        self.main_scene: MainScene = main_scene
        self.texts: list[Text] = self.get_texts()

    def get_texts(self) -> list[Text]:
        victory_text: Text = Text(f'Winner: {self.main_scene.winner}' if self.main_scene.winner else 'Draw', 70)
        victory_text.update_center_position(center_cord=(self.main_scene.resolution[0] // 2,
                                                         self.main_scene.resolution[1] // 2))

        space_text: Text = Text('Press space to continue', 40)
        space_text.update_center_position(center_cord=(self.main_scene.resolution[0] // 2,
                                                       self.main_scene.resolution[1] // 2 + 55))
        return [victory_text, space_text]

    def event_check(self, event: pg.event) -> None:
        super().event_check(event)
        if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
            MainScene().start()

    def draw_to_screen(self) -> None:
        for text in self.texts:
            text.draw(self.main_scene.screen)
