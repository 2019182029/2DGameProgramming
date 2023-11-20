from pico2d import *

import game_world
import select_mode
import game_framework

from player_1 import Player
from court import Court
from ball import Ball
from referee import Referee


def init():
    global court
    global player_1, player_2
    global ball
    global referee

    court = Court()
    game_world.add_object(court)

    player_1 = Player(500, 150, 'resource\\tennis_player_1.png')
    player_2 = Player(500, 750, 'resource\\tennis_player_2.png')
    game_world.add_object(player_1, 3)
    game_world.add_object(player_2, 3)

    ball = Ball()
    game_world.add_object(ball, 2)

    referee = Referee()
    game_world.add_object(referee, 1)

    game_world.add_collision_pair('player:ball', player_1, None)
    game_world.add_collision_pair('player:ball', player_2, None)
    game_world.add_collision_pair('player:ball', None, ball)



def finish():
    game_world.clear()


def update():
    game_world.update()
    game_world.handle_collision()
    referee.setheading(ball)


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()
    # delay(0.1)


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            # game_framework.change_mode(select_mode)
            game_framework.quit()
        else:
            player_1.handle_event(event)


def pause():
    pass


def resume():
    pass
