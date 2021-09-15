import pygame as pg
from scenes.base import Base
from misc import Color, Sign


class MainScene(Base):
    def __init__(self, game, cell_count: int = 3):
        super().__init__(game, 'Tic Tac Toe')
        # graphics
        self.size_block: int = 150
        self.retreat: int = 2
        self.cell_count: int = cell_count
        self.resolution: tuple = tuple([self.size_block * self.cell_count + self.retreat * (self.cell_count + 1)] * 2)
        self.screen = pg.display.set_mode(self.resolution)

        # logic
        self.move: int = 1
        self.winner: str = ''
        self.field: list[list[str]] = [[Sign.empty] * self.cell_count for _ in range(self.cell_count)]

    def finish(self) -> None:
        self.game.Scenes.gameover(self.game, self).start()

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
        pg.draw.line(self.screen, Color.red, rect.topright, rect.bottomleft, 5)
        pg.draw.line(self.screen, Color.red, rect.topleft, rect.bottomright, 5)

    def draw_circle(self, rect: pg.Rect) -> None:
        pg.draw.circle(self.screen, Color.green, rect.center, self.size_block // 2, 5)

    @staticmethod
    def check_cursor_click(cursor_pos: tuple, rect: pg.Rect, cell_sign: str) -> bool:
        return rect.left <= cursor_pos[0] <= rect.right and rect.top <= cursor_pos[1] <= rect.bottom \
               and cell_sign == Sign.empty

    def get_cord_for_rect(self, i: int) -> int:
        return self.size_block * i + (i + 1) * self.retreat

    def get_rect(self, row_cord: int, col_cord: int) -> pg.Rect:
        return pg.Rect(row_cord, col_cord, self.size_block, self.size_block)