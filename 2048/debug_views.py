from typing import Tuple

from main import Board
import curses


BOX_CHARS = ' ╵╷│╴┘┐┤╶└┌├─┴┬┼'
UP =    0b0001
DOWN =  0b0010
LEFT =  0b0100
RIGHT = 0b1000


def _board_to_chars(board_coord: int, cell_size: int) -> int:
    return cell_size * board_coord + (cell_size // 2)


class IView:
    def draw(self, board: Board) -> None:
        raise NotImplementedError

    def clear(self) -> None:
        raise NotImplementedError


class _PainterView(IView):
    def __init__(self, cell_width: int, cell_height: int, out_width: int, out_height: int):
        self._cell_width = cell_width
        self._cell_height = cell_height
        self._out_width = out_width
        self._out_height = out_height

    def draw(self, board: Board) -> None:
        self.clear()

        # Fill in borders
        for x_coord in range(self._out_width):
            self.draw_at(0, x_coord, BOX_CHARS[LEFT | RIGHT])
            self.draw_at(-1, x_coord, BOX_CHARS[LEFT | RIGHT])
        for y_coord in range(self._out_height):
            self.draw_at(y_coord, 0, BOX_CHARS[UP | DOWN])
            self.draw_at(y_coord, -1, BOX_CHARS[UP | DOWN])

        # Draw corners
        for x_coord, x_char in [(0, RIGHT), (-1, LEFT)]:
            for y_coord, y_char in [(0, DOWN), (-1, UP)]:
                self.draw_at(y_coord, x_coord, BOX_CHARS[x_char | y_char])

        # Fill in internal grid-lines
        for y_coord in range(0, self._out_height):
            for x_coord in range(0, self._out_width):
                box_idx = 0
                if y_coord % self._cell_height == 0:
                    if x_coord != 0:
                        box_idx |= LEFT
                    if x_coord != self._out_width-1:
                        box_idx |= RIGHT
                if x_coord % self._cell_width == 0:
                    if y_coord != 0:
                        box_idx |= UP
                    if y_coord != self._out_height-1:
                        box_idx |= DOWN
                self.draw_at(y_coord, x_coord, BOX_CHARS[box_idx])

        # Fill values
        val_alphabet = '0123456789' + ''.join([chr(x) for x in range(ord('A'), ord('Z')+1)])

        for pos, val in board:
            self.draw_at(_board_to_chars(pos.row, self._cell_height), _board_to_chars(pos.col, self._cell_width), val_alphabet[val])

    def clear(self) -> None:
        raise NotImplementedError

    def draw_at(self, y: int, x: int, s: str) -> None:
        raise NotImplementedError


class PTUIView(_PainterView):
    def __init__(self, cell_size: Tuple[int, int], board_size: Tuple[int, int]):
        cell_width, cell_height = cell_size
        board_width, board_height = board_size

        super().__init__(cell_size[0], cell_size[1], board_width * cell_width + 1, board_height * cell_height + 1)

        self._out_chars = []
        self.clear()

    def clear(self) -> None:
        self._out_chars = [['?'] * self._out_width for _ in range(self._out_height)]

    def draw_at(self, y: int, x: int, s: str) -> None:
        self._out_chars[y][x] = s

    def draw(self, board: Board) -> None:
        super().draw(board)
        print('\n'.join([''.join([cell for cell in row]) for row in self._out_chars]))


class CursesView(_PainterView):
    def __init__(self, scr: curses.window, cell_size: Tuple[int, int], board_size: Tuple[int, int]):
        self._scr = scr

        cell_width, cell_height = cell_size
        board_width, board_height = board_size

        super().__init__(cell_size[0], cell_size[1], board_width * cell_width + 1, board_height * cell_height + 1)

    def clear(self) -> None:
        self._scr.clear()

    def draw_at(self, y: int, x: int, s: str) -> None:
        if y < 0:
            y = self._out_width + y
        if x < 0:
            x = self._out_width + x
        self._scr.addch(y, x, s)

    def draw(self, board: Board) -> None:
        super().draw(board)
        self._scr.getch()
