from pico2d import *
from event_check import *
from ball import Score
from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector

import play_mode
import game_world
import game_framework
import random
import ball

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
        if mouse_click(e): player.swing()

    @staticmethod
    def do(player):
        if player.action == actions['Swing']:
            if player.frame + FRAMES_PER_TIME * game_framework.frame_time >= 4:
                if player.x > COURT_WIDTH // 2 and player.swing_dir == 'Left':
                    player.face_dir = 'Left'
                    player.action = actions['Stand']
                elif player.x <= COURT_WIDTH // 2 and player.swing_dir == 'Right':
                    player.face_dir = 'Right'
                    player.action = actions['Stand']
                else: player.action = actions['Idle']

            if int(player.frame) == 2:
                if player.swing_dir == 'Left':
                    player.collision_xy = (player.x + 25, player.y - 75, player.x + 75, player.y - 25)
                elif player.swing_dir == 'Right':
                    player.collision_xy = (player.x - 75, player.y - 75, player.x - 25, player.y - 25)

            player.frame = (player.frame + FRAMES_PER_TIME * game_framework.frame_time) % 4
        else:
            player.collision_xy = (0, 0, 0, 0)
            player.frame = (player.frame + FRAMES_PER_TIME * game_framework.frame_time * 0.25) % 4

    @staticmethod
    def draw(player):
        if player.action == actions['Idle']:
            if player.x <= COURT_WIDTH // 2: player.composite_draw_player(23 * 4, 40 * 4 + 17)
            else: player.draw_player(23 * 4, 40 * 4 + 17)
        elif player.face_dir == 'Left': player.composite_draw_player()
        else: player.draw_player()


class Run:
    @staticmethod
    def enter(player, e):
        if d_down(e) or a_up(e): player.xdir += 1
        elif a_down(e) or d_up(e): player.xdir -= 1
        if w_down(e) or s_up(e): player.ydir += 1
        elif s_down(e) or w_up(e): player.ydir -= 1

        player.dir = math.atan2(player.ydir, player.xdir)

        if player.action == actions['Swing']: return
        player.action = actions['Run']

        if player.xdir == 1: player.swing_dir = player.face_dir = 'Left'
        elif player.xdir == -1: player.swing_dir = player.face_dir = 'Right'

    @staticmethod
    def exit(player, e):
        if mouse_click(e): player.swing()

    @staticmethod
    def do(player):
        if player.action == actions['Swing']:
            if player.frame + FRAMES_PER_TIME * game_framework.frame_time >= 4: player.action = actions['Run']

            if int(player.frame) == 2:
                if player.swing_dir == 'Left':
                    player.collision_xy = (player.x + 25, player.y - 75, player.x + 75, player.y - 25)
                elif player.swing_dir == 'Right':
                    player.collision_xy = (player.x - 75, player.y - 75, player.x - 25, player.y - 25)
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

        if d_down(e) or a_up(e): player.xdir += 1
        elif a_down(e) or d_up(e): player.xdir -= 1

    @staticmethod
    def exit(player, e):
        if mouse_click(e): player.xdir = 0

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
        player.swing_dir = 'Left' if player.x >= 500 else 'Right'

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
            player.collision_xy = (player.x - 50, player.y + 50, player.x, player.y + 100)

    @staticmethod
    def draw(player):
        player.draw_player(23 * 4, 40 * 4 + 17)


