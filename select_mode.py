from pico2d import *
from pannel import Pannel

import game_framework
import play_mode
import title_mode

mode_selection = {'PVE': 470, 'PVP': 358}


def init():
    global image
    global arrow
    global pannel_1
    global pannel_2
    global arrow_y

    image = load_image('resource\\selection.png')
    arrow = load_image('resource\\selection_arrow.png')
    pannel_1 = Pannel('resource\\pannel_cpu.png', 250 * 2, 225 * 2)
    pannel_2 = Pannel('resource\\pannel_player.png', 250 * 2, 225 * 2)

    arrow_y = mode_selection['PVE']


def finish():
    pass


def update():
    if arrow_y == mode_selection['PVE']: pannel_1.x = 250 * 2 + 10; pannel_2.x = 250 * 2
    else: pannel_1.x = 250 * 2; pannel_2.x = 250 * 2  + 10


def draw():
    clear_canvas()
    image.draw(250 * 2, 225 * 2, 250 * 4, 225 * 4)
    pannel_1.draw()
    pannel_2.draw()
    arrow.draw(75, arrow_y, 50, 50)
    update_canvas()


def handle_events():
    global arrow_y

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_DOWN) and arrow_y == mode_selection['PVE']:
            arrow_y = mode_selection['PVP']
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_UP) and arrow_y == mode_selection['PVP']:
            arrow_y = mode_selection['PVE']
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE) and arrow_y == mode_selection['PVP']:
            game_framework.change_mode(play_mode)
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            game_framework.change_mode(title_mode)