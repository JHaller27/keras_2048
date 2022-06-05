from dataclasses import dataclass
from typing import Iterator


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

    def __hash__(self) -> int:
        return hash((self.col, self.row))

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

    def rows(self) -> list[list[int]]:
        return [list(row) for row in self._cells]

    def columns(self) -> list[list[int]]:
        return [[row[x] for row in self._cells] for x in range(self._width)]

    def can_merge(self, pos_1: Position, pos_2: Position) -> bool:
        return self[pos_1] == self[pos_2]

    def slide_one(self, from_pos: Position, to_pos: Position) -> bool:
        """
        :return: True if cells merged at to_pos, False otherwise
        """

        merged = False

        # If will slide to cell with same value, increment value at destination
        if self[from_pos] == self[to_pos]:
            self[to_pos] += 1
            merged = True

        # If values are not the same, and dest is not empty, this is an error (this should never happen)
        elif self[to_pos] != 0:
            raise RuntimeError(f'Cannot slide value to non-empty, non-matching cell at {to_pos}')

        # If will slide to empty cell, set dest value to start cell value
        else:
            self[to_pos] = self[from_pos]

        # If slide has happened, start cell must now be empty
        self[from_pos] = 0

        return merged

    def get_max_value(self) -> int:
        return max([val for row in self._cells for val in row])

    def get_empty_positions(self) -> list[Position]:
        return [pos for pos, val in iter(self) if val == 0]
