import pygame
import sys
import math

# Inicializace Pygame
pygame.init()

# Konstanty
WIDTH = 800
HEIGHT = 600
FPS = 60

# Rozměry branky
GOAL_HEIGHT = 140
GOAL_WIDTH = 20
GOAL_Y_OFFSET = (HEIGHT - GOAL_HEIGHT) // 2

# Barvy
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GOAL_COLOR = (200, 200, 200)

# Nastavení obrazovky
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("HaxBall Clone")
clock = pygame.time.Clock()

class Goal:
    def __init__(self, x, width, height, y_offset):
        self.x = x
        self.width = width
        self.height = height
        self.y = y_offset
        self.rect = pygame.Rect(x, y_offset, width, height)

    def draw(self):
        pygame.draw.rect(screen, GOAL_COLOR, self.rect)
        # Horní a dolní tyčka
        pygame.draw.rect(screen, WHITE, (self.x, self.y, self.width, 5))
        pygame.draw.rect(screen, WHITE, (self.x, self.y + self.height - 5, self.width, 5))

    def check_goal(self, ball):
        ball_rect = pygame.Rect(ball.x - ball.radius, ball.y - ball.radius, 
                              ball.radius * 2, ball.radius * 2)
        return self.rect.colliderect(ball_rect)

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

    def move(self):
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

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

class Ball:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.radius = 15  # Zvětšeno z 10 na 15
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
    if keys[kick_key] and check_collision(player, ball) and player.kick_cooldown <= 0:
        dx = ball.x - player.x
        dy = ball.y - player.y
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance > 0:
            dx /= distance
            dy /= distance
            ball.speed_x += dx * player.kick_power
            ball.speed_y += dy * player.kick_power
            player.kick_cooldown = 15

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

# Vytvoření objektů
player1 = Player(WIDTH//4, HEIGHT//2, RED, [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d])
player2 = Player(3*WIDTH//4, HEIGHT//2, BLUE, [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT])
ball = Ball()

# Vytvoření branek
left_goal = Goal(0, GOAL_WIDTH, GOAL_HEIGHT, GOAL_Y_OFFSET)
right_goal = Goal(WIDTH - GOAL_WIDTH, GOAL_WIDTH, GOAL_HEIGHT, GOAL_Y_OFFSET)

# Herní smyčka
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    player1.move()
    player2.move()
    
    handle_collision(player1, ball)
    handle_collision(player2, ball)
    handle_kick(player1, ball, pygame.K_SPACE)
    handle_kick(player2, ball, pygame.K_RETURN)
    handle_player_collision(player1, player2)

    ball.move()

    # Kontrola gólů
    if right_goal.check_goal(ball):
        player1.score += 1
        ball.reset()
    elif left_goal.check_goal(ball):
        player2.score += 1
        ball.reset()

    if player1.score >= 5 or player2.score >= 5:
        running = False

    # Vykreslení
    screen.fill(BLACK)
    
    # Vykreslení hřiště
    pygame.draw.line(screen, WHITE, (WIDTH//2, 0), (WIDTH//2, HEIGHT))
    pygame.draw.circle(screen, WHITE, (WIDTH//2, HEIGHT//2), 50, 1)
    
    # Vykreslení branek
    left_goal.draw()
    right_goal.draw()
    
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

pygame.time.wait(2000)
pygame.quit()
sys.exit()