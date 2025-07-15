import sys

import pygame #type: ignore
import time
from pygame.locals import *
import random

block_size = 40
bg_color = (110, 110, 5)

class apple:
    def __init__(self, surface):
        self.image = pygame.image.load("resources/pixel-apple.png").convert()
        self.parent_screen = surface
        self.x = block_size * 3
        self.y = block_size * 3

    def draw(self):
        #self.parent_screen.fill((110, 110, 5))
        self.parent_screen.blit(self.image, (self.x, self.y))
        #pygame.display.flip()

    def move(self):
        self.x = random.randint(0, 12) * block_size #multiplied by blocksize to transform it into pixel s
        self.y = random.randint(0, 12) * block_size
        #self.draw()

class Snake:
    def __init__(self, surface, length):
        self.len = length
        self.parent_screen = surface
        self.block = pygame.image.load("resources/pixel sblock2.png").convert()
        self.direction = 'down'


        self.block_x = [block_size] * length
        self.block_y = [block_size] * length

    def increase_len(self):
        self.len += 1
        self.block_x.append(-1)
        self.block_y.append(-1)

    def draw(self):
        #self.background = pygame.image.load("resources/background2.jpg")
        for i in range(self.len):
            self.parent_screen.blit(self.block, (self.block_x[i], self.block_y[i]))

        #pygame.display.flip()

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def automove(self):
        for i in range(self.len -1, 0, -1):
            self.block_x[i] = self.block_x[i-1]
            self.block_y[i] = self.block_y[i-1]

        if self.direction == 'up':
            self.block_y[0] -= block_size
        if self.direction == 'down':
            self.block_y[0] += block_size
        if self.direction == 'right':
            self.block_x[0] += block_size
        if self.direction == 'left':
            self.block_x[0] -= block_size

        self.draw()

class Env:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake and Apple")

        pygame.mixer.init()
        self.play_backgroundmusic()
        self.surface = pygame.display.set_mode((500, 500))
        # Load the background image
        self.background = pygame.image.load("resources/indigo2_bg.jpg")
        # Scale the image to match the surface size
        self.background = pygame.transform.scale(self.background, (500, 500))
        # Draw background image instead of filling with color
        self.surface.blit(self.background, (0, 0))
        self.snake = Snake(self.surface, 1)
        self.score = 0
        self.snake.draw()
        self.apple = apple(self.surface)
        self.apple.draw()

        #self. makes an object a class member
    def play(self):
        self.surface.blit(self.background, (0, 0))
        self.snake.automove()
        self.apple.draw()
        self.display_count()
        pygame.display.flip()

        if self.is_collision(self.snake.block_x[0], self.snake.block_y[0], self.apple.x, self.apple.y):
            #print("Snake eats apple")
            self.play_sound("crunch")
            self.snake.increase_len()
            self.apple.move()

        #Snake collision with itself
        for i in range(3, self.snake.len):
            if self.is_collision(self.snake.block_x[0], self.snake.block_y[0], self.snake.block_x[i], self.snake.block_y[i]):
                self.play_sound("scratch")
                raise "Game Over"
                #print("Game Over")
                #quit()

    def play_backgroundmusic(self):
        pygame.mixer.music.load("resources/rhythmic-background-music.mp3")
        pygame.mixer.music.play()

    def play_sound(self, sound):
        sound= pygame.mixer.Sound(f"resources/{sound}.mp3")
        pygame.mixer.Sound.play(sound)

    def show_game_over(self):
        try:
            # Load all required images
            game_over_img = pygame.image.load("resources/Gameover icon2.png").convert_alpha()
            replay_btn = pygame.image.load("resources/Play Button.png").convert_alpha()
            exit_btn = pygame.image.load("resources/exit pixel button.png").convert_alpha()

            # Scale images
            game_over_img = pygame.transform.scale(game_over_img, (300, 200))
            replay_btn = pygame.transform.scale(replay_btn, (100, 50))  # Adjust size as needed
            exit_btn = pygame.transform.scale(exit_btn, (100, 50))  # Adjust size as needed

            # Calculate positions
            img_x = (self.surface.get_width() - game_over_img.get_width()) // 2
            img_y = (self.surface.get_height() - game_over_img.get_height()) // 2

            # Position buttons side by side with some spacing
            button_y = img_y + game_over_img.get_height() + 50
            replay_btn_x = self.surface.get_width() // 2 - replay_btn.get_width() - 20
            exit_btn_x = self.surface.get_width() // 2 + 20

            # Create rectangles for button collision detection
            replay_rect = pygame.Rect(replay_btn_x, button_y, replay_btn.get_width(), replay_btn.get_height())
            exit_rect = pygame.Rect(exit_btn_x, button_y, exit_btn.get_width(), exit_btn.get_height())

            running = True
            while running:
                mouse_pos = pygame.mouse.get_pos()

                # Clear screen and draw background
                self.surface.blit(self.background, (0, 0))

                # Draw game over image
                self.surface.blit(game_over_img, (img_x, img_y))

                # Draw score
                font = pygame.font.SysFont("comicsans", 35)
                score_text = font.render(f"Final Score: {self.snake.len}", True, (255, 255, 255))
                score_rect = score_text.get_rect(
                    center=(self.surface.get_width() // 2, img_y + game_over_img.get_height() + 20))
                self.surface.blit(score_text, score_rect)

                # Draw buttons
                self.surface.blit(replay_btn, (replay_btn_x, button_y))
                self.surface.blit(exit_btn, (exit_btn_x, button_y))

                # Button hover effects
                if replay_rect.collidepoint(mouse_pos):
                    pygame.draw.rect(self.surface, (255, 255, 255), replay_rect, 2)  # White outline
                if exit_rect.collidepoint(mouse_pos):
                    pygame.draw.rect(self.surface, (255, 255, 255), exit_rect, 2)  # White outline

                pygame.display.flip()

                pygame.mixer.music.pause()

                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()

                    elif event.type == MOUSEBUTTONDOWN:
                        if replay_rect.collidepoint(event.pos):
                            # Reset game state
                            self.__init__()  # Reinitialize the game
                            self.run()  # Start new game
                            pygame.mixer.music.unpause()
                            return

                        elif exit_rect.collidepoint(event.pos):
                            pygame.quit()
                            sys.exit()

        except pygame.error as e:
            print(f"Couldn't load images: {e}")
            pygame.quit()
            sys.exit()



    def is_collision(self,x1, y1, x2, y2 ):
        if x1 >= x2 and x1 < x2 + block_size:
            if y1 >= y2 and y1 < y2 + block_size:
                return True
        else:
            return False

    def display_count(self):
        font = pygame.font.SysFont("comicsans", 30)
        text = font.render(f"Score: {self.snake.len}", True, (255, 255, 255))
        self.surface.blit(text, (350, 10))
        #pygame.display.flip()

    def run(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

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
                self.play()
            except Exception as e:
                self.show_game_over()

            time.sleep(0.3) #without pressing keys snake obj keeps moving



if __name__=="__main__":

    game = Env() #Game is the environment
    game.run()
    #this is how we perform object-oriented programming in Python.




pygame.display.flip()


#time.sleep(5)

