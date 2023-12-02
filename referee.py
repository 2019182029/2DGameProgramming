from pico2d import *

import play_mode
import game_framework

direction = {'Middle': 0, 'Down': 1, 'Up': 2}

class Idle:
    @staticmethod
    def enter(referee, e):
        pass

    @staticmethod
    def exit(referee, e):
        pass

    @staticmethod
    def do(referee):
        referee.setheading(play_mode.ball)

    @staticmethod
    def draw(referee):
        referee.image.clip_draw(referee.frame * 17, 0, 17, 44, referee.x, referee.y, 17 * 5, 44 * 5)


class StateMachine:
    def __init__(self, referee):
        self.referee = referee
        self.cur_state = Idle
        self.transitions = {
        }

    def start(self):
        self.cur_state.enter(self.referee, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.referee)

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.referee, e)
                self.cur_state = next_state
                self.cur_state.enter(self.referee, e)
                return True
        return False

    def draw(self):
        self.cur_state.draw(self.referee)

class Referee:
    def __init__(self, image):
        self.x, self.y = 900, 550
        self.frame = direction['Middle']
        self.image = load_image(image)
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def update(self):
        self.state_machine.update()

    def draw(self):
        self.state_machine.draw()

    def setheading(self, ball):
        if ball.y <= 400: self.frame = direction['Down']
        elif ball.y > 700: self.frame = direction['Up']
        else: self.frame = direction['Middle']
