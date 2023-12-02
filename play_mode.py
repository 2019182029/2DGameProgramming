from pico2d import *

import game_world
import select_mode
import pause_mode
import game_framework

from player_1 import Player as P1
from player_2 import Player as P2
from background import Background
from ball import Ball
from referee import Referee
from shadow import Shadow
from bubble import Bubble

serve = 'player_1'

def init():
    global court, net, pannel
    global player_1, player_2
    global ball, shadow
    global referee
    global bubble

    court = Background('resource\\play_mode\\court.png')
    net = Background('resource\\play_mode\\net.png')
    pannel = Background('resource\\play_mode\\pannel.png', (0, 800, 1000, 950))
    game_world.add_object(court)
    game_world.add_object(net, 2)
    game_world.add_object(pannel)

    player_1 = P1(500, 150, 'resource\\play_mode\\tennis_player_1.png')
    player_2 = P2(500, 800, 'resource\\play_mode\\tennis_player_2.png')
    game_world.add_object(player_1, 4)
    game_world.add_object(player_2, 1)

    ball = Ball()
    shadow = Shadow()
    game_world.add_object(ball, 3)
    game_world.add_object(shadow, 2)

    referee = Referee('resource\\objects\\referee.png')
    bubble = Bubble('resource\\objects\\speech_bubble.png')
    game_world.add_object(referee, 2)
    game_world.add_object(bubble, 4)

    game_world.add_collision_pair('ball:pannel', None, pannel)
    game_world.add_collision_pair('ball:pannel', ball, None)

    game_world.add_collision_pair('player:ball', player_1, None)
    game_world.add_collision_pair('player:ball', player_2, None)
    game_world.add_collision_pair('player:ball', None, ball)


def finish():
    global serve

    game_world.clear()
    serve = 'player_2' if serve == 'player_1' else 'player_1'


def update():
    game_world.handle_collision()
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
            game_framework.push_mode(pause_mode)
        else:
            player_1.handle_event(event)
            player_2.handle_event(event)
            ball.handle_event(event)


def pause():
    pass


def resume():
    pass
