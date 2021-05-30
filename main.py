import pygame as pg
import sys
from text import Text

red = 255, 0, 0
green = 0, 255, 0
white = [255] * 3
black = [0] * 3


class Game:
    def __init__(self):
        pg.display.init()
        pg.display.set_caption("Tic tac toe")

        self.size_block = 150
        self.retreat = 7
        self.resolution = self.size_block * 3 + self.retreat * 4, self.size_block * 3 + self.retreat * 4
        self.screen = pg.display.set_mode(self.resolution)
        self.game_over = False
        self.exit = False
        self.time_wait = 5

        self.pole = [[0]*3 for _ in range(3)]
        self.rects = [[0]*3 for _ in range(3)]

        self.victory_text = Text('Win: ', 70, white)
        self.victory_text.update_position(self.victory_text.surface.get_rect(center=((self.resolution[0] // 2, self.resolution[1] // 2))))

        self.space_text = Text('Press space to continue', 40, white)
        self.space_text.update_position(self.space_text.surface.get_rect(center=((self.resolution[0] // 2, self.resolution[1] // 2 + 55))))
        self.rect_init()

        self.move = 1

    def draw_element(self):
        for row in range(3):
            for col in range(3):
                color = white
                if self.pole[row][col] == 1:
                    color = red
                if self.pole[row][col] == 2:
                    color = green
                pg.draw.rect(self.screen, color, self.rects[row][col])
                self.draw_cross_or_circle(self.pole[row][col], self.rects[row][col])

    def draw_cross_or_circle(self, pole, rect):
        if pole == 1:
            pg.draw.line(self.screen, white, rect.topright, rect.bottomleft, 5)
            pg.draw.line(self.screen, white, rect.topleft, rect.bottomright, 5)
        if pole == 2:
            pg.draw.circle(self.screen, white, rect.center, self.size_block // 2, 5)

    def draw_to_screen(self):
        self.screen.fill(black)
        self.draw_element()
        pg.display.update()
        pg.time.wait(self.time_wait)

    def check_rects_border(self, cord_x, cord_y, rect=pg.Rect):
        if rect.left <= cord_x <= rect.right and rect.top <= cord_y <= rect.bottom:
            return 1
        return 0

    def check_game_over(self, move):
        # горизонт
        for row in range(3):
            sum = 0
            for col in range(3):
                if self.pole[row][col] == move:
                    sum += self.pole[row][col]
            if sum == move * 3:
                return True
        # вертикал
        for col in range(3):
            sum = 0
            for row in range(3):
                if self.pole[row][col] == move:
                    sum += self.pole[row][col]
            if sum == move * 3:
                return True
        # диагональ
        if self.pole[0][0] == self.pole[1][1] == self.pole[2][2] != 0 or self.pole[0][2] == self.pole[1][1] == self.pole[2][0] != 0:
            return True
        return False

    def rect_init(self):
        for row in range(3):
            for col in range(3):
                x = self.size_block * col + (col + 1) * self.retreat
                y = self.size_block * row + (row + 1) * self.retreat
                self.rects[row][col] = pg.Rect(x, y, self.size_block, self.size_block)

    def click_event(self):
        mouse_x, mouse_y = pg.mouse.get_pos()
        for i in range(3):
            for j in range(3):
                if self.check_rects_border(mouse_x, mouse_y, self.rects[i][j]) and self.pole[i][j] == 0:
                    sign = 1
                    if self.move % 2 == 0:
                        sign = 2
                    self.pole[i][j] = sign
                    if self.check_game_over(self.pole[i][j]):
                        self.victory_text.update_text(str(self.pole[i][j]))
                        self.game_over = True
                    elif self.move == 9:
                        self.game_over = True
                    self.move += 1

    def event_check(self, event):
        if event.type == pg.QUIT:
            self.exit = self.game_over = True
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            self.click_event()

    def game_logic(self):
        self.draw_to_screen()

    def start(self):
        while not self.game_over:
            for event in pg.event.get():
                self.event_check(event)
            self.game_logic()

    def final_scene(self):
        resource = {
            '1': 'X',
            '2': 'О'
        }
        if self.victory_text.text in resource:
            self.victory_text.update_text(f'Won: {resource[self.victory_text.text]}')
        else:
            self.victory_text.update_text('Draw')
        self.victory_text.update_position(self.victory_text.surface.get_rect(center=((self.resolution[0] // 2, self.resolution[1] // 2))))
        if not self.exit:
            pg.time.wait(750)
        while self.game_over and not self.exit:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.game_over = False
                if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                    main()
                self.screen.fill(black)
                self.victory_text.draw(self.screen)
                self.space_text.draw(self.screen)
                pg.display.update()


def main():
    game = Game()
    game.start()
    game.final_scene()
    sys.exit()


if __name__ == '__main__':
    main()