from pico2d import *

import game_world
import select_mode
import game_framework

from player import Player
from court import Court
from ball import Ball
from referee import Referee


def init():
    global court
    global player
    global ball
    global referee

    court = Court()
    game_world.add_object(court)

    player = Player()
    game_world.add_object(player, 3)

    ball = Ball()
    game_world.add_object(ball, 2)

    referee = Referee()
    game_world.add_object(referee, 1)



def finish():
    game_world.clear()


def update():
    game_world.update()
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
            player.handle_event(event)


def pause():
    pass


def resume():
    pass
