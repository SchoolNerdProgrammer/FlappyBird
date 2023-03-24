import pygame
from pygame.locals import *

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 432
screen_height = 468

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Flappy Alien (Earthquake DLC)")

# game variables
ground_scroll = 0
scroll_speed = 1.5

# load images
bg = pygame.image.load("space background.png")
ground_img = pygame.image.load("cartoon ground.png")
ground_img = pygame.transform.scale(ground_img, (1500, 468))


# alien class
class Alien(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1, 4):
            img = pygame.image.load(f"alien thing{num}.png")  # working - need to create an alien to flap the wings of.
            img = pygame.transform.scale(img, (64, 64))
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0

    def update(self):
        self.counter += 1
        flap_cooldown = 5
        self.vel += 0.5
        if self.vel > 8:
            self.vel = 8
        if self.rect.bottom < 390:
            self.rect.y += int(self.vel)

        # jump
        if pygame.mouse.get_pressed()[0] == 1:
            self.vel = -10

        if self.counter > flap_cooldown:
            self.counter = 0
            self.index += 1
            if self.index == 3:
                self.index = 0
        self.image = self.images[self.index]


bird_group = pygame.sprite.Group()

flappy = Alien(50, int(screen_height) / 2)

bird_group.add(flappy)

bird_group.draw(screen)
bird_group.update()

run = True
while run:

    clock.tick(fps)

    # background image drawn
    screen.blit(bg, (0, 0))

    # draw the alien bird thing
    bird_group.draw(screen)
    bird_group.update()

    # draw and scroll ground
    screen.blit(ground_img, (ground_scroll, 180))
    ground_scroll -= scroll_speed
    if abs(ground_scroll) > 1000:
        ground_scroll = 0

    # event of quitting the game window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # update the game window
    pygame.display.update()