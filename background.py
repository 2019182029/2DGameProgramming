from pico2d import *


class Background:
    def __init__(self, image, bb = None):
        self.image = load_image(image)
        self.bb = bb

    def update(self):
        pass

    def draw(self):
        self.image.draw(250 * 2, 225 * 2, 250 * 4, 225 * 4)
        # draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.bb

    def handle_collision(self, group, other):
        pass
