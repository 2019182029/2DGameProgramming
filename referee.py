from pico2d import *
import game_framework

direction = {'Middle': 0, 'Down': 1, 'Up': 2}

class Referee:
    def __init__(self):
        self.x, self.y = 900, 550
        self.frame = direction['Middle']
        self.image = load_image('resource\\objects\\referee.png')

    def update(self):
        pass

    def draw(self):
        self.image.clip_draw(self.frame * 17, 0, 17, 44, self.x, self.y, 17 * 5, 44 * 5)

    def setheading(self, ball):
        if ball.y <= 400: self.frame = direction['Down']
        elif ball.y > 700: self.frame = direction['Up']
        else: self.frame = direction['Middle']
