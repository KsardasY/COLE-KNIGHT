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
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall1', x, y)
                Tile('d_wall', x, y)
            elif level[y][x] == "^":
                Weapon(2, 1, 'colt2.png', x, y, 0)
                Tile('empty', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                px, py = x, y
    new_player = Player(px, py)
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '#':
                Tile('wall', x, y)
    return new_player, px, py


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        if tile_type == 'wall1':
            walls_group.add(self)
            self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        elif tile_type == "wall":
            self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y - 16)
            hwalls_group.add(self)
        elif tile_type == "d_wall":
            self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y + 16)
        else:
            self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.c = 0
        self.health = HEALTH
        self.protection = PROTECTION
        self.bullets = BULLETS
        if pygame.mouse.get_pos()[0] > tile_width * pos_x + 18:
            self.image = player_image
        else:
            self.image = player_image1
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        self.number_of_weapon = 0
        self.weapons = [colt]
        self.weapon = self.weapons[self.number_of_weapon]
        self.weapon.remove(weapons_group)
        hero_weapon_group.add(self.weapon)

    def animation(self):
        if r or l or h or d:
            if self.c < 25:
                if pygame.mouse.get_pos()[0] > self.rect.x + 18:
                    self.image = player_animation[0]
                else:
                    self.image = player_animation1[0]
            elif self.c < 50:
                if pygame.mouse.get_pos()[0] > self.rect.x + 18:
                    self.image = player_animation[1]
                else:
                    self.image = player_animation1[1]
            else:
                self.c = -1
            self.c += 1
        else:
            self.c = 0
            if pygame.mouse.get_pos()[0] > self.rect.x + 18:
                self.image = player_image
            else:
                self.image = player_image1

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
        self.weapon.rect.x = self.rect.x + 15 - self.weapon.butt
        self.weapon.rect.y = self.rect.y + 20


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
        pygame.draw.rect(self.image, (COLOR['red']), (35, 5, math.ceil(120 * player.health / HEALTH), 20))

        self.image.blit(load_image('shild.png', -1), (5, 30))
        pygame.draw.rect(self.image, COLOR['black'], (34, 29, 122, 22))
        pygame.draw.rect(self.image, COLOR['orange'], (35, 30, math.ceil(120 * player.protection / PROTECTION), 20))

        self.image.blit(load_image('bullet.png', -1), (5, 55))
        pygame.draw.rect(self.image, COLOR['black'], (34, 54, 122, 22))
        pygame.draw.rect(self.image, COLOR['magenta'], (35, 55, math.ceil(120 * player.bullets / BULLETS), 20))

        self.image.blit(text_health, (95 - text_health.get_width() // 2, 9))
        self.image.blit(text_protection, (95 - text_protection.get_width() // 2, 34))
        self.image.blit(text_bullets, (95 - text_bullets.get_width() // 2, 59))


class Weapon(pygame.sprite.Sprite):
    def __init__(self, damage, rate_of_fire, filename, pos_x, pos_y, butt):
        super().__init__(weapons_group, all_sprites)
        self.damage = damage
        self.rate_of_fire = rate_of_fire
        self.image = load_image(filename, -1)
        self.rect = self.image.get_rect().move(pos_x * tile_width, pos_y * tile_height)
        self.butt = butt

    def update(*args):
        for weap in weapons_group:
            if pygame.sprite.spritecollideany(weap, player_group):
                if len(player.weapons) != 2:
                    player.weapon.remove(hero_weapon_group)
                    player.weapon = weap
                    hero_weapon_group.add(player.weapon)
                    weap.remove(weapons_group)
                    player.weapons.append(weap)
                    player.number_of_weapon = 1
                else:
                    weapons_group.add(player.weapon)
                    player.weapon.remove(hero_weapon_group)
                    del player.weapons[player.number_of_weapon]
                    player.weapon = weap
                    hero_weapon_group.add(player.weapon)
                    weap.remove(weapons_group)
                    player.weapons.insert(player.number_of_weapon, weap)

    def change(*args):
        if len(player.weapons) == 2:
            if player.number_of_weapon == 0:
                player.weapon.remove(hero_weapon_group)
                player.weapon = player.weapons[1]
                hero_weapon_group.add(player.weapon)
                player.number_of_weapon = 1
            elif player.number_of_weapon == 1:
                player.weapon.remove(hero_weapon_group)
                player.weapon = player.weapons[0]
                hero_weapon_group.add(player.weapon)
                player.number_of_weapon = 0


class Potion(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(potion_group, all_sprites)
        if tile_type == "health1":
            self.health_potion = HEALTH_POTION1
            self.bullets_potion = 0
        elif tile_type == "bullet1":
            self.health_potion = 0
            self.bullets_potion = BULLET_POTION1
        self.image = potion_images[tile_type]
        potion_group.add(self)
        self.rect = self.image.get_rect().move(tile_width * pos_x + 10, tile_height * pos_y + 10)

    def update(*args):
        for pot in potion_group:
            if pygame.sprite.spritecollideany(pot, player_group):
                player.health += pot.health_potion
                if player.health > HEALTH:
                    player.health = HEALTH
                player.bullets += pot.bullets_potion
                if player.bullets > BULLETS:
                    player.bullets = BULLETS
                pot.kill()


FPS = 200
pygame.init()
WIDTH = 500
HEIGHT = 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill(pygame.Color('black'))
COLOR = {'black': pygame.Color('black'), 'white': pygame.Color('white'), 'red': pygame.Color('red'),
         'green': pygame.Color('green'), 'blue': pygame.Color('blue'), 'yellow': pygame.Color('yellow'),
         'cyan': pygame.Color('cyan'), 'magenta': pygame.Color('magenta'), 'azure': (150, 255, 255),
         'orange': pygame.Color('orange')}

tile_images = {'wall': load_image('wall.png', -1), 'empty': load_image('flour.png'),
               'd_wall': load_image('d_wall.png'), 'wall1': load_image('d_wall.png')}
potion_images = {"health1": load_image('health1.png', -1), "bullet1": load_image('bullet1.png', -1)}
player_image = load_image('hero.png', -1)
player_animation = (load_image('heromove1.png', -1), load_image('heromove2.png', -1))
player_image1 = pygame.transform.flip(load_image('hero.png', -1), True, False)
player_animation1 = (pygame.transform.flip(load_image('heromove1.png', -1), True, False),
                     pygame.transform.flip(load_image('heromove2.png', -1), True, False))
tile_width = 32
tile_height = 32

player = None
potion_group = pygame.sprite.Group()
weapons_group = pygame.sprite.Group()
hero_weapon_group = pygame.sprite.GroupSingle()
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
HEALTH_POTION1 = 1
HEALTH_POTION2 = 2
HEALTH_POTION3 = 4
BULLET_POTION1 = 30
BULLET_POTION2 = 60
BULLET_POTION3 = 120
colt = Weapon(2, 1, 'colt.png', 1, 1, 0)
colt3 = Weapon(2, 1, 'colt3.png', 1, 1, 0)
hero_weapon_group.add(colt)
colt.remove(weapons_group)
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
            if event.key == pygame.K_f:
                Potion.update()
                Weapon.update()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4 or event.button == 5:
                Weapon.change()

    player.animation()
    player.update()
    camera.update(player)
    for sprite in all_sprites:
        camera.apply(sprite)
    tiles_group.draw(screen)
    potion_group.draw(screen)
    walls_group.draw(screen)
    weapons_group.draw(screen)
    player_group.draw(screen)
    hero_weapon_group.draw(screen)
    hwalls_group.draw(screen)
    screen.blit(Panel().image, (0, HEIGHT - 80))
    clock.tick(FPS)
    pygame.display.flip()
