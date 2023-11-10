from pico2d import *
from event_check import *

import game_world
import game_framework

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

actions = {'Idle': 0, 'Run': 1, 'Stand': 2, 'Swing': 3}


def player_composite_draw(player):
    player.image.clip_composite_draw(
        int(player.frame) * 23, player.action * 40, 23, 40, 0, 'h', player.x, player.y, 23 * 4, 40 * 4 )

def player_draw(player):
    player.image.clip_draw(
        int(player.frame) * 23, player.action * 40, 23, 40, player.x, player.y, 23 * 4, 40 * 4)

class Idle:
    @staticmethod
    def enter(player, e):
        if player.face_dir == 'Right' or player.face_dir == 'Left': player.action = actions['Stand']
        else: player.action = actions['Idle']

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_TIME * game_framework.frame_time * 0.25) % 4

    @staticmethod
    def draw(player):
        if player.action == actions['Idle']:
            if player.x > COURT_WIDTH // 2:
                player.image.clip_composite_draw(int(player.frame) * 23, player.action * 40, 23, 40, 0, 'h',
                                                 player.x, player.y, 23 * 4, 40 * 4 + 17)
            else:
                player.image.clip_draw(int(player.frame) * 23, player.action * 40, 23, 40,
                                       player.x, player.y, 23 * 4, 40 * 4 + 17)
        elif player.face_dir == 'Left': player_composite_draw(player)
        else: player_draw(player)


class Swing:
    @staticmethod
    def enter(player, e):
        player.frame = 0
        player.action = actions['Swing']

    @staticmethod
    def exit(player, e):
        if player.x > COURT_WIDTH // 2 and player.swing_dir == 'Right': return
        elif player.x <= COURT_WIDTH // 2 and player.swing_dir == 'Left': return
        player.face_dir = 'Middle'

    @staticmethod
    def do(player):
        if player.frame + FRAMES_PER_TIME * game_framework.frame_time >= 4:
            player.state_machine.handle_event(('TIME_OUT', None))
        player.frame = (player.frame + FRAMES_PER_TIME * game_framework.frame_time) % 4

    @staticmethod
    def draw(player):
        if player.swing_dir == 'Left': player_composite_draw(player)
        else: player_draw(player)


class RunX:
    @staticmethod
    def enter(player, e):
        player.action = actions['Run']

        if right_down(e) or left_up(e):
            player.xdir = 1
            player.face_dir = 'Right'
            player.swing_dir = 'Right'
        elif left_down(e) or right_up(e):
            player.xdir = -1
            player.face_dir = 'Left'
            player.swing_dir = 'Left'

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_TIME * game_framework.frame_time) % 4
        player.x += player.xdir * RUN_SPEED_PPS * game_framework.frame_time

    @staticmethod
    def draw(player):
        if player.face_dir == 'Right': player_draw(player)
        elif player.face_dir == 'Left': player_composite_draw(player)


class RunY:
    @staticmethod
    def enter(player, e):
        player.action = actions['Run']

        if player.face_dir == 'Middle': player.face_dir = 'Right'

        if up_down(e) or down_up(e): player.ydir = 1
        elif down_down(e) or up_up(e): player.ydir = -1

        if player.xdir > 0: player.face_dir = 'Right'
        elif player.xdir < 0: player.face_dir = 'Left'

    @staticmethod
    def exit(player, e):
        player.face_dir = 'Middle'

    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_TIME * game_framework.frame_time) % 4
        player.y += player.ydir * RUN_SPEED_PPS * game_framework.frame_time

    @staticmethod
    def draw(player):
        if player.face_dir == 'Right': player_draw(player)
        elif player.face_dir == 'Left': player_composite_draw(player)


class RunXY:
    @staticmethod
    def enter(player, e):
        player.action = actions['Run']

        if right_down(e) or left_up(e):
            player.xdir = 1
            player.face_dir = 'Right'
            player.swing_dir = 'Right'
        elif left_down(e) or right_up(e):
            player.xdir = -1
            player.face_dir = 'Left'
            player.swing_dir = 'Left'

        if up_down(e) or down_up(e): player.ydir = 1
        elif down_down(e) or up_up(e): player.ydir = -1

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
        if player.face_dir == 'Right': player_draw(player)
        elif player.face_dir == 'Left': player_composite_draw(player)


class StateMachine:
    def __init__(self, player):
        self.player = player
        self.cur_state = Idle
        self.transitions = {
            Idle: {right_down: RunX, left_down: RunX, left_up: RunX, right_up: RunX,
                   up_down: RunY, down_down: RunY, up_up: RunY, down_up: RunY, space_down: Swing},
            RunX: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle,
                   up_down: RunXY, down_down: RunXY, up_up: RunXY, down_up: RunXY},
            RunY: {right_down: RunXY, left_down: RunXY, right_up: RunXY, left_up: RunXY,
                   up_down: Idle, down_down: Idle, up_up: Idle, down_up: Idle},
            RunXY: {right_down: RunY, left_down: RunY, right_up: RunY, left_up: RunY,
                    up_down: RunX, down_down: RunX, up_up: RunX, down_up: RunX},
            Swing: {time_out: Idle}
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
        self.face_dir = 'Middle'
        self.swing_dir = 'Right'
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
