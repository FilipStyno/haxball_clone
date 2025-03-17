import pygame
import sys
from constants import *
from player import Player, handle_collision, handle_kick, handle_player_collision
from ball import Ball
from goal import Goal

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("HaxBall Clone")
        self.clock = pygame.time.Clock()
        
        # Vytvoření objektů
        self.player1 = Player(WIDTH//4, HEIGHT//2, RED, 
                              [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d])
        self.player2 = Player(3*WIDTH//4, HEIGHT//2, BLUE, 
                              [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT])
        self.ball = Ball()

        # Vytvoření branek
        self.left_goal = Goal(0, GOAL_WIDTH, GOAL_HEIGHT, GOAL_Y_OFFSET)
        self.right_goal = Goal(WIDTH - GOAL_WIDTH, GOAL_WIDTH, GOAL_HEIGHT, GOAL_Y_OFFSET)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Pohyb hráčů
            self.player1.move(self.ball)
            self.player2.move(self.ball)
            
            # Kolize mezi hráči
            handle_player_collision(self.player1, self.player2)
            
            # Kolize a kopání
            handle_collision(self.player1, self.ball)
            handle_collision(self.player2, self.ball)
            handle_kick(self.player1, self.ball, pygame.K_SPACE)
            handle_kick(self.player2, self.ball, pygame.K_RETURN)

            # Pohyb míče
            self.ball.move()

            # Kontrola gólů
            if self.right_goal.check_goal(self.ball):
                self.player1.score += 1
                self.ball.reset()
            elif self.left_goal.check_goal(self.ball):
                self.player2.score += 1
                self.ball.reset()

            if self.player1.score >= 5 or self.player2.score >= 5:
                running = False

            # Vykreslení
            self.screen.fill(BLACK)
            
            # Vykreslení hřiště
            pygame.draw.line(self.screen, WHITE, (WIDTH//2, 0), (WIDTH//2, HEIGHT))
            pygame.draw.circle(self.screen, WHITE, (WIDTH//2, HEIGHT//2), 50, 1)
            
            # Vykreslení branek
            self.left_goal.draw(self.screen)
            self.right_goal.draw(self.screen)
            
            # Vykreslení skóre
            font = pygame.font.Font(None, 74)
            score_text = font.render(f"{self.player1.score} - {self.player2.score}", True, WHITE)
            self.screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 20))

            self.player1.draw(self.screen)
            self.player2.draw(self.screen)
            self.ball.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(FPS)

        # Zobrazení vítěze
        winner_text = "Player 1 Wins!" if self.player1.score >= 5 else "Player 2 Wins!"
        font = pygame.font.Font(None, 74)
        text = font.render(winner_text, True, WHITE)
        self.screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2))
        pygame.display.flip()

        pygame.time.wait(2000)
        pygame.quit()
        sys.exit()