import pygame
import sys
import math

screen = pygame.display.set_mode((750,500))
pygame.init()

clock = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    screen.fill((math.sin(clock)*127.5+127.5,255,255))

    pygame.draw.polygon(screen, (0,0,0), ((375 + math.sin(clock)*40,250 + math.cos(clock)*40),(375 + math.sin(clock + 120)*40, 250 + math.cos(clock + 120)*40,250),(375,250)))

    clock = pygame.time.get_ticks()/60

    pygame.display.flip()

"∫ [0,∞] t^{z-1}e^{-t} dt"