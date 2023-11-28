from pico2d import load_image

class Arrow:
    def __init__(self, image, x, y, width, height):
        self.image = load_image(image)
        self.x, self.y = x, y
        self.width, self.height = width, height

    def draw(self):
        self.image.draw(self.x, self.y, self.width, self.height)

    def update(self):
        pass