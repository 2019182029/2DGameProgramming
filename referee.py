from pico2d import *
import game_framework


class Referee:
    def __init__(self):
        self.x, self.y = 900, 550
        self.frame = 0
        self.image = load_image('resource\\referee.png')

    def update(self):
        pass

    def draw(self):
        self.image.clip_draw(self.frame * 17, 0, 17, 44, self.x, self.y, 17 * 5, 44 * 5)
