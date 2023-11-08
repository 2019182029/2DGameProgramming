import game_framework
import play_mode
import title_mode
from pico2d import *


def init():
    global image

    image = load_image('resource\\selection.png')


def finish():
    pass


def update():
    pass


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
            game_framework.change_mode(title_mode)
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
            game_framework.change_mode(play_mode)