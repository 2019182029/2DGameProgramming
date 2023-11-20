from pico2d import *
import random
import game_framework

PIXEL_PER_METER = (10.0 / 0.06)
RUN_SPEED_KMPH = 10.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 6
FRAMES_PER_TIME = ACTION_PER_TIME * FRAMES_PER_ACTION


class Ball:
    def __init__(self):
        self.x, self.y = 500, 250
        self.frame = 1
        self.frame_index = 0
        self.xdir, self.ydir = 0, 0
        self.image = load_image('resource\\tennis_ball.png')

    def update(self):
        self.x += self.xdir * RUN_SPEED_PPS * game_framework.frame_time
        self.y += self.ydir * RUN_SPEED_PPS * game_framework.frame_time

        if self.x >= 750: self.xdir *= -1.0
        elif self.x <= 250: self.xdir *= -1.0
        if self.y >= 950: self.ydir *= -1.0
        elif self.y <= 0: self.ydir *= -1.0

    def draw(self):
        self.image.clip_draw(int(self.frame) * 7, 0, 7, 8, self.x, self.y, 50, 50)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 10, self.y - 12, self.x + 16, self.y + 10

    def handle_collision(self, group, other):
        if group == 'player:ball':
            # self.xdir = random.randint(-50, 50) / 100
            self.ydir = 1 if self.ydir == 0 else self.ydir * -1

