from pico2d import *
from ball import Rally

import play_mode


class Shadow:
    def __init__(self):
        self.image = load_image('resource\\objects\\tennis_ball_shadow.png')

    def update(self):
        pass

    def draw(self):
        if play_mode.ball.state_machine.cur_state == Rally:
            self.image.clip_draw(0, play_mode.ball.frame * 6, 6, 6, play_mode.ball.x, play_mode.ball.y, 25, 25)
