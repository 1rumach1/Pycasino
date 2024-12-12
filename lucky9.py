import pygame
import sys
import random
from pygame.locals import *
import pygame.mixer
from modules import cards  
from modules import shuffled
from modules import get_bet

class Lucky9:
    def __init__(self):
        # Screen Dimensions
        self.SCREEN_WIDTH = 1024
        self.SCREEN_HEIGHT = 576
        self.SCREEN = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Lucky 9")

        # Colors
        self.WHITE = (255, 255, 255)
        self.GRAY = (200, 200, 200)
        self.BLACK = (0, 0, 0)
        self.GREEN = (0, 128, 0)
        self.RED = (255, 0, 0)
        self.BLUE = (0, 0, 255)
        self.LIGHT_GREEN = (144, 238, 144)
        self.LIGHT_RED = (255, 160, 122)
        self.YELLOW = (255, 215, 0)

        # Fonts
        self.FONT = pygame.font.Font(None, 36)
        self.INPUT_FONT = pygame.font.Font(None, 32)
        self.LARGE_FONT = pygame.font.Font(None, 48)

        # Game state variables
        self.current_tokens = 0
        self.background = None
        self.card_images = None
        self.clock = pygame.time.Clock()

    def show_result_dialog(self, result_message, player_hand_value, dealer_hand_value):
        """Display a semi-transparent result dialog with the game's outcome, hand values, and an Exit button."""
        pygame.mixer.init()
    
        # Load sound effects
        if result_message == "You Win!":
            sound = pygame.mixer.Sound("sounds/win.mp3")
        elif result_message == "Dealer Wins!":
            sound = pygame.mixer.Sound("sounds/lose.mp3")
        else: 
            sound = pygame.mixer.Sound("sounds/draw.mp3")
    
        sound.play()
        
        dialog_width, dialog_height = 450, 250
        dialog_x = (self.SCREEN_WIDTH - dialog_width) // 2
        dialog_y = (self.SCREEN_HEIGHT - dialog_height) // 2
    
        exit_button_image = pygame.image.load("img/exit_button.png")
        exit_button_image = pygame.transform.scale(exit_button_image, (100, 50))
        exit_button = pygame.Rect(dialog_x + (dialog_width - 100) // 2, dialog_y + 200, 100, 50)
    
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
    
                if event.type == MOUSEBUTTONDOWN:
                    if exit_button.collidepoint(event.pos):
                        return  
                    
            dialog_surface = pygame.Surface((dialog_width, dialog_height), pygame.SRCALPHA)
            dialog_surface.fill((255, 255, 255, 100))  
            
            border_color = (*self.BLACK, 220)  
            pygame.draw.rect(dialog_surface, border_color, dialog_surface.get_rect(), 5)
    
            result_text = self.LARGE_FONT.render(result_message, True, self.BLACK)
            result_rect = result_text.get_rect(center=(dialog_width // 2, 50))
            dialog_surface.blit(result_text, result_rect)
    
            player_text = self.FONT.render(f"Your Hand Value: {player_hand_value}", True, self.BLACK)
            player_rect = player_text.get_rect(center=(dialog_width // 2, 100))
            dialog_surface.blit(player_text, player_rect)
    
            dealer_text = self.FONT.render(f"Dealer Hand Value: {dealer_hand_value}", True, self.BLACK)
            dealer_rect = dealer_text.get_rect(center=(dialog_width // 2, 150))
            dialog_surface.blit(dealer_text, dealer_rect)
    
            dialog_surface.blit(exit_button_image, (exit_button.x - dialog_x, exit_button.y - dialog_y))
    
            self.SCREEN.blit(dialog_surface, (dialog_x, dialog_y))
    
            pygame.display.flip()
            self.clock.tick(30)

    def calculate_card_value(self, card):
        """Calculate the value of a card for Lucky 9."""
        rank = card.split('_')[1]
        if rank in ['jack', 'queen', 'king']:
            return 0
        elif rank == 'ace':
            return 1
        else:
            return int(rank)

    def calculate_hand_value(self, hand):
        """Calculate the total value of a hand, keeping only the ones digit."""
        total = sum(self.calculate_card_value(card) for card in hand)
        return total % 10

    def draw_text(self, text, color, x, y):
        """Render text on the screen"""
        text_surface = self.FONT.render(text, True, color)
        text_rect = text_surface.get_rect(topleft=(x, y))
        self.SCREEN.blit(text_surface, text_rect)

    def draw_cards(self, hand, start_y, is_hidden=False):
        """Draw cards on the screen"""
        card_width = 100
        card_spacing = 20
        start_x = (self.SCREEN_WIDTH - (len(hand) * (card_width + card_spacing) - card_spacing)) // 2

        for i, card in enumerate(hand):
            if is_hidden and i == 1:
                card_back = pygame.image.load('modules/cardss/card_back.png')
                card_back = pygame.transform.scale(card_back, (card_width, int(card_width * 1.4)))
                self.SCREEN.blit(card_back, (start_x + i * (card_width + card_spacing), start_y))
            else:
                card_image = self.card_images[card]
                card_image = pygame.transform.scale(card_image, (card_width, int(card_width * 1.4)))
                self.SCREEN.blit(card_image, (start_x + i * (card_width + card_spacing), start_y))
  
    def load_background(self):
        """Load and scale background image"""
        self.background = pygame.image.load("img/wood.jpg")
        self.background = pygame.transform.scale(self.background, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

    def play(self, current_tokens):
        """Main game loop"""
        pygame.init()
        pygame.mixer.init() 
        self.current_tokens = current_tokens

        click_sound = pygame.mixer.Sound("sounds/click.mp3")

        self.load_background()

        draw_button_image = pygame.image.load("img/draw.png")
        draw_button_image = pygame.transform.scale(draw_button_image, (200, 50))
        stay_button_image = pygame.image.load("img/stay.png")
        stay_button_image = pygame.transform.scale(stay_button_image, (200, 50))

        # Game loop 
        while True:
            bet_amount = get_bet.get_bet_amount(self.SCREEN, current_tokens)

            if bet_amount is None:
                return current_tokens

            if bet_amount == 0:
                continue

            self.card_images = cards.load_card_images()

            shuffled.create_shuffle_animation(self.SCREEN, self.background)

            deck = [f"{suit}_{rank}" for suit in ['hearts', 'diamonds', 'clubs', 'spades'] 
                    for rank in ['ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king']]

            draw_button = pygame.Rect(self.SCREEN_WIDTH // 2 + 250, self.SCREEN_HEIGHT - 250, 200, 50)
            self.stay_button = pygame.Rect(self.SCREEN_WIDTH // 2 + 250, self.SCREEN_HEIGHT - 150, 200, 50)

            # Game states
            player_hand = []
            dealer_hand = []
            game_over = False
            result_message = ""

            random.shuffle(deck)
            player_hand = [deck.pop(), deck.pop()]
            dealer_hand = [deck.pop(), deck.pop()]

            # Main game loop
            running = True
            while running:
                self.SCREEN.blit(self.background, (0, 0))

                for event in pygame.event.get():
                    if event.type == QUIT:
                        return self.current_tokens

                    if event.type == MOUSEBUTTONDOWN and not game_over:
                        # Draw card button
                        if draw_button.collidepoint(event.pos) and len(player_hand) < 3:
                            click_sound.play()
                            player_hand.append(deck.pop())

                            if len(player_hand) == 3:
                                while self.calculate_hand_value(dealer_hand) < 5 and len(dealer_hand) < 3:
                                    dealer_hand.append(deck.pop())

                                player_value = self.calculate_hand_value(player_hand)
                                dealer_value = self.calculate_hand_value(dealer_hand)

                                if player_value > dealer_value:
                                    result_message = "You Win!"
                                    self.current_tokens += bet_amount
                                elif player_value < dealer_value:
                                    result_message = "Dealer Wins!"
                                    self.current_tokens -= bet_amount
                                else:
                                    result_message = "It's a Tie!"

                                game_over = True

                        # Stay button
                        if self.stay_button.collidepoint(event.pos) and len(player_hand) < 3:
                            click_sound.play()
                            while self.calculate_hand_value(dealer_hand) < 5 and len(dealer_hand) < 3:
                                dealer_hand.append(deck.pop())

                            player_value = self.calculate_hand_value(player_hand)
                            dealer_value = self.calculate_hand_value(dealer_hand)

                            if player_value > dealer_value:
                                result_message = "You Win!"
                                self.current_tokens += bet_amount
                            elif player_value < dealer_value:
                                result_message = "Dealer Wins!"
                                self.current_tokens -= bet_amount
                            else:
                                result_message = "It's a Tie!"

                            game_over = True

                    if event.type == KEYDOWN and event.key == K_RETURN and not game_over:
                        while self.calculate_hand_value(dealer_hand) < 5 and len(dealer_hand) < 3:
                            dealer_hand.append(deck.pop())

                        player_value = self.calculate_hand_value(player_hand)
                        dealer_value = self.calculate_hand_value(dealer_hand)

                        if player_value > dealer_value:
                            result_message = "You Win!"
                            self.current_tokens += bet_amount
                        elif player_value < dealer_value:
                            result_message = "Dealer Wins!"
                            self.current_tokens -= bet_amount
                        else:
                            result_message = "It's a Tie!"

                        game_over = True

                self.draw_cards(player_hand, self.SCREEN_HEIGHT // 2 + 100)

                self.draw_cards(dealer_hand, 100, not game_over)

                self.SCREEN.blit(draw_button_image, draw_button.topleft)
                self.SCREEN.blit(stay_button_image, self.stay_button.topleft)

                self.draw_text(f"Tokens: {self.current_tokens}", self.YELLOW, 10, 10)
                self.draw_text(f"Bet: {bet_amount}", self.RED, 10, 50)
                self.draw_text(f"Player Hand Value: {self.calculate_hand_value(player_hand)}", self.WHITE, 10, self.SCREEN_HEIGHT - 50)

                if game_over:
                    # Reveal all cards
                    running_reveal = True
                    reveal_start_time = pygame.time.get_ticks()

                    while running_reveal:
                        self.SCREEN.blit(self.background, (0, 0))
                        self.draw_cards(player_hand, self.SCREEN_HEIGHT // 2 + 100)
                        self.draw_cards(dealer_hand, 100)
                        self.SCREEN.blit(draw_button_image, draw_button)
                        self.SCREEN.blit(stay_button_image, self.stay_button)

                        self.draw_text(f"Tokens: {self.current_tokens}", self.YELLOW, 10, 10)
                        self.draw_text(f"Bet: {bet_amount}", self.RED, 10, 50)
                        self.draw_text(f"Player Hand Value: {self.calculate_hand_value(player_hand)}", self.WHITE, 10, self.SCREEN_HEIGHT - 50)


                        current_time = pygame.time.get_ticks()
                        if current_time - reveal_start_time >= 2000:  
                            running_reveal = False

                        pygame.display.flip()
                        self.clock.tick(30)

                    self.show_result_dialog(result_message, player_value, dealer_value)
                    break


                pygame.display.flip()
                self.clock.tick(30)

            # Update current_tokens for next round
            current_tokens = self.current_tokens

            # If tokens are zero, break the outer loop
            if current_tokens <= 0:
                break

        return current_tokens

def play(current_tokens):
    lucky9_game = Lucky9()
    return lucky9_game.play(current_tokens)