from pico2d import *

import game_world


def handle_events():
    global running

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False


def create_world():
    global running

    running = True


open_canvas()
create_world()

while running:
    handle_events()
    game_world.update()
    clear_canvas()
    game_world.render()
    update_canvas()
    delay(0.01)

close_canvas()
