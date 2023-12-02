from pico2d import load_image
from ball import Score

import play_mode

class Bubble:
    def __init__(self, image):
        self.image = load_image(image)
        self.x, self.y = 825, 725
        self.frame = 0

    def draw(self):
        if play_mode.ball.state_machine.cur_state == Score:
            self.image.clip_draw(self.frame * 52, 0, 52, 30, self.x, self.y, 52 * 5, 30 * 5)

    def update(self):
        pass