import pygame
import random
import sys
import os

# Initialize Pygame
pygame.init()

# Window and title
screen_width = 600
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Cockroach Game")

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# Function to roll the dice
def roll_dice():
    dice_sound.play()
    results = [random.randint(1, 6) for _ in range(5)]
    return results

# Resource path handling function
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Load dice images
asset_dice = resource_path('assets/images/dice')
dice_images = [pygame.image.load(f'{asset_dice}{i}.png') for i in range(1, 7)]

#Background
asset_background = resource_path('assets\images\Cockroach.png')
backround = pygame.image.load(asset_background)

# Load dice rolling sound
asset_dice_sound = resource_path('assets/sounds/dice.mp3')
dice_sound = pygame.mixer.Sound(asset_dice_sound)

# Predefined positions for the green circle
green_circle_positions = [(240, 585)]
blue_circle_positions = [(171, 27) ,(219, 112), (269, 111), (318, 29), (246, 165), (194, 223), (301, 221)]
def gameloop():
    in_game = True
    screen.blit(backround, (0, 0))
    green_circle_position = None
    blue_circle_position = None

    while in_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                in_game = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_coordinates = pygame.mouse.get_pos()
                print("Mouse coordinates", mouse_coordinates)
                if dice_rect.collidepoint(event.pos):
                    results = roll_dice()
                    #print(f"Results: {results}")
                    for i, result in enumerate(results):
                        screen.blit(dice_images[result - 1], (500, 25 + i * 100))
                    ones_count = sum(1 for result in results if result == 1)
                    if ones_count == 3:
                        if len(green_circle_positions) >= 1:
                            green_circle_position = green_circle_positions.pop(0)
                            pygame.draw.circle(screen, GREEN, green_circle_position, 25)
                    if ones_count == 2:
                        if len(blue_circle_positions) >= 1:
                            blue_circle_position = blue_circle_positions.pop(0)
                            pygame.draw.circle(screen, BLUE, blue_circle_position, 25)
                    print("Number of ones:", ones_count)
                    pygame.display.flip()

         # Draw a button to roll the dice
        dice_rect = pygame.draw.rect(screen, RED, (25, 650, 125, 50))
        pygame.draw.rect(screen, RED, dice_rect)
        font = pygame.font.Font(None, 36)
        text = font.render("Roll Dice", True, WHITE)
        screen.blit(text, (25, 665))
        pygame.display.update()

if __name__ == "__main__":
    gameloop()
