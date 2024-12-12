import pygame
import os

def load_card_images(include_jokers=False):
    card_images = {}
    suits = ['hearts', 'diamonds', 'clubs', 'spades']
    ranks = ['ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king']
    
    for suit in suits:
        for rank in ranks:
            image_path = f'modules/cardss/{suit}_card_{rank}.png'
            card_images[f'{suit}_{rank}'] = pygame.image.load(image_path)
    
    # Conditionally add joker images only if explicitly requested
    if include_jokers:
        joker_colors = ['red', 'black']
        for color in joker_colors:
            joker_path = f'modules/cardss/joker_{color}.png'
            if os.path.exists(joker_path):
                card_images[f'joker_{color}'] = pygame.image.load(joker_path)
    
    return card_images