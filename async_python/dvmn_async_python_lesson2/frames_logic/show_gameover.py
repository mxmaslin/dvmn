import asyncio
from curses_tools import draw_frame, get_frame_size

gameover = """
   _____                         ____                 
  / ____|                       / __ \                
 | |  __  __ _ _ __ ___   ___  | |  | |_   _____ _ __ 
 | | |_ |/ _` | '_ ` _ \ / _ \ | |  | \ \ / / _ \ '__|
 | |__| | (_| | | | | | |  __/ | |__| |\ V /  __/ |   
  \_____|\__,_|_| |_| |_|\___|  \____/  \_/ \___|_|   
                                                      
"""


async def show_gameover(canvas, window_width, window_height):
    gameover_offset_x, gameover_offset_y = get_frame_size(gameover)
    while True:
        draw_frame(
            canvas,
            window_width//2 - gameover_offset_x//2,
            window_height//2 - gameover_offset_y//2,
            gameover
        )
        await asyncio.sleep(0)
