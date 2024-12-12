import pygame
import sys
import lucky9
import war
import toss_coin
import sweeper
import blackjack
import flinko
from pygame.locals import *
import pygame.mixer

# Initialize Pygame
pygame.init()

# Screen Dimensions
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 576
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("PYCASINO")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 255) 
GRAY = (200, 200, 200)
ORANGE = (255, 165, 0)
MAGENTA = (255, 0, 255)
YELLOW = (255, 215, 0)

# Fonts
TITLE_FONT = pygame.font.Font(None, 30)
BUTTON_FONT = pygame.font.Font(None, 23)

class Button:
    def __init__(self, x, y, width, height, text, color, text_color=BLACK):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.font = BUTTON_FONT
        self.callback = None

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)  # Border
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

class RoundedButton(Button):
    def __init__(self, x, y, width, height, text, color, text_color=BLACK):
        super().__init__(x, y, width, height, text, color, text_color)
        self.radius = 10

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=self.radius)
        pygame.draw.rect(screen, BLACK, self.rect, 2, border_radius=self.radius)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

class ButtonContainer:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.buttons = []
        self.tokens = 0

    def add_button(self, text, callback, color=BLUE, text_color=BLACK):
        button_width = 125
        button_height = 35
        button_x = self.rect.x + (self.rect.width - button_width) // 2
        button_y = self.rect.y + len(self.buttons) * (button_height + 10) + 40  # Added offset for token display
        button = RoundedButton(button_x, button_y, button_width, button_height, text, color, text_color)
        button.callback = callback
        self.buttons.append(button)

    def draw(self, screen):
        # Create a surface with per-pixel alpha
        container_surface = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        container_surface.fill((0, 0, 0, 100))  

        # Blit the transparent surface onto the screen
        screen.blit(container_surface, self.rect)

        # Draw the container border
        pygame.draw.rect(screen, BLACK, self.rect, 2)

        # Draw token display with background and border
        token_bg_rect = pygame.Rect(
            self.rect.x + 10, 
            self.rect.y + 10, 
            self.rect.width - 20, 
            30
        )

        # Draw token background with solid white background
        pygame.draw.rect(screen, RED, token_bg_rect)

        # Draw token background border
        pygame.draw.rect(screen, BLACK, token_bg_rect, 2)

        # Draw token text
        token_surface = TITLE_FONT.render(f'Your Tokens: {self.tokens}', True, BLACK)
        token_rect = token_surface.get_rect(center=token_bg_rect.center)
        screen.blit(token_surface, token_rect)

        # Draw the buttons
        for button in self.buttons:
            button.draw(screen)

    def handle_click(self, pos):
        for button in self.buttons:
            if button.is_clicked(pos):
                button.callback()
                return

    def add_tokens(self, amount):
        self.tokens += amount

    def check_tokens(self):
        if self.tokens <= 0:
            print("You need to buy tokens first!")
            return False
        return True

class PyCasino:
    def __init__(self):
        self.button_container = ButtonContainer(SCREEN_WIDTH // 1 - 410, SCREEN_HEIGHT // 3.5, 300, 400)
        self.button_container.add_button('Buy Tokens', self.buy_tokens)
        self.button_container.add_button('Lucky 9', self.play_lucky9, color=GREEN)
        self.button_container.add_button('War', self.play_war, color=MAGENTA)
        self.button_container.add_button('Toss Coin', self.play_toss_coin, color=YELLOW)
        self.button_container.add_button('Sweeper', self.play_sweeper ,color=GRAY)
        self.button_container.add_button('Flinko', self.play_flinko, color=RED)
        self.button_container.add_button('Blackjack', self.play_blackjack, color=WHITE)
        self.button_container.add_button('Exit', self.exit_game, color=ORANGE)

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        self.button_container.draw(screen)

    def run(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:  
                        self.button_container.handle_click(event.pos)

            self.draw(SCREEN)
            pygame.display.flip()
            clock.tick(30)

        pygame.quit()
        sys.exit()

    def buy_tokens(self):
        self.button_container.add_tokens(100)
        print(f"Tokens purchased. Total tokens: {self.button_container.tokens}")

    def play_lucky9(self):
        if self.button_container.check_tokens():
            self.button_container.tokens = lucky9.play(self.button_container.tokens)

    def play_war(self):
        if self.button_container.check_tokens():
            self.button_container.tokens = war.play(self.button_container.tokens)

    def play_toss_coin(self):
        if self.button_container.check_tokens():
            self.button_container.tokens = toss_coin.play(self.button_container.tokens)

    def play_sweeper(self):
        if self.button_container.check_tokens():
            self.button_container.tokens = sweeper.play(self.button_container.tokens)
            
    def play_flinko(self):
        if self.button_container.check_tokens():
            self.button_container.tokens = flinko.play(self.button_container.tokens)

    def play_blackjack(self):
        if self.button_container.check_tokens():
            self.button_container.tokens = blackjack.play(self.button_container.tokens)

    def exit_game(self):
        pygame.quit()
        sys.exit()

    def load_background(self):
        self.background = pygame.image.load("img/casino2.jpg")
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))

    def load_background_music(self):
        pygame.mixer.music.load("sounds/bg.mp3") 
        pygame.mixer.music.set_volume(0.4)  
        pygame.mixer.music.play(-1)
        
def main():
    casino = PyCasino()
    casino.load_background()
    casino.load_background_music()
    casino.run()

if __name__ == "__main__":
    main()