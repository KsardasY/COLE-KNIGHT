import pygame
import os
import sys
import math


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '#'), level_map))


def generate_level(level):
    i = 0
    level = list(map(lambda x: list(x), level))
    while i < len(level):
        s = []
        for j in range(len(level[i])):
            if level[i][j] != '@':
                s.append(level[i][j])
            else:
                s.append('.')
        level.insert(i + 1, s)
        i += 2
    for i in range(1, len(level)):
        for j in range(len(level[i])):
            if level[i][j] == '.' and level[i - 1][j] == '#':
                level[i][j] = '*'
    for i in range(1, len(level)):
        for j in range(len(level[i])):
            if level[i][j] == '#' and level[i - 1][j] == '.':
                level[i][j] = '^'
    level.append('*' * len(level[-1]))
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '^':
                Tile('hwall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
            elif level[y][x] == '*':
                Tile('dwall', x, y)
    return new_player, x, y


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        if tile_type == 'wall':
            walls_group.add(self)
        if tile_type == 'hwall':
            hwalls_group.add(self)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.health = HEALTH
        self.protection = PROTECTION
        self.bullets = BULLETS
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * pos_x + 18, tile_height * pos_y + 19)

    def update(self):
        if l:
            self.rect.x -= 1
            if pygame.sprite.spritecollideany(self, walls_group):
                self.rect.x += 1
        if h:
            self.rect.y -= 1
            if pygame.sprite.spritecollideany(self, walls_group):
                self.rect.y += 1
        if d:
            self.rect.y += 1
            if pygame.sprite.spritecollideany(self, walls_group):
                self.rect.y -= 1
        if r:
            self.rect.x += 1
            if pygame.sprite.spritecollideany(self, walls_group):
                self.rect.x -= 1


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)


class Panel:
    def __init__(self):
        font = pygame.font.Font(None, 24)
        text_health = font.render(str(player.health) + '/' + str(HEALTH), 1, COLOR['white'])
        text_protection = font.render(str(player.protection) + '/' + str(PROTECTION), 1, COLOR['white'])
        text_bullets = font.render(str(player.bullets) + '/' + str(BULLETS), 1, COLOR['white'])
        self.image = pygame.Surface((160, 80))
        self.image.fill(COLOR['azure'])
        pygame.draw.rect(self.image, COLOR['blue'], (0, 0, 200, 80), 1)

        self.image.blit(load_image('heart.png', -1), (5, 5))
        pygame.draw.rect(self.image, COLOR['black'], (34, 4, 122, 22))
        pygame.draw.rect(self.image, COLOR['red'], (35, 5, math.ceil(120 * player.health / HEALTH), 20))

        self.image.blit(load_image('shild.png', -1), (5, 30))
        pygame.draw.rect(self.image, COLOR['black'], (34, 29, 122, 22))
        pygame.draw.rect(self.image, COLOR['yellow'], (35, 30, math.ceil(120 * player.protection / PROTECTION), 20))

        self.image.blit(load_image('bullet.png', -1), (5, 55))
        pygame.draw.rect(self.image, COLOR['black'], (34, 54, 122, 22))
        pygame.draw.rect(self.image, COLOR['magenta'], (35, 55, math.ceil(120 * player.bullets / BULLETS), 20))

        self.image.blit(text_health, (95 - text_health.get_width() // 2, 9))
        self.image.blit(text_protection, (95 - text_protection.get_width() // 2, 34))
        self.image.blit(text_bullets, (95 - text_bullets.get_width() // 2, 59))


FPS = 200
pygame.init()
WIDTH = 500
HEIGHT = 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill(pygame.Color('black'))
COLOR = {'black': pygame.Color('black'), 'white': pygame.Color('white'), 'red': pygame.Color('red'),
         'green': pygame.Color('green'), 'blue': pygame.Color('blue'), 'yellow': pygame.Color('yellow'),
         'cyan': pygame.Color('cyan'), 'magenta': pygame.Color('magenta'), 'azure': (150, 255, 255)}

tile_images = {'wall': load_image('wall.png'), 'empty': load_image('flour.png'), 'dwall': load_image('d_wall.png'),
               'hwall': load_image('wall.png')}
player_image = load_image('hero.png', -1)
tile_width = 50
tile_height = 25

player = None
hwalls_group = pygame.sprite.Group()
walls_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

clock = pygame.time.Clock()
start_screen()
HEALTH = 5
PROTECTION = 5
BULLETS = 200
player, level_x, level_y = generate_level(load_level('map.txt'))
running = True
camera = Camera()
h = False
d = False
l = False
r = False

while running:
    event = None
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                l = True
            elif event.key == pygame.K_w:
                h = True
            elif event.key == pygame.K_s:
                d = True
            elif event.key == pygame.K_d:
                r = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                l = False
            elif event.key == pygame.K_w:
                h = False
            elif event.key == pygame.K_s:
                d = False
            elif event.key == pygame.K_d:
                r = False
    player.update()
    camera.update(player)
    for sprite in all_sprites:
        camera.apply(sprite)
    tiles_group.draw(screen)
    walls_group.draw(screen)
    player_group.draw(screen)
    hwalls_group.draw(screen)
    screen.blit(Panel().image, (0, HEIGHT - 80))
    clock.tick(FPS)
    pygame.display.flip()
