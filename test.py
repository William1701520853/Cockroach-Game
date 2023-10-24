import pygame
import random
import math
import sys
import os

#Start pygame
pygame.init()

#Window size
screen_width = 600
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Cockroach Game")

# Definir colores
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
NEGRO = (0, 0, 0)
AZUL = (0, 0, 255)

# Función para tirar el dado
def tirar_dado():
    dice_sound.play()
    resultados = [random.randint(1, 6) for _ in range(5)]
    return resultados


#Function of the assets path
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)
    
#Background
asset_background = resource_path('assets\images\Cockroach.png')
backround = pygame.image.load(asset_background)

# Cargar imágenes de los dados
asset_dice = resource_path('assets\images\Cockroach.png')
imagenes_dados = [pygame.image.load(f'assets\images\dado{i}.png') for i in range(1, 7)]

#Dice sound
asset_dice_sound = resource_path('assets\sounds\dice.mp3')
dice_sound = pygame.mixer.Sound(asset_dice_sound)

def gameloop():
    in_game = True
    screen.blit(backround, (0, 0))
    while in_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                in_game = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                coordenadas_mouse = pygame.mouse.get_pos()
                print("coordenadas_mouse", coordenadas_mouse)
                if dado_rect.collidepoint(event.pos):
                    resultados = tirar_dado()
                    print(f"Resultado: {resultados}")
                    for i, resultado in enumerate(resultados):
                        screen.blit(imagenes_dados[resultado - 1], (500, 25 + i * 100))
                    cantidad_de_unos = sum(1 for resultado in resultados if resultado == 1)
                    if cantidad_de_unos == 3:
                        pygame.draw.circle(screen, VERDE, (240, 585), 25)
                    print("Cantidad de unos:", cantidad_de_unos)
                    pygame.display.flip()

         # Dibujar un botón para tirar el dado
        dado_rect = pygame.draw.rect(screen, ROJO, (25, 650, 125, 50))
        pygame.draw.rect(screen, ROJO, dado_rect)
        font = pygame.font.Font(None, 36)
        texto = font.render("Tirar Dado", True, BLANCO)
        screen.blit(texto, (25, 665))
        pygame.display.update()

gameloop()     