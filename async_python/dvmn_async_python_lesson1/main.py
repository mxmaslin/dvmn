import curses
import time

from frames.stars import create_stars
from frames.fire import fire
from frames.rocket import animate_spaceship

from constants import TIC_TIMEOUT, SHIP_LENGTH, SHIP_WIDTH


with open('frames/rocket_frame_1.txt') as file_1:
    rocket_frame_1 = file_1.read()
with open('frames/rocket_frame_2.txt') as file_2:
    rocket_frame_2 = file_2.read()


def draw(canvas):
    curses.curs_set(False)
    canvas.border()
    canvas.nodelay(True)

    window_height, window_width = canvas.getmaxyx()

    coroutines = []
    stars = create_stars(canvas)
    coroutines += stars

    bang = fire(canvas, 10, 10)
    coroutines += [bang]

    initial_y = window_height // 2 - SHIP_LENGTH // 2
    initial_x = window_width // 2 - SHIP_WIDTH // 2
    rocket = animate_spaceship(
        canvas, initial_y, initial_x, rocket_frame_1, rocket_frame_2
    )
    coroutines += [rocket]

    while True:
        for coroutine in coroutines:
            try:
                coroutine.send(None)
            except StopIteration:
                coroutines.remove(coroutine)

        canvas.refresh()

        time.sleep(1 * TIC_TIMEOUT)


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)
