# import is used to iclude path of a class or the entire package in program
import pygame

# pygame.locals used to include constants in game.
from pygame.locals import *
import time
import random

size = 20


# Classes provides template for creating objects, which can bind code into data.
class apple:
    # Python def keyword is used to define a function.
    def __init__(self, parent_screen):
        # Self represents the instance of the class.
        self.parent_screen = parent_screen
        # pygame.image.load function call is used to load images.
        self.image = pygame.image.load("resources/app.png").convert()
        self.x = size * 3
        self.y = size * 3

    # draw() function is used to draw image on a specific point.
    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.x))
        # display.flip() is important everytime when we make any changes on display.
        pygame.display.flip()

    # move() function is used to move image in different sections of screen.
    # random module is used to generate random numbers.
    def move(self):
        self.x = random.randint(1, 14) * size
        self.y = random.randint(1, 19) * size


class Snake:
    def __init__(self, parent_screen, length):
        self.parent_screen = parent_screen
        self.block = pygame.image.load("resources/downmouth.gif").convert()
        self.direction = "down"
        self.body = pygame.image.load("resources/body.png")
        self.length = length
        self.x = [20] * length
        self.y = [20] * length

    def move_up(self):
        if self.direction != "down":
            self.direction = "up"
            self.block = pygame.image.load("resources/upmouth.gif")

    def move_down(self):
        if self.direction != "up":
            self.direction = "down"
            self.block = pygame.image.load("resources/downmouth.gif")

    def move_left(self):
        if self.direction != "right":
            self.direction = "left"
            self.block = pygame.image.load("resources/leftmouth.gif")

    def move_right(self):
        if self.direction != "left":
            self.direction = "right"
            self.block = pygame.image.load("resources/rightmouth.gif")

    def walk(self):
        # self.prev_x = self.x[0]  # Save the previous head position
        # self.prev_y = self.y[0]

        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == "up":
            self.y[0] -= size
        elif self.direction == "down":
            self.y[0] += size
        elif self.direction == "right":
            self.x[0] += size
        elif self.direction == "left":
            self.x[0] -= size

        self.draw()

    def draw(self):
        # Draw the head
        self.parent_screen.blit(self.block, (self.x[0], self.y[0]))

        # Draw the body segments
        for i in range(1, self.length):
            self.parent_screen.blit(self.body, (self.x[i], self.y[i]))

        pygame.display.flip()

    def increase_length(self):
        self.length += 1
        self.x.append(1)
        self.y.append(1)


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.play_backgroud_music()
        self.surface = pygame.display.set_mode((800, 600))
        self.snake = Snake(self.surface, 1)
        self.snake.draw()
        self.apple = apple(self.surface)
        self.apple.draw()

    def render_background(self):
        bg = pygame.image.load("resources/background-image.png")
        self.surface.blit(bg, (0, 0))

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + size:
            if y1 >= y2 and y1 < y2 + size:
                return True
        return False

    def display_score(self):
        font = pygame.font.SysFont("Arial", 30)
        # score is set to snake length - 1 as length start with 1 as snake head.
        score = font.render(
            f"Score: {self.snake.length * 10 -10}", True, (200, 200, 200)
        )
        self.surface.blit(score, (650, 10))

    def show_game_over(self):
        self.render_background()
        font = pygame.font.SysFont("Arial", 30)
        line1 = font.render(
            # score is set to snake length - 1 as length start with 1 as snake head.
            f"Game Over! Score : {self.snake.length * 10-10}",
            True,
            (200, 200, 200),
        )
        self.surface.blit(line1, (200, 300))

        line2 = font.render(
            f"To play again press Enter!",
            True,
            (200, 200, 200),
        )
        self.surface.blit(line2, (200, 350))
        pygame.display.flip()
        pygame.mixer.music.pause()

    def reset(self):
        self.snake = Snake(self.surface, 1)
        self.apple = apple(self.surface)

    def play_backgroud_music(self):
        pygame.mixer.music.load("resources/bg.music.mp3")
        pygame.mixer.music.play(-1, 0)

    def play_sound(self, sound):
        sound = pygame.mixer.Sound(f"resources/{sound}.mp3")
        pygame.mixer.Sound.play(sound)

    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        # snake collidig with apple
        if self.is_collision(
            self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.x
        ):
            self.play_sound("crunch.1")
            self.snake.increase_length()
            self.apple.move()

        # snake colliding with itself
        for i in range(2, self.snake.length):
            if self.is_collision(
                self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]
            ):
                self.play_sound("game-over")
                raise "Collision Occured"
        # snake colliding with boundries of window
        if not (0 <= self.snake.x[0] <= 800 and 0 <= self.snake.y[0] <= 600):
            self.play_sound("game-over")
            raise "Hit the boundry error"

    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False
                    if not pause:
                        if event.key == K_UP:
                            self.snake.move_up()
                        if event.key == K_DOWN:
                            self.snake.move_down()
                        if event.key == K_LEFT:
                            self.snake.move_left()
                        if event.key == K_RIGHT:
                            self.snake.move_right()

                elif event.type == QUIT:
                    running = False

            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep(0.1)


if __name__ == "__main__":
    game = Game()
    game.run()
