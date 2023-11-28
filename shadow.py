from pico2d import *
import play_mode


class Shadow:
    def __init__(self):
        self.image = load_image('resource\\objects\\tennis_ball_shadow.png')

    def update(self):
        pass

    def draw(self):
        self.image.clip_draw(0, play_mode.ball.frame * 6, 6, 6, play_mode.ball.x, play_mode.ball.y, 25, 25)
