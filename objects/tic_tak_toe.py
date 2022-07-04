from typing import Final
import pygame as pg

from misc import IEventful, IDrawable
from settings import CELL_COUNT, CELL_SIZE, GRID_THICKNESS, Color, GAME_NAME


class Sign:
    X: Final = 'X'
    O: Final = '0'
    EMPTY: Final = ''


class TicTacToe(IDrawable, IEventful):

    def __init__(self):
        self.__move: int = 1
        self.__field = [[Sign.EMPTY] * CELL_COUNT for _ in range(CELL_COUNT)]
        self.__field_rects = []
        self.__update_title()
        self.__setup_field_rects()

    # region Public

    # region Implementation of IDrawable, IEventful

    def process_draw(self, screen: pg.Surface) -> None:
        context = {
            Sign.X: self.__draw_cross,
            Sign.O: self.__draw_circle
        }
        for y, row in enumerate(self.__field_rects):
            for x, rect in enumerate(row):
                pg.draw.rect(screen, Color.GREEN, rect)
                if (sign := self.__field[y][x]) in context:
                    context[sign](screen, rect)

    def process_event(self, event: pg.event.Event) -> None:
        if not (event.type == pg.MOUSEBUTTONDOWN and event.button == 1):
            return
        cursor_pos = pg.mouse.get_pos()
        for y, row in enumerate(self.__field_rects):
            for x, rect in enumerate(row):
                if not (self.__cursor_click_isvalid(cursor_pos, rect) and self.__field[y][x] == Sign.EMPTY):
                    continue
                self.__field[y][x] = (sign := Sign.X if self.__move % 2 else Sign.O)
                if self.get_win_status(self.__field, sign):
                    from scenes import GameOverScene, SceneManager
                    SceneManager().current = GameOverScene(sign)
                    return
                elif self.__move == CELL_COUNT ** 2:
                    from scenes import GameOverScene, SceneManager
                    SceneManager().current = GameOverScene('Draw')
                    return
                self.__move += 1
                self.__update_title()

    # endregion

    @staticmethod
    def get_win_status(field: list[list[str, ...]], move: str) -> bool:
        for i in range(CELL_COUNT):
            lines = [[field[j][i] for j in range(CELL_COUNT)], field[i]]
            for line in lines:
                if line.count(move) == CELL_COUNT:
                    return True

        secondary_diagonal = [field[i][CELL_COUNT - i - 1] for i in range(CELL_COUNT)]
        main_diagonal = [field[i][i] for i in range(CELL_COUNT)]

        for line in (secondary_diagonal, main_diagonal):
            if line.count(move) == CELL_COUNT:
                return True

        return False

    # endregion

    # region Private

    @staticmethod
    def __draw_cross(screen: pg.Surface, rect: pg.Rect) -> None:
        margin = 40
        bold = 7

        top_right = (rect.topright[0] - margin, rect.topright[1] + margin)
        bottom_left = (rect.bottomleft[0] + margin, rect.bottomleft[1] - margin)
        pg.draw.line(screen, Color.BROWN, top_right, bottom_left, bold)

        top_left = (rect.topleft[0] + margin, rect.topleft[1] + margin)
        bottom_right = (rect.bottomright[0] - margin, rect.bottomright[1] - margin)
        pg.draw.line(screen, Color.BROWN, top_left, bottom_right, bold)

    @staticmethod
    def __draw_circle(screen: pg.Surface, rect: pg.Rect) -> None:
        pg.draw.circle(screen, Color.WHEAT, rect.center, CELL_SIZE // 2 - 40, 7)

    @staticmethod
    def __cursor_click_isvalid(cursor_pos: tuple, rect: pg.Rect) -> bool:
        return rect.left <= cursor_pos[0] <= rect.right and rect.top <= cursor_pos[1] <= rect.bottom

    def __setup_field_rects(self) -> None:
        self.__field_rects.clear()
        for row in range(CELL_COUNT):
            self.__field_rects.append([])
            row_coord = CELL_SIZE * row + GRID_THICKNESS * (row + 1)
            for col in range(CELL_COUNT):
                col_coord = CELL_SIZE * col + GRID_THICKNESS * (col + 1)
                self.__field_rects[-1].append(pg.Rect(row_coord, col_coord, CELL_SIZE, CELL_SIZE))

    def __update_title(self):
        pg.display.set_caption(f'{GAME_NAME} - {Sign.X if self.__move % 2 else Sign.O}')

    # endregion
