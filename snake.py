__author__ = 'tim'
import pygame
import random
import os
import sys

width, height = 20, 20
center = width/2, height/2

os.environ['SDL_VIDEO_CENTERED'] = '1'


class SnakeWorld(object):
    def __init__(self, environment):
        self.environment = environment

    def draw_point(self, color, point):
        pygame.draw.rect(self.environment.screen, color, (point[0] * 10, point[1]*10, 10, 10))


class Candie(SnakeWorld):
    def __init__(self, environment):
        super(Candie, self).__init__(environment)
        self.point = center
        self.color = (200, 120, 120)

    def eaten(self):
        self.point = random.randrange(width), random.randrange(height)

    def draw(self):
        self.draw_point(self.color, self.point)


class Snake(SnakeWorld):
    def __init__(self, environment):
        super(Snake, self).__init__(environment)

        self.body = []
        self.directions = [(0, -1), (-1, 0), (0, 1), (1, 0)]
        self.direction_index = 0

        self.body.append(center)

        self.size = (10, 10)
        self.color = (100, 100, 100)

        self.direction = (0, -1)

    def turn_right(self):
        self.direction_index = (self.direction_index - 1) % 4

    def turn_left(self):
        self.direction_index = (self.direction_index + 1) % 4

    def touch(self, candie):
        if candie.point == self.body[0]:
            return True
        return False

    def touch_self(self):
        head = self.body[0]
        if head in self.body[1:]:
            return True
        return False

    def touch_wall(self):
        head = self.body[0]
        if head[0] < 0 or head[1] < 0 or head[1] >= width or head[0] >= height:
            return True
        return False

    def eat(self, candie):
        candie.eaten()
        self.extend()

    def extend(self):
        first = self.body[0]
        direction = self.directions[self.direction_index]
        extended = first[0] + direction[0], first[1] + direction[1]
        self.body.insert(0, extended)

    def draw(self, static=False):

        if not static:
            self.extend()
            self.body.pop()

        for point in self.body:
            self.draw_point(self.color, point)


class Core(object):
    STATE_INIT_PLAY = -1
    STATE_NORMAL_PLAY = 0
    STATE_GAME_OVER = 1

    def __init__(self, surface, name):
        pygame.display.set_caption(name)
        self.screen = surface
        self.clock = pygame.time.Clock()
        self.tick = 6.0
        self.state = Core.STATE_INIT_PLAY

    def dispatch(self, event):
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.state = Core.STATE_INIT_PLAY
            #sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pass
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.snake.turn_left()
            if event.key == pygame.K_RIGHT:
                self.snake.turn_right()

    def init_play(self):
        self.snake = Snake(self)
        self.candie = Candie(self)
        self.state = Core.STATE_NORMAL_PLAY

    def normal_play(self):
        """ main logic for playing """

        if self.snake.touch(self.candie):
            self.snake.eat(self.candie)

        self.candie.draw()
        self.snake.draw()

        if self.snake.touch_self() or self.snake.touch_wall():
            self.state = Core.STATE_GAME_OVER

    def game_over(self):
        myfont = pygame.font.SysFont(None, 15)
        label = myfont.render("Game Over!", 1, (200, 0, 0))
        self.candie.draw()
        self.snake.draw(static=True)
        self.screen.blit(label, (100, 100))

    def get_tick(self):
        self.tick *= 1.0001
        return int(self.tick)

    STATE_MAP = {
        STATE_INIT_PLAY: init_play,
        STATE_GAME_OVER: game_over,
        STATE_NORMAL_PLAY: normal_play,
    }

    def run(self):
        """ whole loop of the game"""
        while True:
            for event in pygame.event.get():
                self.dispatch(event)

            self.screen.fill([0xFF, 0xFF, 0xFF])

            state_function = Core.STATE_MAP[self.state]
            state_function(self)

            pygame.display.flip()
            self.clock.tick(self.get_tick())


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((width*10, height*10))
    main = Core(screen, 'Node')
    main.run()