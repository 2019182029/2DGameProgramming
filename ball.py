from pico2d import *
from event_check import *

import random
import game_framework
import game_world
import play_mode
import select_mode

PIXEL_PER_METER = (10.0 / 0.06)
RUN_SPEED_KMPH = 20.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

frames = {'Big': 0, 'Middle': 1, 'Small': 2}


class Rally:
    @staticmethod
    def enter(ball, e):
        pass

    @staticmethod
    def exit(ball, e):
        pass

    @staticmethod
    def do(ball):
        ball.x += ball.xdir * RUN_SPEED_PPS * game_framework.frame_time
        ball.y += ball.ydir * RUN_SPEED_PPS * game_framework.frame_time
        ball.z += ball.zdir * RUN_SPEED_PPS * game_framework.frame_time

        ball.dir = math.atan2(ball.x, ball.y)

        match ball.z // 100:
            case 0:
                ball.frame = frames['Small']
            case 2:
                ball.frame = frames['Middle']
            case 4:
                ball.frame = frames['Big']

        if ball.z < 0 and ball.zdir < 0 and ball.bounced == True:
            ball.state_machine.handle_event(('Score', None))

        if ball.z < 0 and ball.zdir < 0:
            ball.zdir *= -1
            ball.bounced = True
        elif ball.z // 100 > 5 and ball.zdir > 0:
            ball.zdir *= -1

    @staticmethod
    def draw(ball):
        ball.parabolic_motion()
        draw_rectangle(*ball.get_bb())


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
            # game_framework.change_mode(select_mode)
            game_framework.quit()

        ball.x += ball.xdir * RUN_SPEED_PPS * game_framework.frame_time
        ball.y += ball.ydir * RUN_SPEED_PPS * game_framework.frame_time

    @staticmethod
    def draw(ball):
        ball.parabolic_motion()


class StateMachine:
    def __init__(self, ball):
        self.ball = ball
        self.cur_state = Rally
        self.transitions = {
            Rally: {game_over: Score}
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
        self.x, self.y, self.z = 500, 250, 0
        self.frame = 0
        self.frame_index = 0
        self.dir = 0
        self.xdir, self.ydir, self.zdir = 0, 0, 1
        self.score_start_time = 0
        self.bounced = False
        self.image = load_image('resource\\tennis_ball.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def update(self):
        self.state_machine.update()

    def draw(self):
        self.state_machine.draw()

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

    def get_bb(self):
        if self.x > 500:
            return (self.x - math.cos(self.dir + math.pi / 2) * (self.z // (50 - abs(500 - self.x) // 10)) - 25,
                    self.y + math.sin(self.dir + math.pi / 2) * (self.z // 10) - 25,
                    self.x - math.cos(self.dir + math.pi / 2) * (self.z // (50 - abs(500 - self.x) // 10)) + 25,
                    self.y + math.sin(self.dir + math.pi / 2) * (self.z // 10) + 25)
        elif self.x < 500:
            return (self.x + math.cos(self.dir + math.pi / 2) * (self.z // (50 - abs(500 - self.x) // 10)) - 25,
                    self.y + math.sin(self.dir + math.pi / 2) * (self.z // 10) - 25,
                    self.x + math.cos(self.dir + math.pi / 2) * (self.z // (50 - abs(500 - self.x) // 10)) + 25,
                    self.y + math.sin(self.dir + math.pi / 2) * (self.z // 10) + 25)
        else:
            return (self.x - 25,
                    self.y + math.sin(self.dir + math.pi / 2) * (self.z // 10) - 25,
                    self.x + 25,
                    self.y + math.sin(self.dir + math.pi / 2) * (self.z // 10) + 25)

    def handle_collision(self, group, other):
        if group == 'player:ball':
            self.bounced = False
            self.xdir = random.randint(-10, 10) / 200
            if self.ydir == 0: self.ydir = 0.5
            elif (self.ydir < 0 and other == play_mode.player_1) or (self.ydir > 0 and other == play_mode.player_2):
                self.ydir *= -1
            if self.zdir < 0: self.zdir *= -1
        elif group == 'ball:pannel':
            if self.ydir > 0: self.ydir *= -1
