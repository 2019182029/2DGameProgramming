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
        if player.action == actions['Swing']: return

        if player.face_dir == 'Right' or player.face_dir == 'Left': player.action = actions['Stand']
        else: player.action = actions['Idle']

    @staticmethod
    def exit(player, e):
        if space_down(e): player.swing()

    @staticmethod
    def do(player):
        if player.action == actions['Swing']:
            if player.frame + FRAMES_PER_TIME * game_framework.frame_time >= 4:
                if player.x > COURT_WIDTH // 2 and player.swing_dir == 'Left':
                    player.face_dir = 'Right'
                    player.action = actions['Stand']
                elif player.x <= COURT_WIDTH // 2 and player.swing_dir == 'Right':
                    player.face_dir = 'Left'
                    player.action = actions['Stand']
                else: player.action = actions['Idle']

            if int(player.frame) == 2:
                if player.swing_dir == 'Left':
                    player.collision_xy = (player.x + 20, player.y - 10, player.x + 60, player.y + 10)
                elif player.swing_dir == 'Right':
                    player.collision_xy = (player.x - 60, player.y - 10, player.x - 20, player.y + 10)

            player.frame = (player.frame + FRAMES_PER_TIME * game_framework.frame_time) % 4
        else:
            player.collision_xy = (0, 0, 0, 0)
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


class Run:
    @staticmethod
    def enter(player, e):
        if right_down(e) or left_up(e):
            player.xdir += 1
            player.swing_dir = 'Right'
        elif left_down(e) or right_up(e):
            player.xdir -= 1
            player.swing_dir = 'Left'
        if up_down(e) or down_up(e): player.ydir += 1
        elif down_down(e) or up_up(e): player.ydir -= 1

        player.dir = math.atan2(player.ydir, player.xdir)

        if player.action == actions['Swing']: return
        player.action = actions['Run']

        if player.xdir == 1: player.face_dir = 'Right'
        elif player.xdir == -1: player.face_dir = 'Left'

    @staticmethod
    def exit(player, e):
        # if player.xdir == 0: player.face_dir = 'Middle'
        if space_down(e): player.swing(); print('1')

    @staticmethod
    def do(player):
        if player.action == actions['Swing']:
            if player.frame + FRAMES_PER_TIME * game_framework.frame_time >= 4: player.action = actions['Run']

            if int(player.frame) == 2:
                if player.swing_dir == 'Right':
                    player.collision_xy = (player.x + 20, player.y - 10, player.x + 60, player.y + 10)
                elif player.swing_dir == 'Left':
                    player.collision_xy = (player.x - 60, player.y - 10, player.x - 20, player.y + 10)

        if player.xdir == 0 and player.ydir == 0 and not player.action == actions['Swing']:
            player.state_machine.handle_event(('CHA_STOPPED', None))

        player.frame = (player.frame + FRAMES_PER_TIME * game_framework.frame_time) % 4
        if not player.xdir == 0: player.x += RUN_SPEED_PPS * math.cos(player.dir) * game_framework.frame_time
        player.y += RUN_SPEED_PPS * math.sin(player.dir) * game_framework.frame_time

    @staticmethod
    def draw(player):
        if player.face_dir == 'Right': player_draw(player)
        elif player.face_dir == 'Left': player_composite_draw(player)


class StateMachine:
    def __init__(self, player):
        self.player = player
        self.cur_state = Idle
        self.transitions = {
            Idle: {right_down: Run, left_down: Run, left_up: Run, right_up: Run,
                   up_down: Run, down_down: Run, up_up: Run, down_up: Run, space_down: Idle},
            Run: {right_down: Run, left_down: Run, right_up: Run, left_up: Run,
                  up_down: Run, down_down: Run, up_up: Run, down_up: Run, cha_stopped: Idle, space_down: Run}
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
        self.collision_xy = (0, 0, 0, 0)

        self.frame = 0
        self.action = 0

        self.dir = 0
        self.xdir, self.ydir = 0, 0
        self.face_dir = 'Middle'
        self.swing_dir = 'Right'

        self.image = load_image('resource\\tennis_player.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def swing(self):
        self.frame = 0
        self.action = actions['Swing']
        self.collision_xy = (0, 0, 0, 0)

        if self.face_dir == 'Middle': self.swing_dir = 'Left' if self.x > COURT_WIDTH // 2 else 'Right'

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.collision_xy

    def handle_collision(self, group, other):
        pass