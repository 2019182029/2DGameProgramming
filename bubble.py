from pico2d import *
from ball import Score

import play_mode

class Bubble:
    def __init__(self, image):
        self.image = load_image(image)
        self.x, self.y = 825, 725
        self.frame = 0
        self.sound = load_wav('resource\\objects\\referee.wav')
        self.sound.set_volume(64)
        self.sound_play = True

    def draw(self):
        if play_mode.ball.state_machine.cur_state == Score:
            self.image.clip_draw(self.frame * 52, 0, 52, 30, self.x, self.y, 52 * 5, 30 * 5)
            if self.sound_play:
                self.sound.play()
                self.sound_play = False
        else: self.sound_play = True

    def update(self):
        pass