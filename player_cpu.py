from pico2d import *
from event_check import *
from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector

import play_mode
import game_world
import game_framework
import random

# Player Run Speed
PIXEL_PER_METER = (10.0 / 0.06)
RUN_SPEED_KMPH = 10.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Player Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4
FRAMES_PER_TIME = ACTION_PER_TIME * FRAMES_PER_ACTION

COURT_WIDTH = 1000
COURT_HEIGHT = 950

actions = {'Idle': 0, 'Run': 1, 'Stand': 2, 'Swing': 3, 'Serve_Ready': 4, 'Serve_Do': 5, 'Serve_Swing': 6}

class Player:
    def __init__(self, x, y, image):
        self.x, self.y = x, y
        self.collision_xy = (0, 0, 0, 0)

        self.frame = 0
        self.action = actions['Idle']

        self.dir = 0
        self.xdir, self.ydir = 0, 0
        self.face_dir = 'Middle'
        self.swing_dir = 'Right'

        self.image = load_image(image)

    def composite_draw_player(self, width = 23 * 4, height = 40 * 4):
        self.image.clip_composite_draw(
            int(self.frame) * 23, self.action * 40, 23, 40, 0, 'h', self.x, self.y, width, height)

    def draw_player(self, width = 23 * 4, height = 40 * 4):
        self.image.clip_draw(
            int(self.frame) * 23, self.action * 40, 23, 40, self.x, self.y, width, height)

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        self.bt.run()

    def draw(self):
        if self.face_dir == 'Right' or self.face_dir == 'Middle': self.draw_player()
        elif self.face_dir == 'Left': self.composite_draw_player()

    def handle_event(self, event):
        pass

    def get_bb(self):
        return self.collision_xy

    def handle_collision(self, group, other):
        pass

    def set_target_location(self, x, y):
        self.tx, self.ty = x, y
        return BehaviorTree.SUCCESS

    def move_slightly_to(self, tx, ty):
        self.dir = math.atan2(ty - self.y, tx - self.x)
        self.x += RUN_SPEED_PPS * math.cos(self.dir) * game_framework.frame_time
        self.y += RUN_SPEED_PPS * math.sin(self.dir) * game_framework.frame_time

    def distance_less_than(self, x1, y1, x2, y2, r):
        distance2 = (x1 - x2) ** 2 + (y1 - y2) ** 2
        return distance2 < (PIXEL_PER_METER * r) ** 2

    def should_serve(self):
        if play_mode.serve == 'player_2':
            self.action = actions['Serve_Ready']
            return BehaviorTree.SUCCESS
        else: return BehaviorTree.FAIL

    def set_random_location(self):
        self.tx, self.ty = random.randint(200, 800 + 1), 800
        return BehaviorTree.SUCCESS

    def move_to(self, r = 0.5):
        self.move_slightly_to(self.tx, self.ty)
        if self.distance_less_than(self.tx, self.ty, self.x, self.y, r): return BehaviorTree.SUCCESS
        else: return BehaviorTree.RUNNING

    def do_serve(self):
        self.frame = 0
        self.action = actions['Serve_Swing']
        if self.frame + FRAMES_PER_TIME * game_framework.frame_time > FRAMES_PER_ACTION: return BehaviorTree.SUCCESS
        else: return BehaviorTree.RUNNING
        # self.frame = (self.frame + FRAMES_PER_TIME * game_framework.frame_time * 0.75) % 4
        if 1 <= int(self.frame) <= 2:
            self.collision_xy = (self.x - 50, self.y + 50, self.x, self.y + 100)

    def is_ball_hitted(self):
        if play_mode.ball.last_hitted_by == 'player_1': return BehaviorTree.SUCCESS
        else: return BehaviorTree.FAIL

    def set_target_location(self):
        c = (650 - play_mode.ball.y) / (play_mode.ball.ydir * play_mode.ball.RUN_SPEED_PPS * game_framework.frame_time)
        self.tx = play_mode.ball.x + play_mode.ball.xdir * c
        self.ty = play_mode.ball.y + play_mode.ball.ydir * c
        return BehaviorTree.SUCCESS

    def is_ball_nearby(self, r):
        if self.distance_less_than(play_mode.ball.x, play_mode.ball.y, self.x, self.y, r): return BehaviorTree.SUCCESS
        else: return BehaviorTree.FAIL

    def do_swing(self):
        self.frame = 0
        self.action = actions['Swing']
        self.collision_xy = (0, 0, 0, 0)

        if self.face_dir == 'Middle': self.swing_dir = 'Left' if self.x > COURT_WIDTH // 2 else 'Right'

        if self.frame + FRAMES_PER_TIME * game_framework.frame_time >= 4:
            if self.x > COURT_WIDTH // 2 and self.swing_dir == 'Left':
                self.face_dir = 'Left'
                self.action = actions['Stand']
            elif self.x <= COURT_WIDTH // 2 and self.swing_dir == 'Right':
                self.face_dir = 'Right'
                self.action = actions['Stand']
            else: self.action = actions['Idle']
            return BehaviorTree.SUCCESS

        if int(self.frame) == 2:
            if self.swing_dir == 'Left':
                self.collision_xy = (self.x + 25, self.y - 75, self.x + 75, self.y - 25)
            elif self.swing_dir == 'Right':
                self.collision_xy = (self.x - 75, self.y - 75, self.x - 25, self.y - 25)

        # self.frame = (self.frame + FRAMES_PER_TIME * game_framework.frame_time) % 4
        return BehaviorTree.RUNNING

    def do_Idle(self):
        self.action = actions['Idle']
        # self.frame = (self.frame + FRAMES_PER_TIME * game_framework.frame_time) % 4
        return BehaviorTree.SUCCESS

    def build_behavior_tree(self):
        a1 = Action('Do serve', self.do_serve)
        a2 = Action('Set location', self.set_target_location)
        a3 = Action('Move to', self.move_to)
        a4 = Action('Do swing', self.do_swing)
        a5 = Action('Set random location', self.set_random_location)
        a6 = Action('Do Idle', self.do_Idle)

        c1 = Condition('Have to do serve?', self.should_serve)
        c2 = Condition('Is ball hitted by P1?', self.is_ball_hitted)
        c3 = Condition('Is ball nearby?', self.is_ball_nearby)

        SEQ_serve = Sequence('Serve', c1, a5, a3, a1)
        SEQ_move_to = Sequence('Move', a2, a3)
        SEQ_swing = Sequence('Swing', c3, a4)
        SEQ_move_and_swing = Sequence('Move and Swing', c2, SEQ_move_to, SEQ_swing)

        SEL_swing_or_do_idle = Selector('Swing or Do Idle', SEQ_move_and_swing, a6)
        SEL_serve_or_swing_or_do_idle = Selector('Serve or Swing or Do Idle', SEQ_serve, SEL_swing_or_do_idle)

        self.bt = BehaviorTree(SEL_serve_or_swing_or_do_idle)