from pico2d import *


class Court:
    def __init__(self):
        self.image = load_image('resource\\playground.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(250 * 2, 225 * 2, 250 * 4, 225 * 4)
