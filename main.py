import pygame as pg
from text import Text
from constans import Color, Sign


class Game:
    def __init__(self):
        self.size_block: int = 150
        self.retreat: int = 7
        self.time_wait: int = 5
        self.move: int = 1

        self.winner = None

        self.resolution: tuple = (self.size_block * 3 + self.retreat * 4, self.size_block * 3 + self.retreat * 4)
        self.screen = pg.display.set_mode(self.resolution)

        self.game_over: bool = False
        self.exit: bool = False

        self.pole = [[Sign.empty] * 3 for _ in range(3)]
        self.rects = [[0] * 3 for _ in range(3)]

        self.victory_text: Text = Text('', 70, Color.white)
        self.victory_text.update_center_position(center_cord=(self.resolution[0] // 2, self.resolution[1] // 2))

        self.space_text: Text = Text('Press space to continue', 40, Color.white)
        self.space_text.update_center_position(center_cord=(self.resolution[0] // 2, self.resolution[1] // 2 + 55))

    def start(self):
        self.field_init()
        self.main_loop()
        self.final_scene()

    def draw_element(self):
        context = {
            Sign.x: self.draw_cross,
            Sign.o: self.draw_circle
        }
        for row in range(3):
            for col in range(3):
                cell = self.pole[row][col]
                cell_rect = self.rects[row][col]
                if cell in context:
                    context[cell](cell_rect)
                else:
                    pg.draw.rect(self.screen, Color.white, cell_rect)

    def draw_cross(self, rect):
        # 1
        pg.draw.rect(self.screen, Color.red, rect)
        pg.draw.line(self.screen, Color.white, rect.topright, rect.bottomleft, 5)
        pg.draw.line(self.screen, Color.white, rect.topleft, rect.bottomright, 5)

    def draw_circle(self, rect):
        # 2
        pg.draw.rect(self.screen, Color.green, rect)
        pg.draw.circle(self.screen, Color.white, rect.center, self.size_block // 2, 5)

    def draw_to_screen(self):
        self.screen.fill(Color.black)
        self.draw_element()
        pg.display.update()
        pg.time.wait(self.time_wait)

    @staticmethod
    def collision_with_rect(cord_x, cord_y, rect=pg.Rect):
        if rect.left <= cord_x <= rect.right and rect.top <= cord_y <= rect.bottom:
            return True
        return False

    @staticmethod
    def check_win(move, dirs):
        for dir in dirs:
            for row in range(3):
                sum = 0
                for col in range(3):
                    if dir(row, col) == move:
                        sum += 1
                if sum == 3:
                    return True

    # todo refactor func
    def check_game_over(self, move):
        # горизонт
        dirs = [
            lambda x, y: self.pole[x][y],  # горизонт
            lambda y, x: self.pole[x][y],  # вертикаль
        ]
        if self.check_win(move, dirs):
            return True
        # диагональ
        if self.pole[0][0] == self.pole[1][1] == self.pole[2][2] != Sign.empty or \
                self.pole[0][2] == self.pole[1][1] == self.pole[2][0] != Sign.empty:
            return True
        return False

    def field_init(self):
        cord = lambda i: self.size_block * i + (i + 1) * self.retreat
        for row in range(3):
            for col in range(3):
                self.rects[row][col] = pg.Rect(cord(col), cord(row), self.size_block, self.size_block)

    # todo refactor
    def click_event(self):
        mouse_x, mouse_y = pg.mouse.get_pos()
        for i in range(3):
            for j in range(3):
                if self.collision_with_rect(mouse_x, mouse_y, self.rects[i][j]) and self.pole[i][j] == Sign.empty:
                    if self.move % 2:
                        sign = Sign.x
                    else:
                        sign = Sign.o
                    self.pole[i][j] = sign
                    if self.check_game_over(self.pole[i][j]):
                        self.winner = self.pole[i][j]
                        self.game_over = True
                    elif self.move == 9:
                        self.game_over = True
                    self.move += 1

    def event_check(self, event):
        if event.type == pg.QUIT:
            self.exit = self.game_over = True
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            self.click_event()

    # todo refactor
    def game_logic(self):
        self.draw_to_screen()

    def main_loop(self):
        while not self.game_over:
            for event in pg.event.get():
                self.event_check(event)
            self.game_logic()

    # todo refactor
    def final_scene(self):
        if self.winner:
            self.victory_text.update_text(f'Won: {self.winner}')
        else:
            self.victory_text.update_text('Draw')
        self.victory_text.update_center_position(center_cord=(self.resolution[0] // 2, self.resolution[1] // 2))
        if not self.exit:
            pg.time.wait(750)
        while self.game_over and not self.exit:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.game_over = False
                if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                    self.__init__()
                    self.start()
                self.screen.fill(Color.black)
                self.victory_text.draw(self.screen)
                self.space_text.draw(self.screen)
                pg.display.update()
