import pygame
import random

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 432
screen_height = 468

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Flappy Alien")

# game variables
ground_scroll = 0
scroll_speed = 3  # 3
flying = False
game_over = False
pipe_gap = 130  # 130
pipe_frequency = 2000  # ms #2000
last_pipe = pygame.time.get_ticks() - pipe_frequency
score_counter = -2

# text font rendering
font = pygame.font.Font("freesansbold.ttf", 32)
text = font.render(f"{score_counter}", True, "white")
textRect = text.get_rect()
textRect.center = (screen_width / 2, 30)
# load images
bg = pygame.image.load("imgs/space background.png")
ground_img = pygame.image.load("imgs/cartoon ground.png")
ground_img = pygame.transform.scale(ground_img, (1500, 468))
buttom_img = pygame.image.load("imgs/erestart.png")


def reset_game():
    pipe_group.empty()
    flappy.rect.x = 50
    flappy.rect.y = int(screen_height / 2)
    counter = -2
    flappy.image = pygame.transform.rotate(flappy.images[flappy.index], 0)
    flappy.image = flappy.images[0]
    global scroll_speed
    scroll_speed = 3
    return counter


# alien class
class Alien(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1, 4):
            img = pygame.image.load(f"imgs/he alien thing{num}.png")
            img = pygame.transform.scale(img, (32, 32))
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
        self.clicked = False

    def update(self):
        self.counter += 1
        flap_cooldown = 4

        if flying:
            # gravity
            self.vel += 0.3
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom < 390:
                self.rect.y += int(self.vel)
        if not game_over and flying:
            # jump

            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                self.vel = -6
                self.rect.y += int(self.vel)
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

            # animation
            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index == 3:
                    self.index = 0
            self.image = self.images[self.index]

            # rotate the bird
            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -1)
        elif game_over:
            self.image = pygame.transform.rotate(self.images[self.index], -90)
            print("rotate")


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("imgs/pipe.png")
        self.rect = self.image.get_rect()
        # position 1 is from the top, -1 is from the bottom
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(pipe_gap / 2)]
        if position == -1:
            self.rect.topleft = [x, y + int(pipe_gap / 2)]

    def update(self):
        if not game_over:
            self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()


class Button:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):
        action = False

        # get mouse pos
        pos = pygame.mouse.get_pos()

        # check if mosue is over button
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True

        # draw button
        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action


bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

flappy = Alien(50, int(screen_height) / 2)
bird_group.add(flappy)

# create the button
button = Button(screen_width // 2 - 70, screen_height // 2 - 120, buttom_img)

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
    pipe_group.draw(screen)
    pipe_group.update()
    # ground scroll updater

    screen.blit(ground_img, (ground_scroll, 192))

    # pipe collision check
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.bottom < 0:
        game_over = True

    # ground collision check
    if flappy.rect.bottom > 389:
        game_over = True
        flying = False

    # draw and scroll ground
    if game_over == False and flying == True:

        # generate new pipes
        time_now = pygame.time.get_ticks()
        if (time_now - last_pipe) > pipe_frequency:
            pipe_height = random.randint(-80, 80)
            btm_pipe = Pipe(screen_width + 20, (int(screen_height) / 2) + pipe_height, -1)
            top_pipe = Pipe(screen_width + 20, (int(screen_height) / 2) + pipe_height, 1)
            pipe_group.add(btm_pipe, top_pipe)
            last_pipe = time_now
            score_counter += 1
            print(score_counter)
            scroll_speed += 2
        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 1000:
            ground_scroll = 0

    # check for gameover and then reset
    if game_over:
        if button.draw():
            game_over = False
            score_counter = reset_game()

    if score_counter >= 0:
        screen.blit(text, textRect)
        text = font.render(f"{score_counter + 1}", True, "white")
    # event of quitting the game window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
            flying = True
    # update the game window
    pygame.display.update()
