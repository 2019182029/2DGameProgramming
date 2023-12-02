from pico2d import *
from background import Background
from pannel import Pannel

import game_framework
import select_mode
import game_world
import time


def init():
    global title_menu
    global instruction
    global title_mode_start_time
    global instruction_display

    title_menu = Background('resource\\title_mode\\title_menu.png', music = 'resource\\title_mode\\title_mode.mp3')
    instruction = Pannel('resource\\title_mode\\title_instruction.png', 250 * 2, 225 * 2, 250 * 4, 225 * 4)

    game_world.add_object(title_menu)

    title_mode_start_time = time.time()
    instruction_display = True


def finish():
    game_world.clear()


def update():
    global title_mode_start_time
    global instruction_display

    if time.time() - title_mode_start_time > 1.0:
        instruction_display = True if instruction_display == False else False
        title_mode_start_time = time.time()

def draw():
    clear_canvas()
    game_world.render()
    if instruction_display: instruction.draw()
    update_canvas()


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            title_menu.bgm.pause()
            game_framework.change_mode(select_mode)
