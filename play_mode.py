from pico2d import *

import game_world
import selection_mode
import game_framework


def init():
    global image

    image = load_image('playground.png')


def finish():
    game_world.clear()


def update():
    game_world.update()


def draw():
    clear_canvas()
    image.draw(250, 225, 502, 450)
    update_canvas()
    delay(0.01)


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(selection_mode)


def pause():
    pass


def resume():
    pass
