from pico2d import *
from pannel import Pannel

import game_framework
import game_world
import pause_mode
import play_mode


def init():
    global score_board
    global score_mode_start_time

    score_board = Pannel('resource\\score_mode\\score_board.png', 250 * 2, 225 * 2, 250 * 4, 225 * 4)
    score_mode_start_time = get_time()

    game_world.add_object(score_board, 4)

def finish():
    game_world.remove_object(score_board)


def update():
    if (get_time() - score_mode_start_time > 2):
        game_framework.pop_mode()
        game_framework.change_mode(play_mode)


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.push_mode(pause_mode)


def pause():
    pass


def resume():
    pass
