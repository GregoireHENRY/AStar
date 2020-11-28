"""
Cell module
"""

from enum import Enum
from typing import Tuple


class AStar:
    """A* struct"""

    def __init__(self):
        self.parent: Cell = None
        self.local_value: int = None
        self.global_value: int = None
        self.is_visited: bool = False


class CellState(Enum):
    """All different possible states for a cell."""

    EMPTY = " "
    BORDER = "#"
    START = "X"
    END = "O"
    PATH = "."


class Cell:
    """Cell"""

    def __init__(self, position_x: int, position_y: int, state: CellState):
        self.position_x = position_x
        self.position_y = position_y
        self.state = state
        self.previous_state = CellState.EMPTY
        self.a_star = AStar()

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return self.state.value

    def change_state(self, new_state: CellState):
        """Change state of the cell and keep in memory the previous state."""
        self.previous_state = self.state
        self.state = new_state

    def revert(self):
        """Revert the previous state of a cell."""
        save_previous_state = self.previous_state
        self.previous_state = self.state
        self.state = save_previous_state

    def get_position(self) -> Tuple[int, int]:
        return self.position_x, self.position_y
