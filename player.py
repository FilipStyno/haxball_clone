import pygame
import math
from constants import *

def check_collision(player, ball):
    distance = math.sqrt((player.x - ball.x)**2 + (player.y - ball.y)**2)
    return distance < player.radius + ball.radius

class Player:
    def __init__(self, x, y, color, controls):
        self.x = x
        self.y = y
        self.radius = 20
        self.color = color
        self.speed = 5
        self.controls = controls
        self.score = 0
        self.kick_power = 15
        self.kick_cooldown = 0
        self.velocity_x = 0
        self.velocity_y = 0

    def move(self, ball):
        keys = pygame.key.get_pressed()
        self.velocity_x = 0
        self.velocity_y = 0
        
        # Kontrola kontaktu s míčem
        ball_contact = check_collision(self, ball)
        
        # Nastavení rychlosti pohybu
        move_speed = self.speed * (0.3 if ball_contact else 1.0)
        
        if keys[self.controls[0]]:  # Nahoru
            self.velocity_y = -move_speed
        if keys[self.controls[1]]:  # Dolů
            self.velocity_y = move_speed
        if keys[self.controls[2]]:  # Doleva
            self.velocity_x = -move_speed
        if keys[self.controls[3]]:  # Doprava
            self.velocity_x = move_speed

        # Normalizace diagonálního pohybu
        if self.velocity_x != 0 and self.velocity_y != 0:
            diagonal_speed = math.sqrt(self.velocity_x**2 + self.velocity_y**2)
            scale = move_speed / diagonal_speed
            self.velocity_x *= scale
            self.velocity_y *= scale

        # Aplikace pohybu s omezením hranic
        self.x = max(self.radius, min(WIDTH - self.radius, self.x + self.velocity_x))
        self.y = max(self.radius, min(HEIGHT - self.radius, self.y + self.velocity_y))

        if self.kick_cooldown > 0:
            self.kick_cooldown -= 1

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

def handle_collision(player, ball):
    if check_collision(player, ball):
        dx = ball.x - player.x
        dy = ball.y - player.y
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance == 0:
            return
        
        # Zpomalení míče při kontaktu s hráčem
        ball.speed_x *= 0.3  # Výrazné zpomalení
        ball.speed_y *= 0.3
        
        # Udržení míče blízko hráče
        ball.x = player.x + dx * (player.radius + ball.radius) / distance
        ball.y = player.y + dy * (player.radius + ball.radius) / distance

def handle_kick(player, ball, kick_key):
    keys = pygame.key.get_pressed()
    if keys[kick_key] and check_collision(player, ball):
        dx = ball.x - player.x
        dy = ball.y - player.y
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance > 0:
            dx /= distance
            dy /= distance
            ball.speed_x += dx * player.kick_power
            ball.speed_y += dy * player.kick_power
            
def handle_player_collision(player1, player2):
    dx = player2.x - player1.x
    dy = player2.y - player1.y
    distance = math.sqrt(dx**2 + dy**2)
    
    if distance < player1.radius + player2.radius:
        if distance == 0:
            return
        
        overlap = (player1.radius + player2.radius) - distance
        dx /= distance
        dy /= distance
        
        # Posun hráčů od sebe
        player1.x -= dx * overlap / 2
        player1.y -= dy * overlap / 2
        player2.x += dx * overlap / 2
        player2.y += dy * overlap / 2