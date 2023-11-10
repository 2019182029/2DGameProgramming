from pico2d import *
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
        self.x, self.y = 500, 100
        self.frame = 0
        self.xdir, self.ydir = 0, 0.5
        self.image = load_image('resource\\tennis_ball.png')

    def update(self):
        self.frame = (self.frame + FRAMES_PER_TIME * game_framework.frame_time * 0.25) % 6
        self.y += self.ydir * RUN_SPEED_PPS * game_framework.frame_time

    def draw(self):
        self.image.clip_draw(int(self.frame) * 7, 0, 7, 8, self.x, self.y, 50, 50)
