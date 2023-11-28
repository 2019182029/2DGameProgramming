from pico2d import *

import game_framework
import play_mode
import title_mode

mode_selection = {'vs_CPU': 470, 'vs_Player': 358}


def init():
    global image
    global arrow
    global pannel_cpu
    global pannel_player
    global arrow_y

    image = load_image('resource\\selection.png')
    arrow = load_image('resource\\selection_arrow.png')
    pannel_cpu = load_image('resource\\pannel_cpu.png')
    pannel_player = load_image('resource\\pannel_player.png')

    arrow_y = mode_selection['vs_CPU']


def finish():
    pass


def update():
    pass


def draw():
    clear_canvas()
    image.draw(250 * 2, 225 * 2, 250 * 4, 225 * 4)
    if arrow_y == mode_selection['vs_CPU']:
        pannel_cpu.draw(250 * 2 + 10, 225 * 2, 250 * 4, 225 * 4)
        pannel_player.draw(250 * 2, 225 * 2, 250 * 4, 225 * 4)
    else :
        pannel_cpu.draw(250 * 2, 225 * 2, 250 * 4, 225 * 4)
        pannel_player.draw(250 * 2 + 10, 225 * 2, 250 * 4, 225 * 4)
    arrow.draw(75, arrow_y, 50, 50)
    update_canvas()


def handle_events():
    global arrow_y

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_DOWN) and arrow_y == mode_selection['vs_CPU']:
            arrow_y = mode_selection['vs_Player']
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_UP) and arrow_y == mode_selection['vs_Player']:
            arrow_y = mode_selection['vs_CPU']
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE) and arrow_y == mode_selection['vs_Player']:
            game_framework.change_mode(play_mode)
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            game_framework.change_mode(title_mode)