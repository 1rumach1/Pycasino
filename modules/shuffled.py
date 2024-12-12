import pygame
import random
from pygame.locals import *
import pygame.mixer

def create_shuffle_animation(screen, background):

    pygame.mixer.init()
    shuffle_sound = pygame.mixer.Sound("sounds/shuffle.mp3")
    shuffle_sound.play()
    
    # Load shuffle images
    shuffle_images = [
        pygame.image.load(f"modules/deck/shuffle_{i}.png") 
        for i in range(1, 40)  
    ]
    
    num_loops = 3
    
    for _ in range(num_loops):
        random.shuffle(shuffle_images)
        
        # Animation loop
        for img in shuffle_images:
            angle = random.uniform(-15, 15)
            rotated_img = pygame.transform.rotate(img, angle)
            
            scale = random.uniform(0.8, 1.2)
            scaled_img = pygame.transform.scale(rotated_img, 
                                                (int(200 * scale), 
                                                 int(300 * scale)))
            
            # Clear screen with background
            screen.blit(background, (0, 0))
            
            # Position the image near the left side deck
            img_rect = scaled_img.get_rect(center=(100, screen.get_height() // 2))
            screen.blit(scaled_img, img_rect)
            
            # Update display
            pygame.display.flip()
            pygame.time.delay(40)
        

        pygame.time.delay(45)