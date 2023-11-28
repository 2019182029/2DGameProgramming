from pico2d import load_image

class Pannel:
    def __init__(self, image, x, y):
        self.image = load_image(image)
        self.x, self.y = x, y

    def draw(self):
        self.image.draw(self.x, self.y, 250 * 4, 225 * 4)

    def update(self):
        pass