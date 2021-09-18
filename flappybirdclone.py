import pygame as pg
import pygame.sprite
from pygame.locals import *
import random

pg.init()

WIDTH = 1024
HEIGHT = 720

screen = pg.display.set_mode((WIDTH, HEIGHT))


class Bird(pg.sprite.Sprite):
    def __init__(self):
        super(Bird, self).__init__()
        self.surface = pg.Surface((80 / 5, 120 / 5))
        self.surface.fill((255, 0, 0))
        self.rect = self.surface.get_rect()
        self.rect.x = 1024 - 250
        self.rect.y = HEIGHT // 2
        self.jump = False
        self.acc = pg.math.Vector2(0, 0)
        self.vel = pg.math.Vector2(0, 0)
        self.pos = pg.math.Vector2(0, HEIGHT // 2)
        self.alive = True
        self.hasGravity = False

    def jump(self):
        self.jump = True

    def update(self):
        if self.hasGravity:
            self.acc = pg.math.Vector2(0, 0.5)

            if self.jump:
                self.vel.y = -10
                self.jump = False

            # self.acc += self.vel * .05

            self.vel += self.acc
            self.pos += self.vel + 0.5 * self.acc
            self.rect.center = self.pos

            self.rect.x = 1024 - 250


class PipeTop(pygame.sprite.Sprite):
    def __init__(self, x):
        super(PipeTop, self).__init__()
        self.surface = pg.surface.Surface((50, random.randint(50, HEIGHT - 150)))
        # self.surfaceBottom = pg.surface.Surface((50, (HEIGHT - self.surfaceTop.get_rect().bottom) - 150))
        self.surface.fill((0, 255, 0))
        # self.surfaceBottom.fill((0,255,0))
        self.rect = self.surface.get_rect()
        # self.rectBottom = self.surfaceBottom.get_rect()
        self.rect.top = 0
        self.rect.x = x
        # self.rectBottom.bottom = HEIGHT
        # self.rectBottom.x = x


class PipeBottom(pygame.sprite.Sprite):
    def __init__(self, x, pipeTop):
        super(PipeBottom, self).__init__()
        # self.surfaceTop = pg.surface.Surface((50, random.randint(50,HEIGHT / 2 - 20)))
        self.surface = pg.surface.Surface((50, (HEIGHT - pipeTop.surface.get_rect().bottom) - 150))
        # self.surfaceTop.fill((0,255,0))
        self.surface.fill((0, 255, 0))
        # self.rectTop = self.surfaceTop.get_rect()
        self.rect = self.surface.get_rect()
        # self.rectTop.top = 0
        # self.rectTop.x = x
        self.rect.bottom = HEIGHT
        self.rect.x = x


class Target(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Target, self).__init__()
        self.surface = pg.surface.Surface((50, 150))
        # self.surfaceBottom = pg.surface.Surface((50, (HEIGHT - self.surfaceTop.get_rect().bottom) - 150))

        # self.surfaceBottom.fill((0,255,0))
        self.rect = self.surface.get_rect()
        # self.rectBottom = self.surfaceBottom.get_rect()
        self.rect.top = y
        self.rect.x = x
    # self.rect.midbottom = y
    # self.rectBottom.bottom = HEIGHT
    # self.rectBottom.x = x


def setup(pipeGroup, targetGroup):
    for i in range(100):
        pipeTop = PipeTop(1024 + (i * 300))
        pipeGroup.add(pipeTop)
        pipeGroup.add(PipeBottom(1024 + (i * 300), pipeTop))
        targetGroup.add(Target(pipeTop.rect.x, pipeTop.rect.height))
    # return pipeGroup


start = False
# pipe = Pipe(1024 + 100)
bird = Bird()
pipeGroup = pg.sprite.Group()
targetGroup = pg.sprite.Group()

setup(pipeGroup, targetGroup)

clock = pg.time.Clock()

speed = 0

count = 0

font = pg.font.Font('MomcakeBold-WyonA.otf', 32)
counterfont = pg.font.Font('MomcakeBold-WyonA.otf', 64)
font2 = pg.font.Font('MomcakeBold-WyonA.otf', 24)
text = font.render('Game Over!', True, (255, 255, 255))
text2 = font2.render('Press Enter to restart', True, (255, 255, 255))
beginText = font.render('Press space to begin!', True, (255, 255, 255))

textRect = text.get_rect()
text2Rect = text2.get_rect()
beginTextRect = beginText.get_rect()

textRect.center = (WIDTH // 2, HEIGHT // 2)
text2Rect.center = (WIDTH // 2, HEIGHT // 2 + 50)
beginTextRect.center = (WIDTH // 2, HEIGHT // 2)

cooldown = 30

running = True
while running:

    counter = counterfont.render(str(count), True, (255, 255, 255))
    counterTextRect = counter.get_rect()

    events = pg.event.get()
    for event in events:
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                if not start:
                    start = True
                    speed = 3
                    bird.jump = True
                    bird.hasGravity = True
                if bird.alive:
                    print("CHECK!")
                    bird.jump = True
            if event.key == K_RETURN and not bird.alive:
                pipeGroup.empty()
                targetGroup.empty()
                setup(pipeGroup, targetGroup)
                bird.pos.y = HEIGHT // 2
                bird.acc.y = 0
                bird.vel.y = 0
                bird.pos.x = 1024 - 250
                bird.rect.y = HEIGHT // 2
                speed = 0
                print(bird.rect.y)
                bird.alive = True
                print("REBORN")
                start = False
                bird.hasGravity = False
                count = 0

    screen.fill((0, 0, 0))

    # pressedkeys = pg.key.get_pressed()

    bird.update()

    if pipeGroup is not None:
        for pipes in pipeGroup:
            screen.blit(pipes.surface, pipes.rect)

    if targetGroup is not None:
        for target in targetGroup:
            screen.blit(target.surface, target.rect)

    if bird.rect.x >= 1024 - 250 and pipeGroup is not None:
        for target in targetGroup:
            if not bird.alive and speed > 0:
                speed -= .0006
            target.rect.move_ip(-speed * 2, 0)

        for pipes in pipeGroup:
            if not bird.alive and speed > 0:
                speed -= .0006
            pipes.rect.move_ip(-speed, 0)
            pipes.rect.move_ip(-speed, 0)

    if not bird.alive:
        screen.blit(text, textRect)
        screen.blit(text2, text2Rect)

    if pipeGroup is not None:
        if pg.sprite.spritecollideany(bird, pipeGroup):
            bird.alive = False

    if targetGroup is not None:
        if pg.sprite.spritecollideany(bird, targetGroup) and cooldown <= 0:
            count += 1
            cooldown = 30
        else:
            cooldown -= 1

    if not start:
        screen.blit(beginText, beginTextRect)

    if start and bird.alive:
        screen.blit(counter, counterTextRect)

    screen.blit(bird.surface, bird.rect)

    pg.display.flip()

    clock.tick(60)
