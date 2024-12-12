import pygame
import sys
import random
import math
from modules import get_bet

class Flinko:
    def __init__(self):
        # Screen Dimensions
        self.SCREEN_WIDTH = 1024
        self.SCREEN_HEIGHT = 576
        self.SCREEN = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Flinko")

        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.YELLOW = (255, 215, 0)

        # Game physics
        self.GRAVITY = 0.5
        self.BALL_RADIUS = 8
        
        # Peg configuration
        self.PEG_RADIUS = 18
        self.ROWS = 7
        self.COLUMN_SPACING = 85
        self.VERTICAL_SPACING = 66

        # Game state
        self.ball = None
        self.pegs = []
        self.buckets = []
        self.current_tokens = 0
        self.wall_images = None
        self.wall_width = 50 
     
    def show_result_dialog(self, result_message, is_win):
        pygame.mixer.init()
        sound = pygame.mixer.Sound("sounds/win.mp3") if is_win else pygame.mixer.Sound("sounds/lose.mp3")
        sound.play()
    
        dialog_width, dialog_height = 450, 250
        dialog_x = (self.SCREEN_WIDTH - dialog_width) // 2
        dialog_y = (self.SCREEN_HEIGHT - dialog_height) // 2
    
        exit_button_image = pygame.image.load("img/exit_button.png")
        exit_button_image = pygame.transform.scale(exit_button_image, (100, 50))
        exit_button = pygame.Rect(dialog_x + (dialog_width - 100) // 2, dialog_y + 200, 100, 50)
    
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
    
                if event.type == pygame.MOUSEBUTTONDOWN and exit_button.collidepoint(event.pos):
                    return 

            dialog_surface = pygame.Surface((dialog_width, dialog_height), pygame.SRCALPHA)
            dialog_surface.fill((255, 255, 255, 100))  

            border_color = (*self.BLACK, 220)  
            pygame.draw.rect(dialog_surface, border_color, dialog_surface.get_rect(), 5)

            large_font = pygame.font.Font(None, 48)

            result_text = large_font.render(result_message, True, self.BLACK)
            result_rect = result_text.get_rect(center=(dialog_width // 2, 100))
            dialog_surface.blit(result_text, result_rect)

            dialog_surface.blit(exit_button_image, (exit_button.x - dialog_x, exit_button.y - dialog_y))

            self.SCREEN.blit(dialog_surface, (dialog_x, dialog_y))

            pygame.display.flip()
            clock.tick(30)   
            
    def load_wall_images(self):
        """Load and scale wall images for the left and right sides"""
        wall_image = pygame.image.load("img/wall.png")

        wall_height = self.SCREEN_HEIGHT
        self.wall_images = {
            'left': pygame.transform.scale(wall_image, (self.wall_width, wall_height)),
            'right': pygame.transform.scale(wall_image, (self.wall_width, wall_height))
        }

    def create_pegs(self):
        """Create pegs in a pyramid pattern starting from 2 pegs"""
        self.pegs = []
        for row in range(self.ROWS):
            offset = (self.SCREEN_WIDTH - row * self.COLUMN_SPACING) / 2
            for col in range(row + 2):  # Changed from row + 1 to row + 2
                x = offset + col * self.COLUMN_SPACING
                y = 100 + row * self.VERTICAL_SPACING
                self.pegs.append((x, y))

    def create_ball(self):
        """Create a ball at the top of the screen"""
        self.ball = {
            'x': self.SCREEN_WIDTH / 2,
            'y': 50,
            'vx': 0,
            'vy': 0
        }

    def create_buckets(self):
        """Create alternating win/lose buckets at the bottom"""
        bucket_width = 85
        total_width = self.ROWS * bucket_width
        start_x = (self.SCREEN_WIDTH - total_width) / 2
        
        for i in range(self.ROWS + 1):
            x = start_x + i * bucket_width
            self.buckets.append({
                'x': x,
                'width': bucket_width,
                'win': i % 2 == 1  
            })

    def update_ball(self):
        """Update ball physics and collision"""
        # gravity
        self.ball['vy'] += self.GRAVITY

        # Update position
        self.ball['x'] += self.ball['vx']
        self.ball['y'] += self.ball['vy']

        # Wall collisions 
        left_wall_x = self.SCREEN_WIDTH / 2 - (self.ROWS * self.COLUMN_SPACING / 2) - self.wall_width
        right_wall_x = self.SCREEN_WIDTH / 2 + (self.ROWS * self.COLUMN_SPACING / 2)

        # Left wall bounce
        if self.ball['x'] - self.BALL_RADIUS < left_wall_x + self.wall_width:
            self.ball['x'] = left_wall_x + self.wall_width + self.BALL_RADIUS
            self.ball['vx'] *= -0.6  # Bounce with energy loss

        # Right wall bounce
        if self.ball['x'] + self.BALL_RADIUS > right_wall_x:
            self.ball['x'] = right_wall_x - self.BALL_RADIUS
            self.ball['vx'] *= -0.6  # Bounce with energy loss

        for peg in self.pegs:
            # Calculate distance between ball center and peg center
            dx = self.ball['x'] - peg[0]
            dy = self.ball['y'] - peg[1]
            distance = math.sqrt(dx**2 + dy**2)

            # Check if ball is colliding with peg
            if distance <= self.BALL_RADIUS + self.PEG_RADIUS:
                # Calculate collision normal
                normal_x = dx / distance
                normal_y = dy / distance

                # Separate the ball from the peg
                overlap = (self.BALL_RADIUS + self.PEG_RADIUS) - distance
                self.ball['x'] += normal_x * overlap
                self.ball['y'] += normal_y * overlap

                # Reflect velocity with energy loss
                dot_product = (self.ball['vx'] * normal_x + self.ball['vy'] * normal_y)
                self.ball['vx'] = (self.ball['vx'] - 2 * dot_product * normal_x) * 0.8
                self.ball['vy'] = (self.ball['vy'] - 2 * dot_product * normal_y) * 0.8

                # Add slight randomness to bounce
                self.ball['vx'] += random.uniform(-0.5, 0.5)
                self.ball['vy'] += random.uniform(-0.5, 0.5)

    def draw(self):
        """Draw game elements"""
        self.SCREEN.fill(self.BLACK)
        self.SCREEN.blit(self.background, (0, 0)) 
    
        # Draw walls
        if self.wall_images:
            left_wall_x = self.SCREEN_WIDTH / 2.1 - (self.ROWS * self.COLUMN_SPACING / 2) - self.wall_width
            right_wall_x = self.SCREEN_WIDTH / 1.5+ (self.ROWS * self.COLUMN_SPACING / 3) + self.wall_width
        
        self.SCREEN.blit(self.wall_images['left'], (left_wall_x, 0))
        self.SCREEN.blit(self.wall_images['right'], (right_wall_x, 0))
    
        # Draw pegs
        peg_image = pygame.image.load("img/peg.png")
        peg_image = pygame.transform.scale(peg_image, (self.PEG_RADIUS * 2, self.PEG_RADIUS * 2))
        for peg in self.pegs:
            self.SCREEN.blit(peg_image, (int(peg[0] - self.PEG_RADIUS), int(peg[1] - self.PEG_RADIUS)))
    
        # Draw buckets
        for bucket in self.buckets:
            color = self.GREEN if bucket['win'] else self.RED
            pygame.draw.rect(self.SCREEN, color, 
                             (bucket['x'], self.SCREEN_HEIGHT - 50, bucket['width'], 50))
    
        # Draw ball
        if self.ball:
            ball_image = pygame.image.load("img/ball.png")
            ball_image = pygame.transform.scale(ball_image, (self.BALL_RADIUS * 2, self.BALL_RADIUS * 2))
            self.SCREEN.blit(ball_image, (int(self.ball['x'] - self.BALL_RADIUS), int(self.ball['y'] - self.BALL_RADIUS)))

    def check_game_over(self):
        """Checks if ball has reached bottom"""
        if self.ball['y'] >= self.SCREEN_HEIGHT - 50:
            for bucket in self.buckets:
                if (bucket['x'] <= self.ball['x'] <= bucket['x'] + bucket['width']):
                    return bucket['win']
            return False

        return None

    def play(self, current_tokens):
        """Main game loop"""
        pygame.init()
        self.current_tokens = current_tokens
        clock = pygame.time.Clock()
        
        while True:
            bet_amount = get_bet.get_bet_amount(self.SCREEN, current_tokens)

            if bet_amount is None:
                return current_tokens
            
            self.background = pygame.image.load("img/red1.jpg")
            self.background = pygame.transform.scale(self.background, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

            self.load_wall_images()

            self.create_pegs()
            self.create_ball()
            self.create_buckets()

            running = True
            game_over = False
            win = None

            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return current_tokens

                    if event.type == pygame.KEYDOWN and not game_over:
                        self.ball['vx'] = random.uniform(-1, 1)

                if not game_over:
                    self.update_ball()
                    game_result = self.check_game_over()

                    if game_result is not None:
                        game_over = True
                        win = game_result

                self.draw()
                pygame.display.flip()
                clock.tick(60)

                if game_over:
                    if win:
                        self.current_tokens += bet_amount
                        self.show_result_dialog("You Win!", True)
                    else:
                        self.current_tokens -= bet_amount
                        self.show_result_dialog("You Lose!", False)
                    break

            current_tokens = self.current_tokens

            if current_tokens <= 0:
                break

        return current_tokens


def play(current_tokens):
    flinko_game = Flinko()
    return flinko_game.play(current_tokens)