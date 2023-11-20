from pico2d import *


class Court:
    def __init__(self, image):
        self.image = load_image(image)

    def update(self):
        pass

    def draw(self):
        self.image.draw(250 * 2, 225 * 2, 250 * 4, 225 * 4)
