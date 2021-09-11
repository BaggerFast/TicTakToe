import pygame as pg
import sys

from constans import Sign, Color
from text import Text


class BaseScene:
    def __init__(self, header_name: str):
        pg.display.set_caption(header_name)
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


class MainScene(BaseScene):
    def __init__(self, cell_count: int = 3):
        super().__init__('Tic Tac Toe')
        # graphics
        self.size_block: int = 150
        self.retreat: int = 2
        self.cell_count: int = cell_count
        self.figure_thickness = 10
        self.resolution: tuple = tuple([self.size_block * self.cell_count + self.retreat * (self.cell_count + 1)] * 2)
        self.screen = pg.display.set_mode(self.resolution)

        # logic
        self.move: int = 1
        self.winner: str = ''
        self.field: list[list[str]] = [[Sign.empty] * self.cell_count for _ in range(self.cell_count)]

    def finish(self) -> None:
        GameOverScene(self).start()

    def event_check(self, event: pg.event) -> None:
        super().event_check(event)
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            self.click_event()

    def click_event(self) -> None:
        cursor_pos = pg.mouse.get_pos()
        for row in range(self.cell_count):
            row_cord = self.get_cord_for_rect(row)
            for col in range(self.cell_count):
                col_cord = self.get_cord_for_rect(col)
                if self.check_cursor_click(cursor_pos, self.get_rect(row_cord, col_cord), self.field[row][col]):
                    sign = Sign.x if self.move % 2 else Sign.o
                    self.field[row][col] = sign
                    if self.check_win_status(sign):
                        self.winner = sign
                        self.scene_active = False
                    elif self.move == self.cell_count ** 2:
                        self.scene_active = False
                    self.move += 1

    def check_win_status(self, move: str) -> bool:
        for i in range(self.cell_count):
            lines = [[self.field[j][i] for j in range(self.cell_count)], self.field[i]]
            for line in lines:
                if line.count(move) == self.cell_count:
                    return True

        diagonals = [[self.field[i][i] for i in range(self.cell_count)],
                     [self.field[x][abs(self.cell_count - x - 1)] for x in range(self.cell_count)]]

        for line in diagonals:
            if line.count(move) == self.cell_count:
                return True
        return False

    def draw_to_screen(self) -> None:
        context = {
            Sign.x: lambda i: self.draw_cross(rect=i),
            Sign.o: lambda i: self.draw_circle(rect=i)
        }
        self.screen.fill(Color.white)
        for row in range(self.cell_count):
            row_cord = self.get_cord_for_rect(row)
            for col in range(self.cell_count):
                rect = self.get_rect(row_cord, self.get_cord_for_rect(col))
                pg.draw.rect(self.screen, Color.black, rect)
                if self.field[row][col] in context:
                    context[self.field[row][col]](rect)

    def draw_cross(self, rect: pg.Rect) -> None:
        indent = 23

        pg.draw.line(self.screen, Color.red, (rect.topright[0] - indent, rect.topright[1] + indent),
                     (rect.bottomleft[0] + indent, rect.bottomleft[1] - indent), self.figure_thickness)

        pg.draw.line(self.screen, Color.red, [i + indent for i in rect.topleft],
                     [i - indent for i in rect.bottomright], self.figure_thickness)

    def draw_circle(self, rect: pg.Rect) -> None:
        pg.draw.circle(self.screen, Color.green, rect.center, self.size_block // 2 - 15, self.figure_thickness)

    @staticmethod
    def check_cursor_click(cursor_pos: tuple, rect: pg.Rect, cell_sign: str) -> bool:
        return rect.left <= cursor_pos[0] <= rect.right and rect.top <= cursor_pos[1] <= rect.bottom \
               and cell_sign == Sign.empty

    def get_cord_for_rect(self, i: int) -> int:
        return self.size_block * i + (i + 1) * self.retreat

    def get_rect(self, row_cord: int, col_cord: int) -> pg.Rect:
        return pg.Rect(row_cord, col_cord, self.size_block, self.size_block)


class GameOverScene(BaseScene):
    def __init__(self, main_scene: MainScene):
        super().__init__('Game Over')
        self.main_scene: MainScene = main_scene
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
            MainScene(cell_count=self.main_scene.cell_count).start()

    def draw_to_screen(self) -> None:
        for text in self.texts:
            text.draw(screen=self.main_scene.screen)
