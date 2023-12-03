from pico2d import *
from event_check import *
from player_1 import Serve_Swing as SS1
from player_2 import Serve_Swing as SS2

import random
import game_framework
import game_world
import play_mode
import score_mode

PIXEL_PER_METER = (10.0 / 0.06)
RUN_SPEED_KMPH = 20.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

frames = {'Big': 0, 'Middle': 1, 'Small': 2}
judgment = {'IN': 0, 'OUT': 1, 'FAULT': 2}


class Rally:
    @staticmethod
    def enter(ball, e):
        pass

    @staticmethod
    def exit(ball, e):
        pass

    @staticmethod
    def do(ball):
        if play_mode.bubble.frame == judgment['OUT']:
            ball.ydir *= 0.25
            if ball.last_hitted_by == 'player_1': score_mode.p2_score_num += 1
            else: score_mode.p1_score_num += 1
            ball.state_machine.handle_event(('Score', None))

        ball.x += ball.xdir * RUN_SPEED_PPS * game_framework.frame_time
        ball.y += ball.ydir * RUN_SPEED_PPS * game_framework.frame_time
        ball.z += ball.zdir * RUN_SPEED_PPS * game_framework.frame_time

        ball.dir = math.atan2(ball.x, ball.y)

        match ball.z // 75:
            case 0:
                ball.frame = frames['Small']
                if ball.bounding == False:
                    ball.bound_sound.play()
                ball.bounding = True
            case 2:
                ball.bounding = False
                ball.frame = frames['Middle']
            case 4:
                ball.frame = frames['Big']

        if ball.z < 0 and ball.zdir < 0 and ball.bounced == True:
            if play_mode.bubble.frame != judgment['OUT']: score_mode.p1_score_num += 1
            else: score_mode.p2_score_num += 1
            ball.state_machine.handle_event(('Score', None))

        if ball.z < 0 and ball.zdir < 0:
            ball.zdir *= -1
            ball.bounced = True
            if ball.in_out():
                play_mode.bubble.frame = judgment['IN']
                if abs(ball.ydir) == 0.125: play_mode.bubble.frame = judgment['OUT']
            else: play_mode.bubble.frame = judgment['OUT']
        elif ball.z // 100 > 5 and ball.zdir > 0:
            ball.zdir *= -1

        if ball.y < -5:
            ball.xdir, ball.ydir, ball.zdir = 0, 0, 0
            if play_mode.bubble.frame != judgment['OUT']: score_mode.p2_score_num += 1
            else: score_mode.p1_score_num += 1
            ball.state_machine.handle_event(('Score', None))

    @staticmethod
    def draw(ball):
        ball.parabolic_motion()
        # draw_rectangle(*ball.get_bb())


class Score:
    @staticmethod
    def enter(ball, e):
        ball.frame = frames['Small']
        ball.xdir *= 0.25
        ball.ydir *= 0.25
        ball.z = 0
        ball.score_start_time = get_time()

        game_world.collision_pairs['player:ball'][1].remove(ball)

    @staticmethod
    def exit(ball, e):
        pass

    @staticmethod
    def do(ball):
        if (get_time() - ball.score_start_time > 1):
            game_framework.push_mode(score_mode)
            # game_framework.quit()
            pass

        ball.x += ball.xdir * RUN_SPEED_PPS * game_framework.frame_time
        ball.y += ball.ydir * RUN_SPEED_PPS * game_framework.frame_time

    @staticmethod
    def draw(ball):
        ball.parabolic_motion()


class Serve_Ready:
    @staticmethod
    def enter(ball, e):
        ball.frame = frames['Small']

    @staticmethod
    def exit(ball, e):
        pass

    @staticmethod
    def do(ball):
        if play_mode.serve == 'player_1': ball.x, ball.y = play_mode.player_1.x + 35, play_mode.player_1.y + 20
        else: ball.x, ball.y = play_mode.p2.x - 15, play_mode.p2.y - 15

    @staticmethod
    def draw(ball):
        ball.image.clip_draw(0, ball.frame * 6, 6, 6, ball.x, ball.y, 25, 25)


