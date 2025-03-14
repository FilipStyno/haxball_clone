import pygame
import sys
import math

# Inicializace Pygame
pygame.init()

# Konstanty
WIDTH = 800
HEIGHT = 600
FPS = 60

# Barvy
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Nastavení obrazovky
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("HaxBall Clone")
clock = pygame.time.Clock()

class Player:
    def __init__(self, x, y, color, controls):
        self.x = x
        self.y = y
        self.radius = 20
        self.color = color
        self.speed = 5
        self.controls = controls
        self.score = 0

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[self.controls[0]]:  # Nahoru
            self.y = max(self.radius, self.y - self.speed)
        if keys[self.controls[1]]:  # Dolů
            self.y = min(HEIGHT - self.radius, self.y + self.speed)
        if keys[self.controls[2]]:  # Doleva
            self.x = max(self.radius, self.x - self.speed)
        if keys[self.controls[3]]:  # Doprava
            self.x = min(WIDTH - self.radius, self.x + self.speed)

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

class Ball:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.radius = 10
        self.speed_x = 0
        self.speed_y = 0
        self.friction = 0.98

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y
        
        # Odrazy od stěn
        if self.x - self.radius <= 0 or self.x + self.radius >= WIDTH:
            self.speed_x *= -1
        if self.y - self.radius <= 0 or self.y + self.radius >= HEIGHT:
            self.speed_y *= -1

        # Tření
        self.speed_x *= self.friction
        self.speed_y *= self.friction

    def draw(self):
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.radius)

    def reset(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.speed_x = 0
        self.speed_y = 0

def check_collision(player, ball):
    distance = math.sqrt((player.x - ball.x)**2 + (player.y - ball.y)**2)
    return distance < player.radius + ball.radius

def handle_kick(player, ball, kick_key):
    keys = pygame.key.get_pressed()
    if keys[kick_key] and check_collision(player, ball):
        dx = ball.x - player.x
        dy = ball.y - player.y
        length = math.sqrt(dx**2 + dy**2)
        if length > 0:
            dx /= length
            dy /= length
            ball.speed_x = dx * 15
            ball.speed_y = dy * 15

# Vytvoření objektů
player1 = Player(WIDTH//4, HEIGHT//2, RED, [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d])
player2 = Player(3*WIDTH//4, HEIGHT//2, BLUE, [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT])
ball = Ball()

# Herní smyčka
running = True
while running:
    # Zpracování událostí
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Pohyb hráčů
    player1.move()
    player2.move()
    
    # Kopání míče
    handle_kick(player1, ball, pygame.K_SPACE)
    handle_kick(player2, ball, pygame.K_RETURN)

    # Pohyb míče
    ball.move()

    # Kontrola gólů
    if ball.x < 0:
        player2.score += 1
        ball.reset()
    elif ball.x > WIDTH:
        player1.score += 1
        ball.reset()

    # Kontrola vítězství
    if player1.score >= 5 or player2.score >= 5:
        running = False

    # Vykreslení
    screen.fill(BLACK)
    
    # Vykreslení hřiště
    pygame.draw.line(screen, WHITE, (WIDTH//2, 0), (WIDTH//2, HEIGHT))
    
    # Vykreslení skóre
    font = pygame.font.Font(None, 74)
    score_text = font.render(f"{player1.score} - {player2.score}", True, WHITE)
    screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 20))

    player1.draw()
    player2.draw()
    ball.draw()

    pygame.display.flip()
    clock.tick(FPS)

# Zobrazení vítěze
winner_text = "Player 1 Wins!" if player1.score >= 5 else "Player 2 Wins!"
font = pygame.font.Font(None, 74)
text = font.render(winner_text, True, WHITE)
screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2))
pygame.display.flip()

# Čekání před ukončením
pygame.time.wait(2000)
pygame.quit()
sys.exit()