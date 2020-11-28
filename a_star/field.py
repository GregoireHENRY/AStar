"""
Field module
"""

import math
import operator
from typing import List, Tuple, Union

from pudb import set_trace as bp  # pylint: disable=unused-import

from a_star.cell import Cell, CellState

ADJACENT_MOVES = ((0, -1), (1, 0), (0, 1), (-1, 0))
DISTANCE_BETWEEN_NEIGHBOURS = 1


class Field:
    """Field"""

    def __init__(self, WIDTH=int, HEIGHT=int):
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.BORDERS_X = (0, WIDTH - 1)
        self.BORDERS_Y = (0, HEIGHT - 1)
        self.data: List[List[Cell]] = []
        self.start_position = None
        self.end_position = None
        self.init_field()

    def init_field(self):
        self.data = [
            [
                Cell(x, y, CellState.BORDER)
                if (x in self.BORDERS_X or y in self.BORDERS_Y)
                else Cell(x, y, CellState.EMPTY)
                for x in range(self.WIDTH)
            ]
            for y in range(self.HEIGHT)
        ]

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        if not self.data:
            return "empty field"
        return "\n".join("".join(str(cell) for cell in line) for line in self.data)

    def __getitem__(self, index=int) -> List[Cell]:
        return self.data[index]

    def get(self, position: Tuple[int, int]) -> Union[None, Cell]:
        """Get Cell at position."""
        if not self.is_inside(position[0], position[1]):
            return None
        return self[position[1]][position[0]]

    def is_inside(self, position_x: int, position_y: int) -> bool:
        """Test if a point of the path if inside the field."""
        return (
            self.BORDERS_X[0] < position_x < self.BORDERS_X[1]
            and self.BORDERS_Y[0] < position_y < self.BORDERS_Y[1]
        )

    def place_if_not_border(self, position_x: int, position_y: int, state: CellState) -> bool:
        """Place the starting or ending point of the path."""
        cell = self.get((position_x, position_y))
        if cell and cell != CellState.BORDER:
            cell.change_state(state)
            return True
        return False

    def place_start(self, position_x: int, position_y: int) -> None:
        """Place the start point of the path."""
        if self.place_if_not_border(position_x, position_y, CellState.START):
            self.remove_previous_point(self.start_position)
            self.start_position = (position_x, position_y)

    def place_end(self, position_x: int, position_y: int) -> None:
        """Place the end point of the path."""
        if self.place_if_not_border(position_x, position_y, CellState.END):
            self.remove_previous_point(self.end_position)
            self.end_position = (position_x, position_y)

    def place_border(self, position_x: int, position_y: int) -> None:
        """Place a border."""
        self.place_if_not_border(position_x, position_y, CellState.BORDER)

    def place_border_from_to(
        self, START_POSITION_X: int, START_POSITION_Y: int, END_POSITION_X: int, END_POSITION_Y: int
    ) -> None:
        """Place ranges of borders."""
        RANGE_X = range(START_POSITION_X, END_POSITION_X + 1)
        RANGE_Y = range(START_POSITION_Y, END_POSITION_Y + 1)
        for y in RANGE_Y:
            for x in RANGE_X:
                self.place_if_not_border(x, y, CellState.BORDER)

    def remove_previous_point(self, position: Union[None, Tuple[int, int]]) -> None:
        """Remove the previous start or end position if existing."""
        if not position:
            return
        cell = self.get(position)
        if cell:
            cell.revert()

    def get_neighbours(self, cell: Cell) -> List[Cell]:
        """Get neighbours of a cell."""
        neighbours: List[Cell] = []
        for delta in ADJACENT_MOVES:
            neighbour_position = cell.position_x + delta[0], cell.position_y + delta[1]
            neighbour = self.get(neighbour_position)
            if neighbour and neighbour.state != CellState.BORDER:
                neighbours.append(neighbour)
        return neighbours

    def find_path(self) -> Union[None, List[Cell]]:
        """Find path from start to end points."""
        # test before start of algo
        if not self.start_position or not self.end_position:
            return None
        # test if cells start and end exist
        cell_start = self.get(self.start_position)
        cell_end = self.get(self.end_position)
        if not cell_start or not cell_end:
            return None
        cell_start.a_star.local_value = 0
        cell_start.a_star.global_value = self.distance_between_cells(cell_end, cell_start)
        # the list of cells to test starts with the starting cell
        list_cells_to_test: List[Cell] = [cell_start]
        # loop to find cost by path to reach end cell
        while list_cells_to_test:
            cell = list_cells_to_test[0]
            if cell.a_star.is_visited:
                list_cells_to_test.pop(0)
                continue
            neighbours = self.get_neighbours(cell)
            for neighbour in neighbours:
                # A* condition to look forward and avoid going backward
                if (
                    neighbour.a_star.local_value is None
                    or cell.a_star.local_value
                    < neighbour.a_star.local_value + DISTANCE_BETWEEN_NEIGHBOURS
                ):
                    neighbour.a_star.parent = cell
                    neighbour.a_star.local_value = (
                        cell.a_star.local_value + DISTANCE_BETWEEN_NEIGHBOURS
                    )
                    neighbour.a_star.global_value = (
                        self.distance_between_cells(cell_end, neighbour)
                        + neighbour.a_star.local_value
                    )
                    if neighbour != cell_end:
                        # neighbour.change_state(CellState.PATH)
                        list_cells_to_test.append(neighbour)
            cell.a_star.is_visited = True
            list_cells_to_test.pop(0)
            list_cells_to_test.sort(key=operator.attrgetter("a_star.global_value"))
        list_cells_to_test.sort(key=operator.attrgetter("a_star.global_value"))
        # goes through end cell parents to find optimized path
        path = [cell_end]
        while path[-1].a_star.parent is not None:
            path.append(path[-1].a_star.parent)
        path.pop(0)
        path.pop(-1)
        return path

    def distance_between_cells(self, cell_1: Cell, cell_2: Cell) -> int:
        """Compute the Manhattan distance between two cells."""
        return abs(cell_2.position_x - cell_1.position_x) + abs(
            cell_2.position_y - cell_2.position_y
        )