class Serve_Do:
    @staticmethod
    def enter(ball, e):
        if play_mode.serve == 'player_1': ball.x, ball.y = play_mode.player_1.x + 38, play_mode.player_1.y + 50
        else: ball.x, ball.y = play_mode.p2.x - 10, play_mode.p2.y + 18

    @staticmethod
    def exit(ball, e):
        pass

    @staticmethod
    def do(ball):
        ball.z += ball.zdir * RUN_SPEED_PPS * game_framework.frame_time

        match ball.z // 100:
            case 0:
                ball.frame = frames['Small']
            case 2:
                ball.frame = frames['Middle']
            case 4:
                ball.frame = frames['Big']

        if ball.z // 100 > 5 and ball.zdir > 0:
            ball.zdir *= -1

        if ball.z < 0 and ball.zdir < 0:
            play_mode.bubble.frame = judgment['FAULT']
            if play_mode.serve == 'player_1': score_mode.p1_score_num += 1
            else: score_mode.p2_score_num += 1
            ball.state_machine.handle_event(('Score', None))

    @staticmethod
    def draw(ball):
        ball.image.clip_draw(0, ball.frame * 6, 6, 6,
                                ball.x,
                                ball.y + math.sin(ball.dir + math.pi / 2) * (ball.z // 5),
                                25, 25)
        # draw_rectangle(*ball.get_bb())


class StateMachine:
    def __init__(self, ball):
        self.ball = ball
        self.cur_state = Serve_Ready
        self.transitions = {
            Rally: {game_over: Score},
            Score: {},
            Serve_Ready: {p1_space_down: Serve_Do, p2_mouse_click: Serve_Do, cpu_serve_start: Serve_Do},
            Serve_Do: {game_start: Rally, game_over: Score}
        }

    def start(self):
        self.cur_state.enter(self.ball, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.ball)

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.ball, e)
                self.cur_state = next_state
                self.cur_state.enter(self.ball, e)
                return True
        return False

    def draw(self):
        self.cur_state.draw(self.ball)


