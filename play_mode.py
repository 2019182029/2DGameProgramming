from pico2d import *

import game_world
import select_mode
import game_framework

from player import Player
from court import Court


def init():
    global court
    global player

    court = Court()
    game_world.add_object(court)

    player = Player()
    game_world.add_object(player, 1)


def finish():
    game_world.clear()


def update():
    game_world.update()


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
