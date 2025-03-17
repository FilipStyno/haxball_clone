import pygame
import math
from constants import *

class Ball:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.radius = 15
        self.speed_x = 0
        self.speed_y = 0
        self.friction = 0.98
        self.max_speed = 15
        self.bounce_dampening = 0.8

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y

        speed = math.sqrt(self.speed_x**2 + self.speed_y**2)
        if speed > self.max_speed:
            scale = self.max_speed / speed
            self.speed_x *= scale
            self.speed_y *= scale

        # Odrazy od horní a dolní stěny
        if self.y - self.radius <= 0:
            self.y = self.radius
            self.speed_y = abs(self.speed_y) * self.bounce_dampening
        elif self.y + self.radius >= HEIGHT:
            self.y = HEIGHT - self.radius
            self.speed_y = -abs(self.speed_y) * self.bounce_dampening

        # Odrazy od levé a pravé stěny (mimo branky)
        if self.x - self.radius <= 0 and (self.y < GOAL_Y_OFFSET or self.y > GOAL_Y_OFFSET + GOAL_HEIGHT):
            self.x = self.radius
            self.speed_x = abs(self.speed_x) * self.bounce_dampening
        elif self.x + self.radius >= WIDTH and (self.y < GOAL_Y_OFFSET or self.y > GOAL_Y_OFFSET + GOAL_HEIGHT):
            self.x = WIDTH - self.radius
            self.speed_x = -abs(self.speed_x) * self.bounce_dampening

        self.speed_x *= self.friction
        self.speed_y *= self.friction

        if abs(self.speed_x) < 0.1:
            self.speed_x = 0
        if abs(self.speed_y) < 0.1:
            self.speed_y = 0

    def draw(self, screen):
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.radius)

    def reset(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.speed_x = 0
        self.speed_y = 0