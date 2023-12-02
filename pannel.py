from pico2d import *

class Pannel:
    def __init__(self, image, x, y, width, height, music = None):
        self.image = load_image(image)
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.music = music
        if self.music != None:
            self.bgm = load_music(self.music)
            self.bgm.set_volume(16)
            self.bgm.play()

    def draw(self):
        self.image.draw(self.x, self.y, self.width, self.height)

    def update(self):
        pass