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

    pygame.draw.polygon(screen, (0,0,0), ((200,300),(100,400),(300,300)))

    clock = pygame.time.get_ticks()/60

    pygame.display.flip()