from enum import Enum, auto

from .board import Board


class Command(Enum):
    EXIT = auto()
    MV_UP = auto()
    MV_DOWN = auto()
    MV_LEFT = auto()
    MV_RIGHT = auto()
    ERR = auto()


class IView:
    def draw(self, board: Board) -> None:
        raise NotImplementedError

    def clear(self) -> None:
        raise NotImplementedError

    def get_command(self) -> Command:
        raise NotImplementedError