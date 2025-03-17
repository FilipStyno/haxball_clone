import pygame
from constants import *

class Goal:
    def __init__(self, x, width, height, y_offset):
        self.x = x
        self.width = width
        self.height = height
        self.y = y_offset
        self.rect = pygame.Rect(x, y_offset, width, height)

    def draw(self, screen):
        pygame.draw.rect(screen, GOAL_COLOR, self.rect)
        # Horní a dolní tyčka
        pygame.draw.rect(screen, WHITE, (self.x, self.y, self.width, 5))
        pygame.draw.rect(screen, WHITE, (self.x, self.y + self.height - 5, self.width, 5))

    def check_goal(self, ball):
        ball_rect = pygame.Rect(ball.x - ball.radius, ball.y - ball.radius, 
                              ball.radius * 2, ball.radius * 2)
        return self.rect.colliderect(ball_rect)