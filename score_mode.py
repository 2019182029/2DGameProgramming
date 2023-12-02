from pico2d import *
from pannel import Pannel

import game_framework
import game_world
import pause_mode
import play_mode
import game_mode

score_images = {0: 'resource\\score_mode\\score_0.png',
               15: 'resource\\score_mode\\score_15.png',
               30: 'resource\\score_mode\\score_30.png',
               40: 'resource\\score_mode\\score_40.png',
               40 + 1: 'resource\\score_mode\\score_40.png'}

p1_scores, p2_scores = [0, 15, 30, 40, 40 + 1], [0, 15, 30, 40, 40 + 1]
p1_score_num, p2_score_num = 0, 0

def init():
    global score_board
    global score_mode_start_time
    global p1_score, p2_score
    global scores
    global game_set

    score_board = Pannel('resource\\score_mode\\score_board.png', 250 * 2, 225 * 2, 250 * 4, 225 * 4)

    p1_score = Pannel(score_images[p1_scores[p1_score_num]], 205, 665, 50, 25)
    p2_score = Pannel(score_images[p2_scores[p2_score_num]], 205, 610, 50, 25)

    game_world.add_object(score_board, 4)
    game_world.add_object(p1_score, 4)
    game_world.add_object(p2_score, 4)

    game_set = load_image('resource\\score_mode\\game_set.png')

    score_mode_start_time = get_time()

def finish():
    pass


def update():
    if (get_time() - score_mode_start_time > 2):
        game_framework.pop_mode()
        game_framework.change_mode(play_mode)
    # pass


def draw():
    clear_canvas()
    game_world.render()
    if p1_scores[p1_score_num] > 40 or p2_scores[p2_score_num] > 40: game_framework.push_mode(game_mode)
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
