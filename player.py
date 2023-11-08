from pico2d import *
from event import *

import game_world
import game_framework

# Player Run Speed
PIXEL_PER_METER = (10.0 / 0.06)
RUN_SPEED_KMPH = 10.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Player Action Speed
TIME_PER_ACTION = 0.25
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4
FRAMES_PER_TIME = ACTION_PER_TIME * FRAMES_PER_ACTION


class Idle:
    @staticmethod
    def enter(player, e):
        player.action = 1

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        pass

    @staticmethod
    def draw(player):
        player.image.clip_draw(int(player.frame) * 23, player.action * 40, 23, 40, player.x, player.y, 23 * 4, 40 * 4)


class Ready:

    @staticmethod
    def enter(player, e):
        player.frame = 0
        player.action = 0

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        pass

    @staticmethod
    def draw(player):
        player.image.clip_draw(int(player.frame) * 23, player.action * 40, 23, 40, player.x, player.y, 23 * 4, 40 * 4)


class RunX:
    @staticmethod
    def enter(player, e):
        player.action = 1
        if right_down(e) or left_up(e):
            player.xdir = 1
        elif left_down(e) or right_up(e):
            player.xdir = -1

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_TIME * game_framework.frame_time) % 4
        player.x += player.xdir * RUN_SPEED_PPS * game_framework.frame_time

    @staticmethod
    def draw(player):
        player.image.clip_draw(int(player.frame) * 23, player.action * 40, 23, 40, player.x, player.y, 23 * 4, 40 * 4)


class RunY:
    @staticmethod
    def enter(player, e):
        player.action = 1
        if up_down(e) or down_up(e):
            player.ydir = 1
        elif down_down(e) or up_up(e):
            player.ydir = -1

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_TIME * game_framework.frame_time) % 4
        player.y += player.ydir * RUN_SPEED_PPS * game_framework.frame_time

    @staticmethod
    def draw(player):
        player.image.clip_draw(int(player.frame) * 23, player.action * 40, 23, 40, player.x, player.y, 23 * 4, 40 * 4)


class RunXY:
    @staticmethod
    def enter(player, e):
        player.action = 1
        if right_down(e) or left_up(e):
            player.xdir = 1
        elif left_down(e) or right_up(e):
            player.xdir = -1
        if up_down(e) or down_up(e):
            player.ydir = 1
        elif down_down(e) or up_up(e):
            player.ydir = -1

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_TIME * game_framework.frame_time) % 4
        player.x += player.xdir * RUN_SPEED_PPS * game_framework.frame_time
        player.y += player.ydir * RUN_SPEED_PPS * game_framework.frame_time

    @staticmethod
    def draw(player):
        player.image.clip_draw(int(player.frame) * 23, player.action * 40, 23, 40, player.x, player.y, 23 * 4, 40 * 4)


class StateMachine:
    def __init__(self, player):
        self.player = player
        self.cur_state = Idle
        self.transitions = {
            Idle: {right_down: RunX, left_down: RunX, left_up: RunX, right_up: RunX,
                   up_down: RunY, down_down: RunY, up_up: RunY, down_up: RunY},
            RunX: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle,
                   up_down: RunXY, down_down: RunXY, up_up: RunXY, down_up: RunXY},
            RunY: {right_down: RunXY, left_down: RunXY, right_up: RunXY, left_up: RunXY,
                   up_down: Idle, down_down: Idle, up_up: Idle, down_up: Idle},
            RunXY: {right_down: RunY, left_down: RunY, right_up: RunY, left_up: RunY,
                    up_down: RunX, down_down: RunX, up_up: RunX, down_up: RunX},
            Ready: {}
        }

    def start(self):
        self.cur_state.enter(self.player, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.player)

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.player, e)
                self.cur_state = next_state
                self.cur_state.enter(self.player, e)
                return True
        return False

    def draw(self):
        self.cur_state.draw(self.player)


class Player:
    def __init__(self):
        self.x, self.y = 500, 150
        self.frame = 0
        self.action = 0
        self.face_dir = 1
        self.xdir, ydir = 0, 0
        self.image = load_image('resource\\tennis_player.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
