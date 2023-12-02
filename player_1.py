from pico2d import *
from event_check import *

import play_mode
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

actions = {'Idle': 0, 'Run': 1, 'Stand': 2, 'Swing': 3, 'Serve_Ready': 4, 'Serve_Do': 5, 'Serve_Swing': 6}


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
                if player.x > COURT_WIDTH // 2 and player.swing_dir == 'Right':
                    player.face_dir = 'Right'
                    player.action = actions['Stand']
                elif player.x <= COURT_WIDTH // 2 and player.swing_dir == 'Left':
                    player.face_dir = 'Left'
                    player.action = actions['Stand']
                else: player.action = actions['Idle']

            if int(player.frame) == 2:
                if player.swing_dir == 'Right':
                    player.collision_xy = (player.x, player.y - 25, player.x + 50, player.y + 25)
                elif player.swing_dir == 'Left':
                    player.collision_xy = (player.x - 50, player.y - 25, player.x, player.y + 25)

            player.frame = (player.frame + FRAMES_PER_TIME * game_framework.frame_time) % 4
        else:
            player.collision_xy = (0, 0, 0, 0)
            player.frame = (player.frame + FRAMES_PER_TIME * game_framework.frame_time * 0.25) % 4

    @staticmethod
    def draw(player):
        if player.action == actions['Idle']:
            if player.x > COURT_WIDTH // 2: player.composite_draw_player(23 * 4, 40 * 4 + 17)
            else: player.draw_player(23 * 4, 40 * 4 + 17)
        elif player.face_dir == 'Left': player.composite_draw_player()
        else: player.draw_player()


class Run:
    @staticmethod
    def enter(player, e):
        if right_down(e) or left_up(e): player.xdir += 1
        elif left_down(e) or right_up(e): player.xdir -= 1
        if up_down(e) or down_up(e): player.ydir += 1
        elif down_down(e) or up_up(e): player.ydir -= 1

        player.dir = math.atan2(player.ydir, player.xdir)

        if player.action == actions['Swing']: return
        player.action = actions['Run']

        if player.xdir == 1: player.swing_dir = player.face_dir = 'Right'
        elif player.xdir == -1: player.swing_dir = player.face_dir = 'Left'

    @staticmethod
    def exit(player, e):
        if space_down(e): player.swing()

    @staticmethod
    def do(player):
        if player.action == actions['Swing']:
            if player.frame + FRAMES_PER_TIME * game_framework.frame_time >= 4: player.action = actions['Run']

            if 2 <= int(player.frame) <= 3:
                if player.swing_dir == 'Right':
                    player.collision_xy = (player.x, player.y - 25, player.x + 50, player.y + 25)
                elif player.swing_dir == 'Left':
                    player.collision_xy = (player.x - 50, player.y - 25, player.x, player.y + 25)
        else: player.collision_xy = (0, 0, 0, 0)

        if player.xdir == 0 and player.ydir == 0 and not player.action == actions['Swing']:
            player.state_machine.handle_event(('CHA_STOPPED', None))

        player.frame = (player.frame + FRAMES_PER_TIME * game_framework.frame_time) % 4
        if not player.action == actions['Swing']:
            player.x += RUN_SPEED_PPS * math.cos(player.dir) * game_framework.frame_time
            player.y += RUN_SPEED_PPS * math.sin(player.dir) * game_framework.frame_time

    @staticmethod
    def draw(player):
        if player.face_dir == 'Right' or player.face_dir == 'Middle': player.draw_player()
        elif player.face_dir == 'Left': player.composite_draw_player()


class Serve_Ready:
    @staticmethod
    def enter(player, e):
        player.action = actions['Serve_Ready']

        if right_down(e) or left_up(e): player.xdir += 1
        elif left_down(e) or right_up(e): player.xdir -= 1

    @staticmethod
    def exit(player, e):
        if space_down(e): player.xdir = 0

    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_TIME * game_framework.frame_time) % 4
        player.x += player.xdir * RUN_SPEED_PPS * game_framework.frame_time

    @staticmethod
    def draw(player):
        player.draw_player(23 * 4, 40 * 4 + 17)


class Serve_Do:
    @staticmethod
    def enter(player, e):
        player.action = actions['Serve_Do']
        player.swing_dir = 'Right' if player.x >= 500 else 'Left'

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_TIME * game_framework.frame_time) % 4

    @staticmethod
    def draw(player):
        player.draw_player(23 * 4, 40 * 4 + 17)


class Serve_Swing:
    @staticmethod
    def enter(player, e):
        player.action = actions['Serve_Swing']
        player.frame = 0

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        if player.frame + FRAMES_PER_TIME * game_framework.frame_time > FRAMES_PER_ACTION:
            player.state_machine.handle_event(('GAME_START', None))
        player.frame = (player.frame + FRAMES_PER_TIME * game_framework.frame_time * 0.75) % 4
        if 1 <= int(player.frame) <= 2:
            player.collision_xy = (player.x, player.y + 50, player.x + 50, player.y + 100)

    @staticmethod
    def draw(player):
        player.draw_player(23 * 4, 40 * 4 + 17)


class StateMachine:
    def __init__(self, player):
        self.player = player
        self.cur_state = Serve_Ready if play_mode.serve == 'player_1' else Idle
        self.transitions = {
            Idle: {right_down: Run, left_down: Run, left_up: Run, right_up: Run,
                   up_down: Run, down_down: Run, up_up: Run, down_up: Run, space_down: Idle},
            Run: {right_down: Run, left_down: Run, right_up: Run, left_up: Run,
                  up_down: Run, down_down: Run, up_up: Run, down_up: Run, cha_stop: Idle, space_down: Run},
            Serve_Ready: {right_down: Serve_Ready, left_down: Serve_Ready, right_up: Serve_Ready, left_up: Serve_Ready,
                          space_down: Serve_Do},
            Serve_Do: {space_down: Serve_Swing},
            Serve_Swing: {game_start: Idle}
        }

    def start(self):
        self.cur_state.enter(self.player, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.player)
        self.player.x = clamp(50.0, self.player.x, 950.0)
        self.player.y = clamp(0.0, self.player.y, 530.0)

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
    def __init__(self, x, y, image):
        self.x, self.y = x, y
        self.collision_xy = (0, 0, 0, 0)

        self.frame = 0
        self.action = 0

        self.dir = 0
        self.xdir, self.ydir = 0, 0
        self.face_dir = 'Middle'
        self.swing_dir = 'Right'

        self.image = load_image(image)

        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def composite_draw_player(self, width = 23 * 4, height = 40 * 4):
        self.image.clip_composite_draw(
            int(self.frame) * 23, self.action * 40, 23, 40, 0, 'h', self.x, self.y, width, height)

    def draw_player(self, width = 23 * 4, height = 40 * 4):
        self.image.clip_draw(
            int(self.frame) * 23, self.action * 40, 23, 40, self.x, self.y, width, height)

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
        # draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.collision_xy

    def handle_collision(self, group, other):
        pass
