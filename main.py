import pygame
import random
import math

# Pygame setup
pygame.init()
pygame.mixer.init()
pygame.font.init()  # Initialize the font module


GROUND_HEIGHT = 40

# Constants
WIDTH = 1024
HEIGHT = 768
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)  # Color for the wall
GRAVITY = 0.5
JUMP_POWER = -12
ARROW_SPEED = 15
SCOPE_LENGTH = 100
ARROW_GRAVITY = 0.2

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

current_turn = 1  # 1 for player 1's turn, 2 for player 2's turn
game_over = False


# Wall class
class Wall(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        # Place the wall in the middle of the screen
        self.rect = self.image.get_rect(midtop=(WIDTH / 2, HEIGHT - height - GROUND_HEIGHT))


# Ground class
class Ground(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect(bottom=HEIGHT)


# ArrowMan class
class ArrowMan(pygame.sprite.Sprite):
    def __init__(self, x, y, player_id, is_left=True):
        super().__init__()
        self.is_left = is_left
        self.player_id = player_id
        self.image = pygame.Surface((50, 100), pygame.SRCALPHA)
        self.original_image = self.image  # Keep reference to original image for redrawing
        self.rect = self.image.get_rect(midbottom=(x, y))  # Adjusted for correct ground positioning
        self.y_speed = 0
        self.on_ground = False
        self.angle = 0 if is_left else 180
        self.draw_arrow_man()

    def draw_arrow_man(self):
        self.image = self.original_image.copy()  # Reset image before drawing
        pygame.draw.circle(self.image, BLACK, (25, 20), 10)
        pygame.draw.line(self.image, BLACK, (25, 30), (25, 70), 2)
        pygame.draw.line(self.image, BLACK, (25, 50), (10, 40), 2)
        pygame.draw.line(self.image, BLACK, (25, 50), (40, 40), 2)
        pygame.draw.line(self.image, BLACK, (25, 70), (10, 90), 2)
        pygame.draw.line(self.image, BLACK, (25, 70), (40, 90), 2)

    def update(self):
        if self.player_id == current_turn:
            self.apply_gravity()
            self.check_ground()
        self.draw_arrow_man()

    def apply_gravity(self):
        if not self.on_ground:
            self.y_speed += GRAVITY
        else:
            self.y_speed = 0
        self.rect.y += self.y_speed

    def check_ground(self):
        if self.rect.bottom >= HEIGHT - 40:
            self.rect.bottom = HEIGHT - 40
            self.on_ground = True

    def jump(self):
        if self.on_ground:
            self.y_speed = JUMP_POWER
            self.on_ground = False

    def scope_up(self):
        if not self.on_ground:
            return

        print(self.angle)

        if self.is_left:
            self.angle = arrow_man.angle - 5  # Limit angle
        else:
            self.angle = min(360, self.angle + 5)

    def scope_down(self):
        if not self.on_ground:
            return

        print(self.angle)

        if self.is_left:
            self.angle = min(360, arrow_man.angle + 5)  # Limit angle
        else:
            self.angle = max(180, self.angle - 5)

    def draw_scope(self):
        end_x = self.rect.centerx + SCOPE_LENGTH * math.cos(math.radians(self.angle))
        end_y = self.rect.centery + SCOPE_LENGTH * math.sin(math.radians(self.angle))

        line_length = 5
        pygame.draw.line(SCREEN, RED, (end_x - line_length, end_y - line_length),
                         (end_x + line_length, end_y + line_length), 2)
        pygame.draw.line(SCREEN, RED, (end_x - line_length, end_y + line_length),
                         (end_x + line_length, end_y - line_length), 2)


class Arrow(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        super().__init__()
        self.length = 40
        self.original_image = pygame.Surface((self.length, 2), pygame.SRCALPHA)
        self.original_image.fill(RED)
        self.image = pygame.transform.rotate(self.original_image, -angle)
        self.rect = self.image.get_rect(center=(x, y))
        self.vx = ARROW_SPEED * math.cos(math.radians(angle))
        self.vy = ARROW_SPEED * math.sin(math.radians(angle))
        self.angle = angle
        self.stuck = False

    def update(self):
        global game_over, current_turn

        if not self.stuck:
            self.vy += ARROW_GRAVITY
            self.vx += random.uniform(-0.5, 0.5)
            self.vy += random.uniform(-0.5, 0.5)

            self.rect.x += self.vx
            self.rect.y += self.vy

            angle_rad = math.atan2(self.vy, self.vx)
            self.angle = math.degrees(angle_rad)
            self.image = pygame.transform.rotate(self.original_image, -self.angle)
            self.rect = self.image.get_rect(center=self.rect.center)

            if self.rect.colliderect(wall.rect) or self.rect.bottom >= HEIGHT - 40:
                self.stuck = True
                self.vx = self.vy = 0

            if (pygame.sprite.collide_rect(self, arrow_man) and current_turn == 1) or (pygame.sprite.collide_rect(self, arrow_man2) and current_turn == 2):
                game_over = True  # End the game
                # Determine the winner based on who's turn it was
                winner = "Player 2" if current_turn == 1 else "Player 1"
                print(f"{winner} wins!")
                self.stuck = True  # Prevent further updates

# Other class definitions remain the same...


def shoot_arrow():
    global current_turn
    # Ensure that arrows are shot by the current player
    if current_turn == 1:
        arrow = Arrow(arrow_man.rect.centerx, arrow_man.rect.centery, arrow_man.angle)
    else:
        arrow = Arrow(arrow_man2.rect.centerx, arrow_man2.rect.centery, arrow_man2.angle)
    all_sprites.add(arrow)
    arrows.add(arrow)
    # Switch turns
    current_turn = 2 if current_turn == 1 else 1


# Initialize Pygame and create window
pygame.display.set_caption("ArrowMan Game")
clock = pygame.time.Clock()
game_over_font = pygame.font.SysFont("arial", 64)  # You can adjust the font and size

# Sprite groups
all_sprites = pygame.sprite.Group()
arrows = pygame.sprite.Group()
ground = Ground(GREEN, WIDTH, GROUND_HEIGHT)
wall = Wall(GRAY, WIDTH / 10, HEIGHT / 2)  # Create a grey wall
arrow_man = ArrowMan(50, HEIGHT - 40, 1)  # Player 1
arrow_man2 = ArrowMan(WIDTH - 50, HEIGHT - 40, 2, is_left=False)  # Player 2

# Adding instances to sprite groups
all_sprites.add(ground)
all_sprites.add(wall)  # Add the wall to the sprite group for rendering
all_sprites.add(arrow_man)
all_sprites.add(arrow_man2)

# Game loop
running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if current_turn == 1:
                if event.key == pygame.K_w:
                    arrow_man.scope_up()
                if event.key == pygame.K_s:
                    arrow_man.scope_down()
                if event.key == pygame.K_SPACE:
                    shoot_arrow()
            else:
                if event.key == pygame.K_w:
                    arrow_man2.scope_up()
                if event.key == pygame.K_s:
                    arrow_man2.scope_down()
                if event.key == pygame.K_SPACE:
                    shoot_arrow()

    if not game_over:
        all_sprites.update()

    SCREEN.fill(WHITE)
    all_sprites.draw(SCREEN)
    # Decide which ArrowMan should draw its scope based on the turn
    if current_turn == 1:
        arrow_man.draw_scope()
    else:
        arrow_man2.draw_scope()

    pygame.display.flip()
    if game_over:
        game_over_text = game_over_font.render(f"Game Over! Player {1 if current_turn == 2 else 2} wins!", True, RED)

        # Calculate the position for the text to be centered
        text_rect = game_over_text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        SCREEN.blit(game_over_text, text_rect)
        pygame.display.flip()  # Update the display with the game over message
        pygame.time.wait(3000)  # Wait a few seconds before ending the game
        running = False  # Stop the game loop



pygame.quit()
