import random

from typing import Iterable, Callable, Optional

from .board import Board, Position
from .view import IView, Command


class Game:
    def __init__(self, board: Board, view: IView, max_val: int) -> None:
        self._board = board
        self._view = view
        self._max_val = max_val

        self._merges: set[Position] = set()

        size = self._board.size
        self._width = size.col
        self._height = size.row

    def _find_furthest_position(self, from_pos: Position, next_pos_fn: Callable[[Position], Position]) -> Optional[Position]:
        # Loop over each "next" cell, stop when "next" is invalid and use to_pos
        to_pos = from_pos.copy()
        next_pos = next_pos_fn(to_pos)
        while next_pos.in_bounds(0, 0, self._height, self._width) and self._board[next_pos] == 0:
            to_pos, next_pos = next_pos, next_pos_fn(next_pos)

        # Check for possible merge
        if next_pos.in_bounds(0, 0, self._height, self._width) and self._board[next_pos] == self._board[from_pos] and next_pos not in self._merges:
            to_pos = next_pos

        # Stop if start & end are the same
        if from_pos == to_pos:
            return None

        return to_pos

    def _try_slide_one(self, from_pos: Position, next_pos_fn: Callable[[Position], Position]) -> bool:
        to_pos = self._find_furthest_position(from_pos, next_pos_fn)

        if to_pos is None:
            return False

        was_merge = self._board.slide_one(from_pos, to_pos)
        if was_merge:
            self._merges.add(to_pos)
        return True

    def _slide_all(self, cell_chunks: Iterable[list[int]], mk_pos: Callable[[int, int], Position], reverse: bool, next_fn: Callable[[Position], Position]) -> bool:
        self._merges.clear()

        some_slide = False
        for coord_1, chunk in enumerate(cell_chunks):
            val_itr = enumerate(chunk)
            if reverse:
                val_itr = reversed(list(val_itr))
            for coord_2, val in val_itr:
                # Don't slide empty cells
                if val == 0:
                    continue
                from_pos = mk_pos(coord_1, coord_2)

                slid = self._try_slide_one(from_pos, next_fn)
                some_slide = some_slide or slid

        return some_slide

    def slide_left(self) -> bool:
        return self._slide_all(self._board.rows(), lambda y, x: Position(x, y), False, lambda p: p.left)

    def slide_right(self) -> bool:
        return self._slide_all(self._board.rows(), lambda y, x: Position(x, y), True, lambda p: p.right)

    def slide_up(self) -> bool:
        return self._slide_all(self._board.columns(), lambda x, y: Position(x, y), False, lambda p: p.up)

    def slide_down(self) -> bool:
        return self._slide_all(self._board.columns(), lambda x, y: Position(x, y), True, lambda p: p.down)

    def display_board(self) -> None:
        self._view.draw(self._board)

    def get_command(self) -> Command:
        return self._view.get_command()

    def is_game_over(self) -> bool:
        return self._board.get_max_value() >= self._max_val

    def add_random_val(self) -> None:
        empty_pos = random.choice(self._board.get_empty_positions())
        val = random.choices([1, 2], weights=[0.9, 0.1], k=1)[0]
        self._board[empty_pos] = val
