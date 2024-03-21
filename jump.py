import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((750,500))
pygame.display.set_caption("RIZZLER - THE GAME")
clock = pygame.time.Clock()

class Player(pygame.sprite.GroupSingle):
    def __init__(self, y, maxvel, velocity):
        pygame.sprite.Sprite.__init__(self)
        self.y  = y
        self.maxvel = maxvel
        self.velocity = velocity

player = Player(250, 1, -1)

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.K_SPACE:
            player.velocity = 0

    screen.fill((0,0,0))

    pygame.draw.rect(screen, (255,0,0), pygame.Rect((100,player.y),(50,50)))

    player.y+=player.velocity
    player.velocity+=0.002

    if player.velocity > player.maxvel:
        player.velocity = player.maxvel

    pygame.display.update()

    #sussy amogus