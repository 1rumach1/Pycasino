import pygame
import sys
import random
from pygame.locals import *
import pygame.mixer
from modules import cards  
from modules import shuffled
from modules import get_bet

class Sweeper:
    def __init__(self):
        # Screen Dimensions
        self.SCREEN_WIDTH = 1024
        self.SCREEN_HEIGHT = 576
        self.SCREEN = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Card Sweeper")

        # Colors
        self.WHITE = (255, 255, 255)
        self.GRAY = (200, 200, 200)
        self.BLACK = (0, 0, 0)
        self.GREEN = (0, 128, 0)
        self.RED = (255, 0, 0)
        self.BLUE = (0, 0, 255)
        self.YELLOW = (255, 215, 0)

        # Fonts
        self.FONT = pygame.font.Font(None, 36)
        self.LARGE_FONT = pygame.font.Font(None, 60)

        # Game state variables
        self.current_tokens = 0
        self.background = None
        self.card_images = None
        self.clock = pygame.time.Clock()

        # Grid settings
        self.GRID_ROWS = 5
        self.GRID_COLS = 12
        self.CARD_WIDTH = 70
        self.CARD_HEIGHT = int(self.CARD_WIDTH * 1.4)
        self.GRID_MARGIN = 10

    def create_game_grid(self):
        """Create the game grid with cards and jokers"""
        # Create a full deck of cards
        deck = [f"{suit}_{rank}" for suit in ['hearts', 'diamonds', 'clubs', 'spades'] 
                for rank in ['ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king']]
        
        # Add 8 jokers
        deck.extend(['joker_red'] * 4 + ['joker_black'] * 4)
        
        # Shuffle the deck
        random.shuffle(deck)
        
        # Create grid
        grid = [[None for _ in range(self.GRID_COLS)] for _ in range(self.GRID_ROWS)]
        card_index = 0
        
        for row in range(self.GRID_ROWS):
            for col in range(self.GRID_COLS):
                if card_index < len(deck):
                    grid[row][col] = {
                        'card': deck[card_index],
                        'revealed': False
                    }
                    card_index += 1
        
        return grid

    def draw_grid(self, grid):
        """Draw the grid of cards"""
        card_back = pygame.image.load('modules/cardss/card_back.png')
        card_back = pygame.transform.scale(card_back, (self.CARD_WIDTH, self.CARD_HEIGHT))
        
        for row in range(self.GRID_ROWS):
            for col in range(self.GRID_COLS):
                cell = grid[row][col]
                if cell:
                    x = col * (self.CARD_WIDTH + self.GRID_MARGIN) + 50
                    y = row * (self.CARD_HEIGHT + self.GRID_MARGIN) + 40
                    
                    if cell['revealed']:
                        # Draw revealed card
                        card_image = self.card_images[cell['card']]
                        card_image = pygame.transform.scale(card_image, (self.CARD_WIDTH, self.CARD_HEIGHT))
                        self.SCREEN.blit(card_image, (x, y))
                    else:
                        # Draw card back
                        self.SCREEN.blit(card_back, (x, y))

    def get_grid_position(self, pos):
        """Convert mouse position to grid coordinates"""
        x, y = pos
        for row in range(self.GRID_ROWS):
            for col in range(self.GRID_COLS):
                cell_x = col * (self.CARD_WIDTH + self.GRID_MARGIN) + 50
                cell_y = row * (self.CARD_HEIGHT + self.GRID_MARGIN) + 50
                
                cell_rect = pygame.Rect(cell_x, cell_y, self.CARD_WIDTH, self.CARD_HEIGHT)
                if cell_rect.collidepoint(x, y):
                    return row, col
        return None

    def check_game_status(self, grid):
        """Check if the game is won or lost"""
        joker_found = False
        for row in range(self.GRID_ROWS):
            for col in range(self.GRID_COLS):
                cell = grid[row][col]
                if cell and cell['revealed'] and 'joker' in cell['card']:
                    joker_found = True
        
        # Only return 'lost' after the card is revealed
        if joker_found:
            return 'lost'
        
        # Check if all non-joker cards are revealed
        non_joker_count = sum(1 for row in grid for cell in row if cell and 'joker' not in cell['card'])
        revealed_non_joker_count = sum(1 for row in grid for cell in row if cell and 'joker' not in cell['card'] and cell['revealed'])
        
        return 'won' if revealed_non_joker_count == non_joker_count else 'ongoing'

    def show_game_result(self, result):
        """Show game result dialog"""
        pygame.mixer.init()
        
        # Choose sound based on result
        if result == 'won':
            sound = pygame.mixer.Sound("sounds/win.mp3")
            result_message = "You Win!"
        else:
            sound = pygame.mixer.Sound("sounds/lose.mp3")
            result_message = "Game Over!"
        
        sound.play()
        
        dialog_width, dialog_height = 450, 250
        dialog_x = (self.SCREEN_WIDTH - dialog_width) // 2
        dialog_y = (self.SCREEN_HEIGHT - dialog_height) // 2
        
        exit_button_image = pygame.image.load("img/exit_button.png")
        exit_button_image = pygame.transform.scale(exit_button_image, (100, 50))
        exit_button = pygame.Rect(dialog_x + (dialog_width - 100) // 2, dialog_y + 150, 100, 50)
        
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == MOUSEBUTTONDOWN:
                    if exit_button.collidepoint(event.pos):
                        return
            
            # Create a semi-transparent surface for the dialog
            dialog_surface = pygame.Surface((dialog_width, dialog_height), pygame.SRCALPHA)
            dialog_surface.fill((255, 255, 255, 100))  
            
            # Optional: Add a border
            border_color = (*self.BLACK, 220)  # Black border with some transparency
            pygame.draw.rect(dialog_surface, border_color, dialog_surface.get_rect(), 5)
    
            # Draw the result message
            result_text = self.LARGE_FONT.render(result_message, True, self.RED)
            result_rect = result_text.get_rect(center=(dialog_width // 2, 50))
            dialog_surface.blit(result_text, result_rect)
            # Draw exit button
            dialog_surface.blit(exit_button_image, (exit_button.x - dialog_x, exit_button.y - dialog_y))
            
            # Blit dialog to screen
            self.SCREEN.blit(dialog_surface, (dialog_x, dialog_y))
            
            pygame.display.flip()
            self.clock.tick(30)

    def play(self, current_tokens):
        """Main game loop"""
        pygame.init()
        pygame.mixer.init() 
        self.current_tokens = current_tokens
    
        # Get bet amount first
        bet_amount = get_bet.get_bet_amount(self.SCREEN, current_tokens)
    
        # If user chooses to exit
        if bet_amount is None:
            return current_tokens
    
        # Load background and card images
        self.background = pygame.image.load("img/wood4.jpg")
        self.background = pygame.transform.scale(self.background, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.card_images = cards.load_card_images(include_jokers=True)
        
        shuffled.create_shuffle_animation(self.SCREEN, self.background)
    
        # Create game grid
        grid = self.create_game_grid()
    
        # Game loop
        running = True
        joker_revealed = False  # New flag to track joker reveal
        while running:
            # Event handling
            for event in pygame.event.get():
                if event.type == QUIT:
                    return self.current_tokens
                
                if event.type == MOUSEBUTTONDOWN:
                    # Get grid position of mouse click
                    grid_pos = self.get_grid_position(event.pos)
                    if grid_pos:
                        row, col = grid_pos
                        cell = grid[row][col]
                        if cell and not cell['revealed']:
                            cell['revealed'] = True
                            
                            # Check game status
                            game_status = self.check_game_status(grid)
                            if game_status == 'lost':
                                # Redraw the screen to show the joker card before dialogue
                                self.SCREEN.blit(self.background, (0, 0))
                                self.draw_grid(grid)
                                pygame.display.flip()
                                pygame.time.delay(1000)  # Small delay to ensure card is visible
                                
                                self.show_game_result('lost')
                                self.current_tokens -= bet_amount
                                running = False
                            elif game_status == 'won':
                                self.show_game_result('won')
                                self.current_tokens += bet_amount
                                running = False
    
            # Draw background
            self.SCREEN.blit(self.background, (0, 0))
    
            # Draw grid
            self.draw_grid(grid)
    
            # Update display
            pygame.display.flip()
            self.clock.tick(30)
    
        return self.current_tokens

def play(current_tokens):
    card_sweeper = Sweeper()
    return card_sweeper.play(current_tokens)