from abc import ABC
import pygame as pg

from objects import Objects
from misc import IGenericObject, SingletonMeta


class Scene(IGenericObject, ABC):

    def __init__(self):
        self._objects = Objects()
        self._create_objects()

    # region Public

    # region Implementation of IGenericObject

    def process_event(self, event: pg.event.Event) -> None:
        self._objects.process_event(event)

    def process_logic(self) -> None:
        self._objects.process_logic()

    def process_draw(self, screen: pg.Surface) -> None:
        self._objects.process_draw(screen)

    # endregion

    # endregion

    # region Private

    def _create_objects(self) -> None:
        pass

    # endregion


class SceneManager(metaclass=SingletonMeta):

    def __init__(self):
        self.__current = None
        self.__last = None

    # region Public

    @property
    def current(self) -> Scene:
        return self.__current

    @property
    def last(self) -> Scene:
        return self.__last

    @current.setter
    def current(self, scene: Scene):
        self.__last = self.__current
        self.__current = scene

    # endregion
