from pygame.locals import *
from random import randint
import pygame
import time


class Fruit:
    x = 0
    y = 0
    step = 44

    def __init__(self, x, y):
        self.x = x * self.step
        self.y = y * self.step

    def draw(self, surface, image):
        surface.blit(image, (self.x, self.y))


class Snake:
    x = [0]
    y = [0]
    step = 44
    direction = 0
    length = 3

    # This value determines the speed of the snake
    # This can be used to set the level of play. 
    # Keep the values between 1 - 5, 1 being the most difficult
    updateCountMax = 10
    updateCount = 0

    def __init__(self, length):
        self.length = length
        for i in range(0, 2000):
            self.x.append(-100)
            self.y.append(-100)

        # initial positions, no collision.
        self.x[1] = 1 * 44
        self.x[2] = 2 * 44


    def set_level(self, level):
        level = 5 - level + 1
        if level < 1:
            self.updateCountMax = 1
        elif level > 5:
            self.updateCountMax = 5
        else:    
            self.updateCountMax = level

    def update(self):

        self.updateCount = self.updateCount + 1
        if self.updateCount > self.updateCountMax:

            # update previous positions
            for i in range(self.length - 1, 0, -1):
                self.x[i] = self.x[i - 1]
                self.y[i] = self.y[i - 1]

            # update position of head of snake
            if self.direction == 0:
                self.x[0] = self.x[0] + self.step
            if self.direction == 1:
                self.x[0] = self.x[0] - self.step
            if self.direction == 2:
                self.y[0] = self.y[0] - self.step
            if self.direction == 3:
                self.y[0] = self.y[0] + self.step

            self.updateCount = 0

    def moveRight(self):
        self.direction = 0

    def moveLeft(self):
        self.direction = 1

    def moveUp(self):
        self.direction = 2

    def moveDown(self):
        self.direction = 3

    def draw(self, surface, image):
        for i in range(0, self.length):
            surface.blit(image, (self.x[i], self.y[i]))


class Game:
    def isCollision(self, x1, y1, x2, y2, bsize):
        if x1 >= x2 and x1 <= x2 + bsize:
            if y1 >= y2 and y1 <= y2 + bsize:
                return True
        return False

    def isCollision_with_walls(self, x, y, windowWidth, windowHeight):
        if y < 0 or y > windowHeight - 44 or x < 0 or x > windowWidth - 44:
            return True
        return False


class App:
    windowWidth = 1500
    windowHeight = 1000
    Snake = 1
    Fruit = 2

    def __init__(self):
        self._running = True
        self._display_surf = None
        self._apple_surf = None
        self._snake_body = None
        self.game = Game()
        self.Snake = Snake(1)
        self.Snake.set_level(int(raw_input("Enter the level you would like to play at [1 to 5]: ")))
        self.Fruit = Fruit(10, 10)
        self.score = 0
        self.isHead = True

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((self.windowWidth, self.windowHeight), pygame.HWSURFACE)

        pygame.display.set_caption('The SNAKE Game')
        self._running = True
        self._apple_surf = pygame.image.load("rat.png").convert()
        self._snake_body = pygame.image.load("snake_body.png").convert()

    def on_event(self, event):
        if event.type == QUIT:
            self._running = False

    def on_loop(self):
        self.Snake.update()

        # does snake eat Fruit?
        for i in range(0, self.Snake.length):
            if self.game.isCollision(self.Fruit.x, self.Fruit.y, self.Snake.x[i], self.Snake.y[i], 44):
                self.Fruit.x = randint(2, 9) * 44
                self.Fruit.y = randint(2, 9) * 44
                self.Snake.length = self.Snake.length + 1
                self.score += 1

        # does snake collide with itself?
        for i in range(2, self.Snake.length):
            if self.game.isCollision(self.Snake.x[0], self.Snake.y[0], self.Snake.x[i], self.Snake.y[i], 40):
               message = "You lose! Collision with self"
               self.terminate_game(message)

        for i in range(0, 1):
            if self.game.isCollision_with_walls(self.Snake.x[i], self.Snake.y[i], self.windowWidth, self.windowHeight):
                message = "You lose! Collision with wall"
                self.terminate_game(message)
                
        pass


    def terminate_game(self, message):
        print("=====================================================")
        print(message)
        print ("Your score is: " + str(self.score))
        print("=====================================================")
        exit(0)

    def on_render(self):
        self._display_surf.fill((0, 0, 0))
        self.Snake.draw(self._display_surf, self._snake_body)
        self.Fruit.draw(self._display_surf, self._apple_surf)
        pygame.display.flip()

    def on_cleanup(self): 
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while (self._running):
            pygame.event.pump()
            keys = pygame.key.get_pressed()

            if (keys[K_RIGHT]):
                self.Snake.moveRight()

            if (keys[K_LEFT]):
                self.Snake.moveLeft()

            if (keys[K_UP]):
                self.Snake.moveUp()

            if (keys[K_DOWN]):
                self.Snake.moveDown()

            if (keys[K_ESCAPE]):
                self._running = False

            self.on_loop()
            self.on_render()

            time.sleep(50.0 / 1000.0);
        self.on_cleanup()


if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()