class StateMachine:
    def __init__(self, player):
        self.player = player
        self.cur_state = Serve_Ready if play_mode.serve == 'player_2' else Idle
        self.transitions = {
            Idle: {},
            Run: {},
            Serve_Ready: {cpu_serve_start: Serve_Do},
            Serve_Do: {},
            Serve_Swing: {}
        }

    def start(self):
        self.cur_state.enter(self.player, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.player)
        self.player.x = clamp(200.0, self.player.x, 800.0)
        self.player.y = clamp(550.0, self.player.y, 850.0)

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
        self.c = None
        self.x, self.y = x, y
        self.tx, self.ty = 1000, 1000
        self.collision_xy = (0, 0, 0, 0)

        self.frame = 0
        self.action = actions['Idle']

        self.dir = 0
        self.xdir, self.ydir = 0, 0
        self.face_dir = 'Middle'
        self.swing_dir = 'Right'

        self.image = load_image(image)
        self.state_machine = StateMachine(self)
        self.state_machine.start()
        self.build_behavior_tree()

    def composite_draw_player(self, width = 23 * 4, height = 40 * 4):
        self.image.clip_composite_draw(
            int(self.frame) * 23, self.action * 40, 23, 40, 0, 'h', self.x, self.y, width, height)

    def draw_player(self, width = 23 * 4, height = 40 * 4):
        self.image.clip_draw(
            int(self.frame) * 23, self.action * 40, 23, 40, self.x, self.y, width, height)

    def update(self):
        self.swing_dir = 'Left' if self.x >= 500 else 'Right'
        self.bt.run()

    def draw(self):
        if self.face_dir == 'Right' or self.face_dir == 'Middle': self.draw_player()
        elif self.face_dir == 'Left': self.composite_draw_player()
        draw_rectangle(*self.collision_xy)

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
        self.x += RUN_SPEED_PPS * math.cos(self.dir) * game_framework.frame_time * 0.75
        self.y += RUN_SPEED_PPS * math.sin(self.dir) * game_framework.frame_time * 0.75

    def distance_less_than(self, x1, y1, x2, y2, r):
        distance2 = (x1 - x2) ** 2 + (y1 - y2) ** 2
        return distance2 < (PIXEL_PER_METER * r) ** 2

    def should_serve(self):
        if self.state_machine.cur_state == Serve_Ready: return BehaviorTree.SUCCESS
        else: return BehaviorTree.FAIL

    def set_random_location(self):
        self.tx, self.ty = random.randint(200, 800 + 1), 800
        return BehaviorTree.SUCCESS

    def move_to(self, r = 0.1):
        self.action = actions['Run']
        self.frame = (self.frame + FRAMES_PER_TIME * game_framework.frame_time * 0.5) % 4
        self.move_slightly_to(self.tx, self.ty)
        if self.distance_less_than(self.tx, self.ty, self.x, self.y, r): return BehaviorTree.SUCCESS
        else: return BehaviorTree.RUNNING

    def do_serve_toss(self):
        self.state_machine.handle_event(('CPU_SERVE_START', None))
        if play_mode.ball.zdir < 0 and :
            return BehaviorTree.SUCCESS
        else: return BehaviorTree.RUNNING

    def do_serve_swing(self):
        self.action = actions['Serve_Swing']
        if play_mode.ball.z // 75 <= 2 or int(self.frame) != 0:
            self.frame = (self.frame + FRAMES_PER_TIME * game_framework.frame_time) % 4
        if 1 <= int(self.frame) <= 2:
            self.collision_xy = (self.x - 50, self.y + 50, self.x, self.y + 100)
        if self.frame + FRAMES_PER_TIME * game_framework.frame_time > FRAMES_PER_ACTION:
            # play_mode.serve = 'player_1'
            self.swung += 1
            return BehaviorTree.SUCCESS
        else: return BehaviorTree.RUNNING

    def is_ball_hitted(self):
        if play_mode.ball.last_hitted_by == 'player_1':
            self.c = (700 - play_mode.ball.y) / (play_mode.ball.ydir * ball.RUN_SPEED_PPS * game_framework.frame_time)
        if play_mode.ball.last_hitted_by == 'player_1': return BehaviorTree.SUCCESS
        else: return BehaviorTree.FAIL

    def set_target_location(self):
        if self.c != None:
            if play_mode.ball.x + play_mode.ball.xdir * self.c >= 500:
                self.tx = play_mode.ball.x + play_mode.ball.xdir * self.c - 50
            else: self.tx = play_mode.ball.x + play_mode.ball.xdir * self.c + 50
            self.ty = random.randint(650, 850)
            self.c = None
        return BehaviorTree.SUCCESS

    def is_ball_nearby(self, r):
        if self.distance_less_than(play_mode.ball.x, play_mode.ball.y, self.x, self.y, r): return BehaviorTree.SUCCESS
        else: return BehaviorTree.FAIL

    def is_game_not_over(self):
        if play_mode.ball.state_machine.cur_state != Score: return BehaviorTree.SUCCESS
        else: return BehaviorTree.FAIL

    def do_swing(self):
        self.action = actions['Swing']
        self.collision_xy = (0, 0, 0, 0)

        if self.frame + FRAMES_PER_TIME * game_framework.frame_time * 0.75 > 4:
            return BehaviorTree.SUCCESS

        self.frame = (self.frame + FRAMES_PER_TIME * game_framework.frame_time * 0.75) % FRAMES_PER_ACTION

        if self.face_dir == 'Middle': self.swing_dir = 'Left' if self.x > COURT_WIDTH // 2 else 'Right'

        if int(self.frame) == 2:
            if self.swing_dir == 'Left':
                self.collision_xy = (self.x + 25, self.y - 75, self.x + 75, self.y - 25)
            elif self.swing_dir == 'Right':
                self.collision_xy = (self.x - 75, self.y - 75, self.x - 25, self.y - 25)

        # self.frame = (self.frame + FRAMES_PER_TIME * game_framework.frame_time) % 4
        return BehaviorTree.RUNNING

    def do_Idle(self):
        self.frame = 0
        self.collision_xy = (0, 0, 0, 0)
        if self.x > COURT_WIDTH // 2 and self.swing_dir == 'Left':
            self.face_dir = 'Left'
            self.action = actions['Stand']
        elif self.x <= COURT_WIDTH // 2 and self.swing_dir == 'Right':
            self.face_dir = 'Right'
            self.action = actions['Stand']
        else: self.action = actions['Idle']
        return BehaviorTree.SUCCESS

    def build_behavior_tree(self):
        a1 = Action('Do serve toss', self.do_serve_toss)
        a2 = Action('Set location', self.set_target_location)
        a3 = Action('Move to', self.move_to)
        a4 = Action('Do swing', self.do_swing)
        a5 = Action('Set random location', self.set_random_location)
        a6 = Action('Do Idle', self.do_Idle)
        a7 = Action('Do serve swing', self.do_serve_swing)

        c1 = Condition('Have to do serve?', self.should_serve)
        c2 = Condition('Is ball hitted by P1?', self.is_ball_hitted)
        c3 = Condition('Is ball nearby?', self.is_ball_nearby, 1.0)
        c4 = Condition('Is game not over?', self.is_game_not_over)

        SEQ_serve = Sequence('Serve', c1, a5, a3, a1, a7)
        SEQ_move_to = Sequence('Move', a2, a3)
        SEQ_swing = Sequence('Swing', c3, a4)
        SEQ_move_and_swing = Sequence('Move and Swing', c4, c2, SEQ_move_to, SEQ_swing)

        SEL_swing_or_do_idle = Selector('Swing or Do Idle', SEQ_move_and_swing, a6)
        SEL_serve_or_swing_or_do_idle = Selector('Serve or Swing or Do Idle', SEQ_serve, SEL_swing_or_do_idle)

        self.bt = BehaviorTree(SEL_serve_or_swing_or_do_idle)