from pico2d import *
from pannel import Pannel
from arrow import Arrow

import game_framework
import game_world
import play_mode
import title_mode

selection = {'CONTINUE': 225 * 2, 'RESTART': 225 * 2 - 71, 'RETURN_TO_TITLE': 225 * 2 - 142}

def init():
    global pannel
    global arrow
    global pannel_continue
    global pannel_restart
    global pannel_returnToTitle

    pannel = Pannel('resource\\pause.png', 250 * 2, 225 * 2, 750, 300)
    arrow = Arrow('resource\\pause_arrow.png', 250 * 2, 225 * 2, 750, 300)
    pannel_continue = Pannel('resource\\pannel_continue.png', 250 * 2, 225 * 2, 750, 300)
    pannel_restart = Pannel('resource\\pannel_restart.png', 250 * 2, 225 * 2, 750, 300)
    pannel_returnToTitle = Pannel('resource\\pannel_return_to_title.png', 250 * 2, 225 * 2, 750, 300)

    game_world.add_object(pannel, 4)
    game_world.add_object(arrow, 4)
    game_world.add_object(pannel_continue, 4)
    game_world.add_object(pannel_restart, 4)
    game_world.add_object(pannel_returnToTitle, 4)


def finish():
    game_world.remove_object(pannel)
    game_world.remove_object(arrow)
    game_world.remove_object(pannel_continue)
    game_world.remove_object(pannel_restart)
    game_world.remove_object(pannel_returnToTitle)


def update():
    pass


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
                game_framework.pop_mode()
            elif event.key == SDLK_DOWN and arrow.y != selection['RETURN_TO_TITLE']:
                arrow.y -= 71
            elif event.key == SDLK_UP and arrow.y != selection['CONTINUE']:
                arrow.y += 71
            elif event.key == SDLK_SPACE:
                if arrow.y == selection['CONTINUE']:
                    game_framework.pop_mode()
                elif arrow.y == selection['RESTART']:
                    game_framework.pop_mode()
                    game_framework.change_mode(play_mode)
                else:
                    game_framework.pop_mode()
                    game_framework.change_mode(title_mode)

