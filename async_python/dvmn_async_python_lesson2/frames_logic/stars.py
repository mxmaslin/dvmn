import asyncio
import curses
import random

from constants import STARS_AMOUNT, DIM_TIME, REGULAR_TIME, BRIGHT_TIME
from .sleep import sleep


async def star_phase(offset_ticks):
    random_ticks = random.randint(0, offset_ticks)
    await sleep(random_ticks)


async def blink(canvas, row, column, symbol='*'):
    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        await star_phase(DIM_TIME)
  
        canvas.addstr(row, column, symbol)
        await star_phase(REGULAR_TIME)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        await star_phase(BRIGHT_TIME)

        canvas.addstr(row, column, symbol)
        await star_phase(REGULAR_TIME)


def create_stars(canvas):
    stars = []
    window_height, window_width = canvas.getmaxyx()
    for _ in range(STARS_AMOUNT):
        star_shape = random.choice('+*.:')
        star_y = random.randint(1, window_height - 1)
        star_x = random.randint(1, window_width - 1)
        stars.append(blink(canvas, star_y, star_x, star_shape))
    return stars
