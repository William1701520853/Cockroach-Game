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
YELLOW = (255,255,153)
NONE = (0, 0, 0, 0)

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
black_circle_positions = [(121, 169), (92, 267), (86, 425), (120, 558), (202, 291), (180, 357), (162, 425), (212, 527), (291, 526), (368, 550), (406, 421), (329, 427), (315, 354), (295, 285), (406, 265), (372, 170)]

players = [
    {"name": "Jugador 1", "money": 1000, "has_rolled": False},
    {"name": "Jugador 2", "money": 1000, "has_rolled": False}
]

current_player = 0

# Variable para rastrear si el jugador ha lanzado los dados

def gameloop():
    in_game = True
    screen.blit(backround, (0, 0))
    green_circle_position = None
    blue_circle_position = None
    black_circle_position = None

    player_money = 1000 
    has_rolled = False
    textPlayer = ''
    dice_rect = pygame.draw.rect(screen, NONE, NONE)
    pay_rect = pygame.draw.rect(screen, NONE, NONE)

    green_circle_positions_aux = list(green_circle_positions)
    blue_circle_positions_aux = list(blue_circle_positions)
    black_circle_positions_aux = list(black_circle_positions)

    font_money = pygame.font.Font(None, 36)
    while in_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                in_game = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_coordinates = pygame.mouse.get_pos()
                #print("Mouse coordinates", mouse_coordinates)
                if restart_rect.collidepoint(event.pos):
                    # Limpiar la pantalla
                    screen.fill(BLACK)
                    screen.blit(backround, (0, 0))
                    player_money = 1000
                    has_rolled = False
                    green_circle_positions_aux = list(green_circle_positions)
                    blue_circle_positions_aux = list(blue_circle_positions)
                    black_circle_positions_aux = list(black_circle_positions)
                    
                    
                    textPlayer = ""
                    restart_rect = pygame.draw.rect(screen, WHITE, (0, 700, 600, 100))
                    pygame.draw.rect(screen, BLACK, restart_rect)

                if dice_rect.collidepoint(event.pos):
                    if players[current_player]["has_rolled"]:
                        textPlayer = f"{players[current_player]['name']} ya ha lanzado los dados. Debe pagar si no obtiene un 1."
                    else:
                        results = roll_dice()
                        #print(f"Results: {results}")
                        for i, result in enumerate(results):
                            screen.blit(dice_images[result - 1], (500, 25 + i * 100))
                        ones_count = sum(1 for result in results if result == 1)
                        six_count = sum(1 for result in results if result == 6)
                        if ones_count == 3:
                            if len(green_circle_positions_aux) >= 1:
                                green_circle_position = green_circle_positions_aux.pop(0)
                                pygame.draw.circle(screen, GREEN, green_circle_position, 25)
                        if ones_count == 2:
                            if len(blue_circle_positions_aux) >= 1:
                                blue_circle_position = blue_circle_positions_aux.pop(0)
                                pygame.draw.circle(screen, BLUE, blue_circle_position, 25)
                        if ones_count == 1:
                            if len(black_circle_positions_aux) >= 1:
                                print('IN COUNT black_circle_positions_aux', black_circle_positions_aux)
                                black_circle_position = black_circle_positions_aux.pop(0)
                                pygame.draw.circle(screen, BLACK, black_circle_position, 25)
                        if ones_count >= 1:
                            players[current_player]["has_rolled"] = True
                            current_player = (current_player + 1) % len(players)

                        if ones_count == 0:
                            # El jugador no obtuvo ningún 1, debe pagar una multa
                            players[current_player]["has_rolled"] = True
                            textPlayer = 'Debes pagar si no obtienes 1.'
                            

                            
                    #print("Number of ones:", ones_count)
                if pay_rect.collidepoint(event.pos):
                    player_money -= 100  # Puedes ajustar el costo de la multa
                    has_rolled = False
                    textPlayer = ""
                    restart_rect = pygame.draw.rect(screen, WHITE, (0, 700, 600, 100))
                    pygame.draw.rect(screen, BLACK, restart_rect)
                    

                pygame.display.flip()
                
        font = pygame.font.Font(None, 36)
        # Draw a button to roll the dice
        
        
        if not has_rolled:
            dice_rect = pygame.draw.rect(screen, RED, (25, 650, 125, 50))
            textRollDice = font.render("Roll Dice", True, WHITE)
            pygame.draw.rect(screen, RED, dice_rect)
            hide_rect = pygame.draw.rect(screen, BLACK, (325, 650, 125, 50))
            pay_rect = pygame.draw.rect(screen, NONE, NONE)

            pygame.draw.rect(screen, BLACK, hide_rect)
            screen.blit(textRollDice, (25, 665))


        #Draw a button to reset
        restart_rect = pygame.draw.rect(screen, WHITE, (175, 650, 125, 50))
        pygame.draw.rect(screen, BLUE, restart_rect)
        textReset = font.render("Reset", True, WHITE)

        #Draw a pay button
        
        if has_rolled:
            pay_rect = pygame.draw.rect(screen, YELLOW, (325, 650, 125, 50))
            textPay = font.render("PAY", True, BLACK)
            pygame.draw.rect(screen, YELLOW, pay_rect)
            hide_rect = pygame.draw.rect(screen, BLACK, (25, 650, 125, 50))
            dice_rect = pygame.draw.rect(screen, NONE, NONE)
            pygame.draw.rect(screen, BLACK, hide_rect)
            screen.blit(textPay, (325, 665))


        screen.blit(textReset, (175, 665))
        textPlayerRender = font.render(textPlayer, True, WHITE)
        screen.blit(textPlayerRender, (25, 700))
        textMoney = font_money.render(f"Dinero: ${player_money}", True, WHITE)
        screen.blit(textMoney, (25, 750))
        pygame.display.update()

if __name__ == "__main__":
    gameloop()
