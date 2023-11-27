from pico2d import *


class Background:
    def __init__(self, image):
        self.image = load_image(image)

    def update(self):
        pass

    def draw(self):
        self.image.draw(250 * 2, 225 * 2, 250 * 4, 225 * 4)
        # draw_rectangle(*self.get_bb())

    def get_bb(self):
        return 0, 800, 1000, 950

    def handle_collision(self, group, other):
        pass
