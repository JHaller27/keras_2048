from dataclasses import dataclass
from typing import Iterator, Iterable, Callable, Optional


@dataclass
class Position:
    col: int
    row: int

    def __repr__(self) -> str:
        return f"P({self.col},{self.row})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Position):
            return False
        return self.col == other.col and self.row == other.row

    def copy(self) -> 'Position':
        return Position(self.col, self.row)

    @property
    def left(self) -> 'Position':
        return Position(self.col - 1, self.row)

    @property
    def right(self) -> 'Position':
        return Position(self.col + 1, self.row)

    @property
    def up(self) -> 'Position':
        return Position(self.col, self.row - 1)

    @property
    def down(self) -> 'Position':
        return Position(self.col, self.row + 1)

    def in_bounds(self, start_row: int, start_col: int, end_row: int, end_col: int) -> bool:
        return self.row in range(start_row, end_row) and self.col in range(start_col, end_col)

    @staticmethod
    def range(start_row: int, start_col: int, end_row: int, end_col: int) -> Iterator['Position']:
        for y in range(start_col, end_col):
            for x in range(start_row, end_row):
                yield Position(x, y)


class Board:
    def __init__(self, width: int, height: int):
        self._width = width
        self._height = height

        self._cells = [[0] * self._width for _ in range(self._height)]

    def __getitem__(self, item: Position) -> int:
        if not isinstance(item, Position):
            raise TypeError(f"Cannot index Board with index of type {type(item)}")

        return self._cells[item.row][item.col]

    def __setitem__(self, key: Position, value: int) -> None:
        if not isinstance(key, Position):
            raise TypeError(f"Cannot index Board with index of type {type(key)}")

        self._cells[key.row][key.col] = value

    def __iter__(self):
        return iter([(pos, self[pos]) for pos in Position.range(0, 0, self._height, self._width)])

    @property
    def size(self) -> Position:
        return Position(self._width, self._height)

    def _rows(self) -> list[list[int]]:
        return [list(row) for row in self._cells]

    def _columns(self) -> list[list[int]]:
        return [[row[x] for row in self._cells] for x in range(self._width)]

    def _can_merge(self, pos_1: Position, pos_2: Position) -> bool:
        return self[pos_1] == self[pos_2]

    def _find_furthest_position(self, from_pos: Position, next_pos_fn: Callable[[Position], Position]) -> Optional[Position]:
        # Loop over each "next" cell, stop when "next" is invalid and use to_pos
        to_pos = from_pos.copy()
        next_pos = next_pos_fn(to_pos)
        while next_pos.in_bounds(0, 0, self._height, self._width) and self[next_pos] == 0:
            to_pos, next_pos = next_pos, next_pos_fn(next_pos)

        # If next_pos is in bounds, ie not empty, and has the same value as from_pos, set it as to_pos
        if next_pos.in_bounds(0, 0, self._height, self._width) and self[next_pos] == self[from_pos]:
            to_pos = next_pos

        # Stop if start & end are the same
        if from_pos == to_pos:
            return None

        return to_pos

    def _slide_one(self, from_pos: Position, to_pos: Position) -> None:
        # If will slide to cell with same value, increment value at destination
        if self[from_pos] == self[to_pos]:
            self[to_pos] += 1

        # If values are not the same, and dest is not empty, this is an error (this should never happen)
        elif self[to_pos] != 0:
            raise RuntimeError(f'Cannot slide value to non-empty, non-matching cell at {to_pos}')

        # If will slide to empty cell, set dest value to start cell value
        else:
            self[to_pos] = self[from_pos]

        # If slide has happened, start cell must now be empty
        self[from_pos] = 0

    def _try_slide_one(self, from_pos: Position, next_pos_fn: Callable[[Position], Position]) -> None:
        to_pos = self._find_furthest_position(from_pos, next_pos_fn)

        if to_pos is None:
            return

        self._slide_one(from_pos, to_pos)

    def _slide_all(self, cell_chunks: Iterable[list[int]], mk_pos: Callable[[int, int], Position], reverse: bool, next_fn: Callable[[Position], Position]) -> None:
        for coord_1, chunk in enumerate(cell_chunks):
            val_itr = enumerate(chunk)
            if reverse:
                val_itr = reversed(list(val_itr))
            for coord_2, val in val_itr:
                # Don't slide empty cells
                if val == 0:
                    continue
                from_pos = mk_pos(coord_1, coord_2)
                self._try_slide_one(from_pos, next_fn)

    def slide_left(self) -> None:
        self._slide_all(self._rows(), lambda y, x: Position(x, y), False, lambda p: p.left)

    def slide_right(self) -> None:
        self._slide_all(self._rows(), lambda y, x: Position(x, y), True, lambda p: p.right)

    def slide_up(self) -> None:
        self._slide_all(self._columns(), lambda x, y: Position(x, y), False, lambda p: p.up)

    def slide_down(self) -> None:
        self._slide_all(self._columns(), lambda x, y: Position(x, y), True, lambda p: p.down)

    def get_max_value(self) -> int:
        return max([val for row in self._cells for val in row])

    def get_empty_positions(self) -> list[Position]:
        return [pos for pos, val in iter(self) if val == 0]
