from pico2d import *
from pannel import Pannel

import game_framework
import game_world
import pause_mode
import play_mode
import title_mode
import score_mode

def init():
    global game_set
    global game_mode_start_time

    game_set = Pannel('resource\\score_mode\\game_set.png', 500, 300, 900, 250,
                      'resource\\score_mode\\game_set.mp3')

    game_world.add_object(game_set, 5)

    game_mode_start_time = get_time()
    play_mode.serve = 'player_2'

def finish():
    pass


def update():
    if (get_time() - game_mode_start_time > 13):
        score_mode.p1_score_num, score_mode.p2_score_num = 0, 0
        while game_framework.stack[-1] != play_mode: game_framework.pop_mode()
        game_framework.change_mode(title_mode)


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
            if event.key == SDLK_SPACE:
                game_set.bgm.pause()
                while game_framework.stack[-1] != play_mode: game_framework.pop_mode()
                game_framework.change_mode(title_mode)


def pause():
    pass


def resume():
    pass
