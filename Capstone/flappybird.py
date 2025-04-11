import pygame
import random
import numpy as np
from pygame.locals import *


class FlappyBirdGame:
    def __init__(self):
        pygame.init()

        # Game parameters
        self.fps = 60
        self.screen_width = 864
        self.screen_height = 936
        self.scroll_speed = 4
        self.ground_scroll = 0

        # Initialize screen
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Flappy Bird')

        # Load images
        self.bg = pygame.image.load(r"C:\Users\madua\PycharmProjects\PythonProject\.venv\bg.png")
        self.ground_img = pygame.image.load(r"C:\Users\madua\PycharmProjects\PythonProject\.venv\base.png")

        # Bird properties
        self.bird_y = self.screen_height // 2
        self.bird_velocity = 0
        self.gravity = 1
        self.flap_strength = -10

        # Pipes
        self.pipes = []
        self.pipe_width = 70
        self.pipe_gap = 200
        self.pipe_speed = 4
        self.add_pipe()

        # AI properties
        self.ai_enabled = True

        # Clock for controlling frame rate
        self.clock = pygame.time.Clock()

    def add_pipe(self):
        pipe_x = self.screen_width
        pipe_height = random.randint(100, 400)
        self.pipes.append((pipe_x, pipe_height))

    def ai_decision(self):
        """Simple AI logic: Flap if bird is below the gap center."""
        if not self.pipes:
            return False

        pipe_x, pipe_height = self.pipes[0]
        gap_center = pipe_height + (self.pipe_gap // 2)
        return self.bird_y > gap_center

    def run_game(self):
        run = True
        while run:
            self.clock.tick(self.fps)
            self.draw_elements()
            self.update_game_state()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN and event.key == K_SPACE:
                    self.bird_velocity = self.flap_strength

            if self.ai_enabled and self.ai_decision():
                self.bird_velocity = self.flap_strength

            pygame.display.update()

        pygame.quit()

    def draw_elements(self):
        """Draw background, bird, pipes, and scrolling ground."""
        self.screen.blit(self.bg, (0, 0))

        # Draw pipes
        for pipe_x, pipe_height in self.pipes:
            pygame.draw.rect(self.screen, (0, 255, 0), (pipe_x, 0, self.pipe_width, pipe_height))
            pygame.draw.rect(self.screen, (0, 255, 0),
                             (pipe_x, pipe_height + self.pipe_gap, self.pipe_width, self.screen_height))

        # Draw bird
        pygame.draw.circle(self.screen, (255, 255, 0), (100, self.bird_y), 15)

        # Draw ground
        self.screen.blit(self.ground_img, (self.ground_scroll, 768))

    def update_game_state(self):
        """Update bird position, pipes, and ground scrolling."""
        self.bird_velocity += self.gravity
        self.bird_y += self.bird_velocity

        # Move pipes
        self.pipes = [(x - self.pipe_speed, h) for x, h in self.pipes if x > -self.pipe_width]

        # Add new pipes
        if not self.pipes or self.pipes[-1][0] < self.screen_width - 300:
            self.add_pipe()

        # Scroll ground
        self.ground_scroll -= self.scroll_speed
        if abs(self.ground_scroll) > 35:
            self.ground_scroll = 0


if __name__ == "__main__":
    game = FlappyBirdGame()
    game.run_game()