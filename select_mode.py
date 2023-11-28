from pico2d import *

import game_world
from background import Background
from pannel import Pannel
from arrow import Arrow

import game_framework
import play_mode
import title_mode

mode_selection = {'PVE': 470, 'PVP': 358}


def init():
    global background
    global arrow
    global pannel_1
    global pannel_2

    background = Background('resource\\selection.png')
    arrow = Arrow('resource\\selection_arrow.png', 75, mode_selection['PVE'], 50, 50)
    pannel_1 = Pannel('resource\\pannel_cpu.png', 250 * 2, 225 * 2, 250 * 4, 225 * 4)
    pannel_2 = Pannel('resource\\pannel_player.png', 250 * 2, 225 * 2, 250 * 4, 225 * 4)

    game_world.add_object(background)
    game_world.add_object(arrow, 1)
    game_world.add_object(pannel_1, 1)
    game_world.add_object(pannel_2, 1)


def finish():
    game_world.clear()


def update():
    if arrow.y == mode_selection['PVE']: pannel_1.x = 250 * 2 + 10; pannel_2.x = 250 * 2
    else: pannel_1.x = 250 * 2; pannel_2.x = 250 * 2 + 10


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_DOWN) and arrow.y == mode_selection['PVE']:
            arrow.y = mode_selection['PVP']
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_UP) and arrow.y == mode_selection['PVP']:
            arrow.y = mode_selection['PVE']
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE) and arrow.y == mode_selection['PVP']:
            game_framework.change_mode(play_mode)
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            game_framework.change_mode(title_mode)