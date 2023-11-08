import game_framework
import select_mode
import game_world
from pico2d import *


def init():
    global image

    image = load_image('resource\\title.png')


def finish():
    game_world.clear()


def update():
    game_world.update()


def draw():
    clear_canvas()
    image.draw(250 * 2, 225 * 2, 250 * 4, 225 * 4)
    update_canvas()


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            game_framework.change_mode(select_mode)
