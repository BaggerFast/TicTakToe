from unittest import TestCase
from objects import TicTacToe


class TestVictory(TestCase):

    def test_verticals(self):
        field = [
            ['x', '0', 'x'],
            ['x', '0', 'x'],
            ['x', 'x', '0'],
        ]
        self.assertEqual(TicTacToe.get_win_status(field, 'x'), True)

        field = [
            ['0', 'x', 'x'],
            ['x', 'x', '0'],
            ['0', 'x', '0'],
        ]
        self.assertEqual(TicTacToe.get_win_status(field, 'x'), True)

        field = [
            ['x', '0', 'x'],
            ['0', '0', 'x'],
            ['0', 'x', 'x'],
        ]
        self.assertEqual(TicTacToe.get_win_status(field, 'x'), True)

        field = [
            ['x', '0', 'x'],
            ['x', '0', 'x'],
            ['x', 'x', '0'],
        ]
        self.assertEqual(TicTacToe.get_win_status(field, '0'), False)

    def test_horizontals(self):

        field = [
            ['x', 'x', 'x'],
            ['0', '0', 'x'],
            ['x', 'x', '0'],
        ]
        self.assertEqual(TicTacToe.get_win_status(field, 'x'), True)

        field = [
            ['0', 'x', '0'],
            ['x', 'x', 'x'],
            ['0', '0', 'x'],

        ]
        self.assertEqual(TicTacToe.get_win_status(field, 'x'), True)

        field = [
            ['0', 'x', '0'],
            ['0', '0', 'x'],
            ['x', 'x', 'x'],

        ]
        self.assertEqual(TicTacToe.get_win_status(field, 'x'), True)

        field = [
            ['0', 'x', '0'],
            ['x', 'x', 'x'],
            ['0', '0', 'x'],

        ]
        self.assertEqual(TicTacToe.get_win_status(field, '0'), False)

    def test_diagonals(self):
        field = [
            ['0', 'x', '0'],
            ['x', '0', 'x'],
            ['x', '0', '0'],
        ]
        self.assertEqual(TicTacToe.get_win_status(field, '0'), True)

        field = [
            ['0', '0', 'x'],
            ['0', 'x', '0'],
            ['x', '0', '0'],
        ]
        self.assertEqual(TicTacToe.get_win_status(field, 'x'), True)

        field = [
            ['0', '0', 'x'],
            ['0', 'x', '0'],
            ['x', '0', '0'],
        ]
        self.assertEqual(TicTacToe.get_win_status(field, '0'), False)
