from pico2d import *
import random
import game_framework
import game_world

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

        match ball.z // 300:
            case -1: ball.zdir *= -1
            case 0: ball.frame = frames['Small']
            case 1: ball.frame = frames['Middle']
            case 2: ball.frame = frames['Big']
            case 3: ball.zdir *= -1

    @staticmethod
    def draw(ball):
        ball.image.clip_draw(0, ball.frame * 6, 6, 6, ball.x, ball.y, 25, 25)
        draw_rectangle(*ball.get_bb())


class StateMachine:
    def __init__(self, ball):
        self.ball = ball
        self.cur_state = Rally
        self.transitions = {}

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
        self.xdir, self.ydir, self.zdir = 0, 0, 1
        self.image = load_image('resource\\tennis_ball.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def update(self):
        self.state_machine.update()

    def draw(self):
        self.state_machine.draw()

    def get_bb(self):
        return self.x - 25, self.y - 25, self.x + 25, self.y + 25

    def handle_collision(self, group, other):
        if group == 'player:ball':
            self.xdir = random.randint(-50, 50) / 200
            self.ydir = 0.5 if self.ydir == 0 else self.ydir * -1
            if self.zdir < 0: self.zdir *= -1
        elif group == 'pannel:ball':
            self.ydir *= -1
            game_world.overlap = False

