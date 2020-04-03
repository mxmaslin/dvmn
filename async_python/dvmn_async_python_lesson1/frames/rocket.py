import asyncio

from curses_tools import draw_frame, read_controls
from constants import SHIP_LENGTH, SHIP_WIDTH


async def animate_spaceship(
        canvas, row, column, rocket_frame_1, rocket_frame_2
):
    window_height, window_width = canvas.getmaxyx()
    while True:
        row_step, column_step, fire = read_controls(canvas)

        row_change = row + row_step
        column_change = column + column_step

        vertical_ok = 0 < row_change < window_height - SHIP_LENGTH
        row = row_change if vertical_ok else row
        horizontal_ok = 0 < column_change < window_width - SHIP_WIDTH
        column = column_change if horizontal_ok else column

        draw_frame(canvas, row, column, rocket_frame_1)
        await asyncio.sleep(0)
        draw_frame(canvas, row, column, rocket_frame_1, negative=True)
        draw_frame(canvas, row, column, rocket_frame_2)
        await asyncio.sleep(0)
        draw_frame(canvas, row, column, rocket_frame_2, negative=True)