class Ball:
    def __init__(self):
        self.c = None
        self.x, self.y, self.z = 500, 250, 0
        self.tx, self.ty = 0, 0
        self.dir = 0
        self.xdir, self.ydir, self.zdir = 0, 0, 1

        self.frame = 0
        self.frame_index = 0

        self.score_start_time = 0
        self.bounced = False
        self.bounding = True
        self.wall_bounded = False
        self.last_hitted_by = 'player_2'

        self.image = load_image('resource\\objects\\tennis_ball.png')
        self.bound_sound = load_wav('resource\\play_mode\\bound.wav')
        self.bound_sound.set_volume(255)
        self.rally_sound = load_wav('resource\\play_mode\\rally.wav')
        self.rally_sound.set_volume(64)

        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def update(self):
        self.state_machine.update()

    def draw(self):
        self.state_machine.draw()
        # draw_rectangle(self.tx - 5, self.ty - 5, self.tx + 5, self.ty + 5)

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def parabolic_motion(self):
        if self.x > 500:
            self.image.clip_draw(0, self.frame * 6, 6, 6,
                                 self.x - math.cos(self.dir + math.pi / 2) * (self.z // (50 - abs(500 - self.x) // 10)),
                                 self.y + math.sin(self.dir + math.pi / 2) * (self.z // 10),
                                 25, 25)
        elif self.x < 500:
            self.image.clip_draw(0, self.frame * 6, 6, 6,
                                 self.x + math.cos(self.dir + math.pi / 2) * (self.z // (50 - abs(500 - self.x) // 10)),
                                 self.y + math.sin(self.dir + math.pi / 2) * (self.z // 10),
                                 25, 25)
        else:
            self.image.clip_draw(0, self.frame * 6, 6, 6,
                                 self.x,
                                 self.y + math.sin(self.dir + math.pi / 2) * (self.z // 10),
                                 25, 25)

    def in_out(self):
        if 140 <= self.x < 840 and 80 <= self.y < 280: return True
        if 200 <= self.x < 780 and 280 <= self.y < 475: return True
        if 240 <= self.x < 740 and 475 <= self.y < 670: return True
        if 280 <= self.x < 700 and 670 <= self.y < 870: return True

        return False

    def get_bb(self):
        calculated_x_1 = self.x - math.cos(self.dir + math.pi / 2) * (self.z // (50 - abs(500 - self.x) // 10))
        calculated_x_2 = self.x + math.cos(self.dir + math.pi / 2) * (self.z // (50 - abs(500 - self.x) // 10))
        calculated_y = self.y + math.sin(self.dir + math.pi / 2) * (self.z // 10)

        if self.wall_bounded: return (950, 950, 950, 950)

        if self.state_machine.cur_state == Serve_Do:
            return (self.x - 25, self.y + math.sin(self.dir + math.pi / 2) * (self.z // 5) - 25,
                    self.x + 25, self.y + math.sin(self.dir + math.pi / 2) * (self.z // 5) + 25)

        if self.x >= 500: return (calculated_x_1 - 25, calculated_y - 25, calculated_x_1 + 25, calculated_y + 25)
        else: return (calculated_x_2 - 25, calculated_y - 25, calculated_x_2 + 25, calculated_y + 25)
        # else: return (self.x - 25, calculated_y - 25, self.x + 25, calculated_y + 25)

    def handle_collision(self, group, other):
        if group == 'player:ball':
            if self.state_machine.cur_state == Serve_Do:
                if self.zdir > 0:
                    if play_mode.serve == 'player_1': score_mode.p2_score_num += 1
                    else: score_mode.p1_score_num += 1
                    play_mode.bubble.frame = judgment['FAULT']
                    self.state_machine.handle_event(('Score', None))

                self.rally_sound.play()
                self.state_machine.handle_event(('GAME_START', None))

            self.bounced = False

            if play_mode.game_mode == 'PVP':
                is_serve = other.state_machine.cur_state == SS1 or other.state_machine.cur_state == SS2
            else:
                is_serve = play_mode.player_1.state_machine.cur_state == SS1 or play_mode.player_cpu.action == 6

            if is_serve:
                if other == play_mode.player_1:
                    self.xdir = 0.25 if play_mode.player_1.swing_dir == 'Left' else -0.25
                    self.last_hitted_by = 'player_1'
                    self.rally_sound.play()
                    self.tc = random.choice((700, 750, 800))
                else:
                    self.xdir = -0.25 if play_mode.p2.swing_dir == 'Left' else 0.25
                    self.last_hitted_by = 'player_2'
                    self.rally_sound.play()
                    self.c = None
            else:
                if other == play_mode.player_1:
                    self.xdir = 0.05 if play_mode.player_1.swing_dir == 'Left' else -0.05
                    self.last_hitted_by = 'player_1'
                    self.rally_sound.play()
                    self.tc = random.choice((700, 750, 800))
                else:
                    self.xdir = -0.05 if play_mode.p2.swing_dir == 'Left' else 0.05
                    self.last_hitted_by = 'player_2'
                    self.rally_sound.play()
                    self.c = None

            if self.ydir == 0: self.ydir = 0.5
            elif self.ydir < 0 and other == play_mode.player_1: self.ydir = 0.6
            elif self.ydir > 0 and other == play_mode.p2: self.ydir = -0.5

            if other == play_mode.player_1:
                self.c = (self.tc - self.y) / (self.ydir * RUN_SPEED_PPS * game_framework.frame_time)
                self.tx = self.x + self.xdir * RUN_SPEED_PPS * game_framework.frame_time * self.c
                self.ty = self.y + self.ydir * RUN_SPEED_PPS * game_framework.frame_time * self.c

            if self.zdir < 0: self.zdir *= -1
        elif group == 'ball:pannel':
            if self.last_hitted_by == 'player_1':
                self.wall_bounded = True
                if self.ydir > 0: self.ydir *= -0.25
                if self.zdir > 0: self.zdir *= -1
