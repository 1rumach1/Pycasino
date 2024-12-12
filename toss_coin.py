import pygame
import sys
import random
from pygame.locals import *
import pygame.mixer
from modules import get_bet

class TossCoin:
    def __init__(self):
        # Screen Dimensions
        self.SCREEN_WIDTH = 1024
        self.SCREEN_HEIGHT = 576
        self.SCREEN = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Coin Toss")

        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.YELLOW = (255, 215, 0)
        self.RED = (255, 0, 0)

        # Fonts
        self.FONT = pygame.font.Font(None, 36)
        self.LARGE_FONT = pygame.font.Font(None, 48)

        # Game state variables
        self.current_tokens = 0
        self.background = None
        self.clock = pygame.time.Clock()

    def load_background(self):
        """Load and scale background image"""
        self.background = pygame.image.load("img/red1.jpg")
        self.background = pygame.transform.scale(self.background, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

    def draw_text(self, text, color, x, y):
        """Render text on the screen"""
        text_surface = self.FONT.render(text, True, color)
        text_rect = text_surface.get_rect(topleft=(x, y))
        self.SCREEN.blit(text_surface, text_rect)
        
    def create_coin_animation(self, result):
        pygame.mixer.init()
        shuffle_sound = pygame.mixer.Sound("sounds/coin.mp3")
        shuffle_sound.play()
        
        # Load shuffle and result images
        coin_images = [pygame.image.load(f"modules/toss/goldcoin-{i+1}.png") for i in range(6)]
        result_image = pygame.image.load(f"modules/toss/goldcoin-{result}.png")
        
        # Animation loop (single pass)
        for img in coin_images:
            scaled_img = pygame.transform.scale(img, (300, 300))
            
            self.SCREEN.blit(self.background, (0, 0))
            
            img_rect = scaled_img.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2))
            self.SCREEN.blit(scaled_img, img_rect)
            
            pygame.display.flip()
            pygame.time.delay(200)
        
        self.SCREEN.blit(self.background, (0, 0))
        
        result_image = pygame.transform.scale(result_image, (350, 350))
        result_rect = result_image.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2))
        self.SCREEN.blit(result_image, result_rect)
        pygame.display.flip()
        
        pygame.time.delay(2000)

    def show_result_dialog(self, result_message, is_win, result):
        """Display a semi-transparent result dialog with the game's outcome"""
        pygame.mixer.init()
    
        # Load sound effects
        sound = pygame.mixer.Sound("sounds/win.mp3") if is_win else pygame.mixer.Sound("sounds/lose.mp3")
        sound.play()
        
        dialog_width, dialog_height = 450, 250
        dialog_x = (self.SCREEN_WIDTH - dialog_width) // 2
        dialog_y = (self.SCREEN_HEIGHT - dialog_height) // 2
    
        # Load exit button image
        exit_button_image = pygame.image.load("img/exit_button.png")
        exit_button_image = pygame.transform.scale(exit_button_image, (100, 50))
        exit_button = pygame.Rect(dialog_x + (dialog_width - 100) // 2, dialog_y + 200, 100, 50)
    
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
    
                if event.type == MOUSEBUTTONDOWN:
                    # Check if the Exit button is clicked
                    if exit_button.collidepoint(event.pos):
                        return  
                    
            dialog_surface = pygame.Surface((dialog_width, dialog_height), pygame.SRCALPHA)
            dialog_surface.fill((255, 255, 255, 100))  
            
            border_color = (*self.BLACK, 220)  # Black border with some transparency
            pygame.draw.rect(dialog_surface, border_color, dialog_surface.get_rect(), 5)
    
            result_text = self.LARGE_FONT.render(result_message, True, self.BLACK)
            result_rect = result_text.get_rect(center=(dialog_width // 2, 100))
            dialog_surface.blit(result_text, result_rect)
            
            player_text = self.FONT.render(f"Result: {result}", True, self.BLACK)
            player_rect = player_text.get_rect(center=(dialog_width // 2, 50))
            dialog_surface.blit(player_text, player_rect)
    
            dialog_surface.blit(exit_button_image, (exit_button.x - dialog_x, exit_button.y - dialog_y))
    
            self.SCREEN.blit(dialog_surface, (dialog_x, dialog_y))
    
            pygame.display.flip()
            self.clock.tick(30)

    def play(self, current_tokens):
        """Main game loop"""
        pygame.init()
        pygame.mixer.init() 
        self.current_tokens = current_tokens
        click_sound = pygame.mixer.Sound("sounds/click.mp3")

        # Load background image
        self.load_background()

        # Load head and tail button images
        heads_button_image = pygame.image.load("img/head.png")
        heads_button_image = pygame.transform.scale(heads_button_image, (180, 80))
        tails_button_image = pygame.image.load("img/tail.png")
        tails_button_image = pygame.transform.scale(tails_button_image, (180, 80))

        # Game loop 
        while True:

            bet_amount = get_bet.get_bet_amount(self.SCREEN, current_tokens)

            if bet_amount is None:
                return current_tokens

            if bet_amount == 0:
                continue

            # Button positions
            heads_button = pygame.Rect(self.SCREEN_WIDTH // 2 - 250, self.SCREEN_HEIGHT - 250, 200, 100)
            tails_button = pygame.Rect(self.SCREEN_WIDTH // 2 + 50, self.SCREEN_HEIGHT - 250, 200, 100)

            # Game states
            game_over = False
            player_choice = None
            result = random.choice(["heads", "tails"])
            
            # Main game loop
            running = True
            while running:
                self.SCREEN.blit(self.background, (0, 0))
            
                # Event handling
                for event in pygame.event.get():
                    if event.type == QUIT:
                        return self.current_tokens
            
                    if event.type == MOUSEBUTTONDOWN and not game_over:
                        # Heads button
                        if heads_button.collidepoint(event.pos):
                            click_sound.play()
                            player_choice = "heads"
                            self.create_coin_animation(result)
                            game_over = True
            
                        # Tails button
                        if tails_button.collidepoint(event.pos):
                            click_sound.play()
                            player_choice = "tails"
                            self.create_coin_animation(result)
                            game_over = True

                # Drawing buttons
                self.SCREEN.blit(heads_button_image, heads_button.topleft)
                self.SCREEN.blit(tails_button_image, tails_button.topleft)

                # Display game information
                self.draw_text(f"Tokens: {self.current_tokens}", self.YELLOW, 10, 10)
                self.draw_text(f"Bet: {bet_amount}", self.RED, 10, 50)
                self.draw_text(" HEADS or TAILS", self.RED, self.SCREEN_WIDTH // 2 - 100, self.SCREEN_HEIGHT - 300)

                if game_over:
                    is_win = (player_choice == result)
                    if is_win:
                        result_message = "You Win!"
                        self.current_tokens += bet_amount
                    else:
                        result_message = "Dealer Wins!"
                        self.current_tokens -= bet_amount


                    self.show_result_dialog(result_message, is_win,result)

                    break

                pygame.display.flip()
                self.clock.tick(30)

            current_tokens = self.current_tokens

            if current_tokens <= 0:
                break

        return current_tokens

def play(current_tokens):
    coin_game = TossCoin()
    return coin_game.play(current_tokens)