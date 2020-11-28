"""
a_star
"""

from a_star.a_star import start
from a_star.cell import CellState  # pylint: disable=unused-import

WIDTH = 20
HEIGHT = 20

field = start(WIDTH, HEIGHT)

field.place_start(2, 10)
field.place_end(17, 10)
field.place_border_from_to(10, 7, 10, 14)
field.place_border_from_to(0, 7, 10, 7)
field.place_border_from_to(2, 14, 10, 14)
field.place_border_from_to(7, 14, 7, 17)
field.place_border_from_to(10, 14, 17, 14)
field.place_border_from_to(12, 12, 19, 12)

path = field.find_path()
if path:
    for cell in path:
        cell.change_state(CellState.PATH)
    print(field)
