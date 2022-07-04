from objects import TicTacToe
from .base import Scene


class MainScene(Scene):

    # region Private

    # region Implementation of Scene

    def _create_objects(self) -> None:
        self._objects.append(TicTacToe())

    # endregion

    # endregion
