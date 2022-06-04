from dataclasses import dataclass
from typing import Iterator, Tuple


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

    def _can_merge(self, pos_1: Position, pos_2: Position) -> bool:
        return self[pos_1] == self[pos_2]

    def _slide(self, from_pos: Position, to_pos: Position) -> None:
        if self[from_pos] == self[to_pos]:
            self[to_pos] += 1
        elif self[to_pos] != 0:
            raise RuntimeError(f'Cannot slide value to non-empty, non-matching cell at {to_pos}')
        else:
            self[to_pos] = self[from_pos]

        self[from_pos] = 0

    def slide_left(self) -> None:
        for y_coord, row in enumerate(self._cells):
            for x_coord, val in enumerate(row):
                # Don't slide empty cells
                if val == 0:
                    continue

                # Find left-most slide-able position
                start_pos = Position(x_coord, y_coord)
                curr_pos = start_pos.copy()
                next_pos = curr_pos.left
                while next_pos.in_bounds(0, 0, self._height, self._width) and self[next_pos] == 0:
                    curr_pos, next_pos = next_pos, next_pos.left

                # If next_pos is in bounds, ie not empty, and has the same value as start_pos, set it as curr_pos
                if next_pos.in_bounds(0, 0, self._height, self._width) and self[next_pos] == self[start_pos]:
                    curr_pos = next_pos

                # Slide from start to curr
                if start_pos != curr_pos:
                    self._slide(start_pos, curr_pos)

    def slide_right(self) -> None:
        for y_coord, row in enumerate(self._cells):
            for x_coord, val in reversed(list(enumerate(row))):
                # Don't slide empty cells
                if val == 0:
                    continue

                # Find right-most slide-able position
                start_pos = Position(x_coord, y_coord)
                curr_pos = start_pos.copy()
                next_pos = curr_pos.right
                while next_pos.in_bounds(0, 0, self._height, self._width) and self[next_pos] == 0:
                    curr_pos, next_pos = next_pos, next_pos.right

                # If next_pos is in bounds, ie not empty, and has the same value as start_pos, set it as curr_pos
                if next_pos.in_bounds(0, 0, self._height, self._width) and self[next_pos] == self[start_pos]:
                    curr_pos = next_pos

                # Slide from start to curr
                if start_pos != curr_pos:
                    self._slide(start_pos, curr_pos)

    def slide_up(self) -> None:
        for x_coord in range(self._width):
            col = [self._cells[r][x_coord] for r in range(self._height)]

            for y_coord, val in enumerate(col):
                # Don't slide empty cells
                if val == 0:
                    continue

                # Find right-most slide-able position
                start_pos = Position(x_coord, y_coord)
                curr_pos = start_pos.copy()
                next_pos = curr_pos.up
                while next_pos.in_bounds(0, 0, self._height, self._width) and self[next_pos] == 0:
                    curr_pos, next_pos = next_pos, next_pos.up

                # If next_pos is in bounds, ie not empty, and has the same value as start_pos, set it as curr_pos
                if next_pos.in_bounds(0, 0, self._height, self._width) and self[next_pos] == self[start_pos]:
                    curr_pos = next_pos

                # Slide from start to curr
                if start_pos != curr_pos:
                    self._slide(start_pos, curr_pos)

    def slide_down(self) -> None:
        for x_coord in range(self._width):
            col = [self._cells[r][x_coord] for r in range(self._height)]

            for y_coord, val in reversed(list(enumerate(col))):
                # Don't slide empty cells
                if val == 0:
                    continue

                # Find right-most slide-able position
                start_pos = Position(x_coord, y_coord)
                curr_pos = start_pos.copy()
                next_pos = curr_pos.down
                while next_pos.in_bounds(0, 0, self._height, self._width) and self[next_pos] == 0:
                    curr_pos, next_pos = next_pos, next_pos.down

                # If next_pos is in bounds, ie not empty, and has the same value as start_pos, set it as curr_pos
                if next_pos.in_bounds(0, 0, self._height, self._width) and self[next_pos] == self[start_pos]:
                    curr_pos = next_pos

                # Slide from start to curr
                if start_pos != curr_pos:
                    self._slide(start_pos, curr_pos)
