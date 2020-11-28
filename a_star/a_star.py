"""
A* algorithm to find the shortest path in a 2D grid from a starting point to an end point.
"""

from a_star.field import Field


def start(WIDTH: int, HEIGHT: int) -> Field:
    """a_star"""
    # create field
    field = Field(WIDTH, HEIGHT)
    return field
