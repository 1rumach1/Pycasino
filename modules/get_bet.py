import pygame
from pygame.locals import *

def get_bet_amount(screen, current_tokens):
    SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_width(), screen.get_height()
    popup_width, popup_height = 400, 300
    popup_x = (SCREEN_WIDTH - popup_width) // 2
    popup_y = (SCREEN_HEIGHT - popup_height) // 2

    # Colors and Fonts
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREEN = (0, 128, 0)
    RED = (255, 0, 0)
    YELLOW = pygame.Color('yellow')
    GOLD = pygame.Color('gold')

    font = pygame.font.Font(None, 36)
    input_font = pygame.font.Font(None, 32)

    input_box = pygame.Rect(popup_x + 100, popup_y + 150, 200, 40)
    color_inactive = WHITE
    color_active = GOLD
    color = color_inactive
    active = False
    text = ''
    error_message = ''

    popup_background = pygame.image.load("img/bet.jpg")
    popup_background = pygame.transform.scale(popup_background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    exit_button_image = pygame.image.load("img/exit_button.png")
    exit_button_image = pygame.transform.scale(exit_button_image, (100, 50))

    exit_button = pygame.Rect(popup_x + 150, popup_y + 250, 100, 50)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return None

            if event.type == MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive

                if exit_button.collidepoint(event.pos):
                    return None

            if event.type == KEYDOWN:
                if active:
                    if event.key == K_RETURN:
                        try:
                            bet = int(text)
                            if bet > 0 and bet <= current_tokens:
                                return bet
                            else:
                                error_message = "Invalid bet amount"
                                text = ''
                        except ValueError:
                            error_message = "Please enter a valid number"
                            text = ''

                    elif event.key == K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        # Drawing
        screen.blit(popup_background, (0, 0))

        # Popup background with border
        border_rect = pygame.Rect(popup_x - 5, popup_y - 5, popup_width + 10, popup_height + 10)
        pygame.draw.rect(screen, BLACK, border_rect)
        popup = pygame.Surface((popup_width, popup_height))
        popup.fill(GREEN)
        popup.set_alpha(230)
        screen.blit(popup, (popup_x, popup_y))

        # Title
        title_text = font.render("Enter Bet Amount", True, BLACK)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, popup_y + 50))
        screen.blit(title_text, title_rect)

        # Available tokens
        tokens_text = font.render(f"Available Tokens: {current_tokens}", True, BLACK)
        tokens_rect = tokens_text.get_rect(center=(SCREEN_WIDTH // 2, popup_y + 100))
        screen.blit(tokens_text, tokens_rect)

        # Input box
        txt_surface = input_font.render(text, True, color)
        input_box.w = max(200, txt_surface.get_width() + 10)
        pygame.draw.rect(screen, color, input_box, 2)
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))

        # Error message
        if error_message:
            error_text = font.render(error_message, True, RED)
            error_rect = error_text.get_rect(center=(SCREEN_WIDTH // 2, popup_y + 220))
            screen.blit(error_text, error_rect)

        # Draw Exit button
        screen.blit(exit_button_image, exit_button.topleft)

        pygame.display.flip()