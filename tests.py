from unittest import TestCase

from scenes import MainScene


class TestVictory(TestCase):
    game_3 = MainScene(cell_count=3)
    game_4 = MainScene(cell_count=4)

    def test_vertical(self):
        self.game_3.field = [
            ['x', '0', 'x'],
            ['x', '0', 'x'],
            ['x', 'x', '0'],
        ]
        self.assertEqual(self.game_3.check_win_status('x'), True)

        self.game_3.field = [
            ['0', '0', 'x'],
            ['x', 'x', 'x'],
            ['x', '0', '0'],
        ]
        self.assertEqual(self.game_3.check_win_status('x'), True)

        self.game_4.field = [
            ['0', '0', 'x', '0'],
            ['0', '0', 'x', '0'],
            ['x', 'x', '0', '0'],
            ['x', 'x', '0', '0'],
        ]
        self.assertEqual(self.game_4.check_win_status('0'), True)

    def test_horizon(self):
        self.game_3.field = [
            ['x', 'x', 'x'],
            ['0', '0', 'x'],
            ['x', 'x', '0'],
        ]
        self.assertEqual(self.game_3.check_win_status('x'), True)

        self.game_3.field = [
            ['x', 'x', '0'],
            ['0', '0', 'x'],
            ['x', 'x', 'x'],
        ]
        self.assertEqual(self.game_3.check_win_status('x'), True)

        self.game_4.field = [
            ['x', 'x', '0', '0'],
            ['0', '0', '0', '0'],
            ['0', 'x', 'x', '0'],
            ['x', '0', 'x', '0'],
        ]
        self.assertEqual(self.game_4.check_win_status('0'), True)

    def test_diagonals(self):
        self.game_3.field = [
            ['x', '0', '0'],
            ['0', 'x', '0'],
            ['0', '0', 'x'],
        ]
        self.assertEqual(self.game_3.check_win_status('x'), True)

        self.game_3.field = [
            ['0', '0', 'x'],
            ['0', 'x', '0'],
            ['x', '0', '0'],
        ]
        self.assertEqual(self.game_3.check_win_status('x'), True)

        self.game_4.field = [
            ['x', 'x', 'x', '0'],
            ['x', 'x', '0', 'x'],
            ['x', '0', 'x', 'x'],
            ['0', 'x', 'x', 'x'],
        ]
        self.assertEqual(self.game_4.check_win_status('0'), True)
