import asyncio
import curses
import time
import random

from curses_tools import draw_frame, read_controls, get_frame_size

from frames_logic.obstacles import Obstacle, show_obstacles
from frames_logic.stars import create_stars
from frames_logic.sleep import sleep
from frames_logic.physics import update_speed
from frames_logic.explosion import explode
from frames_logic.show_gameover import show_gameover

from constants import SHIP_LENGTH, SHIP_WIDTH, TIC_TIMEOUT


garbage_frames = {}
for garbage_name in (
        'duck', 'hubble', 'lamp', 'trash_large', 'trash_small', 'trash_xl'
):
    with open(f'frames/{garbage_name}.txt') as file:
        garbage_frames[garbage_name] = file.read()
garbage_frames = list(garbage_frames.values())

with open(f'frames/rocket_frame_1.txt') as file:
    rocket_frame_1 = file.read()
with open(f'frames/rocket_frame_2.txt') as file:
    rocket_frame_2 = file.read()

coroutines = []
spaceship_frame = ''
obstacles = []
obstacles_in_last_collisions = []
year = 1957


async def fill_orbit_with_garbage(canvas):
    global coroutines
    ticks_lower = 30
    ticks_upper = 40
    while True:
        _, columns_number = canvas.getmaxyx()
        garbage_frame = random.choice(garbage_frames)
        _, garbage_columns_num = get_frame_size(garbage_frame)
        origin_column = random.randint(-garbage_columns_num, columns_number)
        garbage_speed = random.random()
        garbage_coroutine = fly_garbage(
            canvas, origin_column, garbage_frame, garbage_speed
        )
        coroutines.append(garbage_coroutine)
        ticks_lower_increment = 0 if ticks_lower <= 1 else 1
        ticks_upper_increment = 0 if ticks_upper <= 1 else 1
        random_ticks = random.randint(ticks_lower, ticks_upper)
        await sleep(random_ticks)
        ticks_lower -= ticks_lower_increment
        ticks_upper -= ticks_upper_increment


async def animate_spaceship():
    global spaceship_frame
    while True:
        await asyncio.sleep(0)
        spaceship_frame = rocket_frame_1
        await asyncio.sleep(0)
        spaceship_frame = rocket_frame_2


async def run_spaceship(canvas, row, column):
    global coroutines
    global year
    window_height, window_width = canvas.getmaxyx()
    row_speed = column_speed = 0
    year_increment = 0.1
    while True:
        row_direction, column_direction, shoot = read_controls(canvas)
        row_speed_update, column_speed_update = update_speed(
            row_speed, column_speed, row_direction, column_direction
        )

        flame_length = 3
        if (row <= 0 and row_direction == -1) or (row >= window_height - SHIP_LENGTH + flame_length and row_direction == 1):
            row_speed_update = 0
        row += row_speed_update

        if (column <= 0 and column_direction == -1) or (column >= window_width - SHIP_WIDTH and column_direction == 1):
            column_speed_update = 0
        column += column_speed_update
        
        year += year_increment
        for obstacle in obstacles:
            if obstacle.has_collision(row, column):
                explosion_row = row + SHIP_LENGTH // 2
                explosion_column = column + SHIP_WIDTH // 2
                await explode(canvas, explosion_row, explosion_column)
                await show_gameover(canvas, window_height, window_width)
                year_increment = 0
                return
        if shoot:
            column_correction = 2
            bang = shot(canvas, row, column + column_correction)
            coroutines.append(bang)
        draw_frame(canvas, row, column, spaceship_frame)
        last_frame = spaceship_frame
        await asyncio.sleep(0)
        draw_frame(canvas, row, column, last_frame, negative=True)
        draw_frame(canvas, row, column, spaceship_frame)
        last_frame = spaceship_frame
        draw_frame(canvas, row, column, last_frame, negative=True)


async def fly_garbage(canvas, column, garbage_frame, speed=0.5):
    """Animate garbage, flying from top to bottom. Сolumn position will stay
    same, as specified on start."""
    rows_number, columns_number = canvas.getmaxyx()
    column = max(column, 0)
    column = min(column, columns_number - 1)
    row = 0
    garbage_rows_num, garbage_columns_num = get_frame_size(garbage_frame)
    obstacle = Obstacle(row, column, garbage_rows_num, garbage_columns_num)
    obstacles.append(obstacle)
    while row < rows_number:
        if obstacle in obstacles_in_last_collisions:
            obstacles.remove(obstacle)
            obstacles_in_last_collisions.remove(obstacle)
            explosion_row = row + garbage_rows_num // 2
            explosion_column = column + garbage_columns_num // 2
            await explode(canvas, explosion_row, explosion_column)
            return
        obstacle.row = row
        draw_frame(canvas, row, column, garbage_frame)
        await asyncio.sleep(0)
        draw_frame(canvas, row, column, garbage_frame, negative=True)
        row += speed
    else:
        obstacles.remove(obstacle)


async def shot(canvas, start_row, start_column, rows_speed=-0.3, columns_speed=0):
    """Display animation of gun shot. Direction and speed can be specified."""
    row, column = start_row, start_column
    canvas.addstr(round(row), round(column), '*')
    await asyncio.sleep(0)
    canvas.addstr(round(row), round(column), 'O')
    await asyncio.sleep(0)
    canvas.addstr(round(row), round(column), ' ')
    row += rows_speed
    column += columns_speed
    symbol = '-' if columns_speed else '|'
    rows, columns = canvas.getmaxyx()
    max_row, max_column = rows - 1, columns - 1
    curses.beep()

    while 0 < row < max_row and 0 < column < max_column:
        canvas.addstr(round(row), round(column), symbol)
        await asyncio.sleep(0)
        for obstacle in obstacles:
            if obstacle.has_collision(row, column):
                obstacles_in_last_collisions.append(obstacle)
                return
        canvas.addstr(round(row), round(column), ' ')
        row += rows_speed
        column += columns_speed


async def draw_border(canvas):
    while True:
        canvas.border()
        await asyncio.sleep(0)


async def show_year(canvas):
    global year
    window_height, window_width = canvas.getmaxyx()
    year_height = 3
    year_width = 6
    year_canvas = canvas.derwin(
        year_height,
        year_width,
        window_height - year_height,
        window_width - year_width
    )
    pos_in_year_canvas_y, pos_in_year_canvas_x = 1, 1
    while True:
        draw_frame(
            year_canvas, pos_in_year_canvas_y, pos_in_year_canvas_x, str(year)
        )
        year_canvas.border()
        await asyncio.sleep(0)


def draw(canvas):
    global coroutines
    curses.curs_set(False)
    canvas.nodelay(True)
    window_height, window_width = canvas.getmaxyx()
    border = draw_border(canvas)
    coroutines.append(border)
    year_display = show_year(canvas)
    coroutines.append(year_display)
    stars = create_stars(canvas)
    coroutines.extend(stars)
    initial_y = window_height // 2 - SHIP_LENGTH // 2
    initial_x = window_width // 2 - SHIP_WIDTH // 2
    animated_spaceship_frames = animate_spaceship()
    coroutines.append(animated_spaceship_frames)
    ship = run_spaceship(canvas, initial_y, initial_x)
    coroutines.append(ship)
    garbage = fill_orbit_with_garbage(canvas)
    coroutines.append(garbage)
    bounding_boxes = show_obstacles(canvas, obstacles)
    coroutines.append(bounding_boxes)
    while True:
        for coroutine in coroutines[:]:
            try:
                coroutine.send(None)
            except StopIteration:
                coroutines.remove(coroutine)
        canvas.refresh()
        time.sleep(1 * TIC_TIMEOUT)


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)
