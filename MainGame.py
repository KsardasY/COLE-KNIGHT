import pygame
import os
import sys
from math import ceil, atan, degrees, sin, radians
from pygame import mixer
from random import randint


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


def playing_song(name):
    mixer.music.load(os.path.join('data', name))
    mixer.music.play(-1)


def playing_sound(name):
    mixer.pre_init(44100, -16, 1, 512)
    mixer.init()
    if proof_for_sound:
        audio = mixer.Sound(os.path.join('data', name))
        audio.play()


def terminate():
    pygame.quit()
    sys.exit()


def how_to_play_screen():
    fon_info = pygame.transform.scale(load_image('fon_how_to_play.png'), (WIDTH, HEIGHT))
    screen.blit(fon_info, (0, 0))
    intro_text = ["Ходьба: ",
                  "W - вверх, S - вниз",
                  "D - вправо, A - влево",
                  "F - подобрать предмет",
                  "LMB - стрельба",
                  "SPACE - переход в другую карту",
                  "*для того, чтобы перейти на",
                  "следущую карту, нужно убить",
                  "всех врагов"]
    font = pygame.font.Font(None, 35)
    text_coord = 80
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 30
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and pygame.mouse.get_pos()[0] >= 439 and pygame.mouse.get_pos()[1] <= 30:
                    return
        pygame.display.flip()
        clock.tick(FPS)


def info_screen():
    fon_info = pygame.transform.scale(load_image('fon_info.png'), (WIDTH, HEIGHT))
    screen.blit(fon_info, (0, 0))
    intro_text = ["Когда-то давно клан ассасинов ",
                  "жил в благополучии и мире,",
                  "но однажды на клан напала", "армия безумного короля.",
                  "В живых остался только глава клана.",
                  "С тех пор он пообещал себе,",
                  "что не успокоится, пока не отомстит",
                  "за своих соклановцев."]
    font = pygame.font.Font(None, 35)
    text_coord = 80
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 30
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and pygame.mouse.get_pos()[0] <= 61 and pygame.mouse.get_pos()[1] <= 31:
                    return
        pygame.display.flip()
        clock.tick(FPS)


def pause():
    global proof_for_song, proof_for_sound, l, h, r, d, running, open_start_screen, move_map
    tiles_group.draw(screen)
    potion_group.draw(screen)
    walls_group.draw(screen)
    weapons_group.draw(screen)
    enemy_group.draw(screen)
    enemy_weapon_group.draw(screen)
    player_group.draw(screen)
    enemy_projectile.draw(screen)
    hero_projectile.draw(screen)
    hero_weapon_group.draw(screen)
    hwalls_group.draw(screen)
    screen.blit(Panel().image, (0, HEIGHT - 80))
    clock.tick(FPS)
    if proof_for_song:
        screen.blit(image_song_on, (160, HEIGHT - 40))
    else:
        screen.blit(image_song_off, (160, HEIGHT - 40))
    if proof_for_sound:
        screen.blit(image_sound_on, (160, HEIGHT - 80))
    else:
        screen.blit(image_sound_off, (160, HEIGHT - 80))
    menu = pygame.transform.scale(load_image('menu.png'), (100, 95))
    exit = pygame.transform.scale(load_image('exit.png'), (40, 40))
    retry = pygame.transform.scale(load_image('retry.png'), (40, 40))
    to_menu = pygame.transform.scale(load_image('to_exit_to_menu.png'), (90, 40))
    screen.blit(menu, (185, 205))
    screen.blit(exit, (190, 210))
    screen.blit(retry, (240, 210))
    screen.blit(to_menu, (190, 255))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                elif event.key == pygame.K_a:
                    l = True
                elif event.key == pygame.K_w:
                    h = True
                elif event.key == pygame.K_s:
                    d = True
                elif event.key == pygame.K_d:
                    r = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    l = False
                elif event.key == pygame.K_w:
                    h = False
                elif event.key == pygame.K_s:
                    d = False
                elif event.key == pygame.K_d:
                    r = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if (event.button == 1 and 190 <= pygame.mouse.get_pos()[0] <= 230 and
                        210 <= pygame.mouse.get_pos()[1] <= 250):
                    terminate()
                elif (event.button == 1 and 240 <= pygame.mouse.get_pos()[0] <= 280 and
                        210 <= pygame.mouse.get_pos()[1] <= 250):
                    open_start_screen = False
                    running = False
                    return
                elif (event.button == 1 and 190 <= pygame.mouse.get_pos()[0] <= 280 and
                        255 <= pygame.mouse.get_pos()[1] <= 295):
                    running = False
                    open_start_screen = True
                    move_map = False
                    pygame.mixer.music.pause()
                    return
                if event.button == 1:
                    if 160 < pygame.mouse.get_pos()[0] < 200 and HEIGHT - 40 <= pygame.mouse.get_pos()[1] <= HEIGHT:
                        if proof_for_song:
                            pygame.mixer.music.pause()
                            proof_for_song = False
                        else:
                            pygame.mixer.music.unpause()
                            proof_for_song = True
                    elif 160 < pygame.mouse.get_pos()[0] < 200 \
                            and HEIGHT - 80 <= pygame.mouse.get_pos()[1] < HEIGHT - 40:
                        if proof_for_sound:
                            proof_for_sound = False
                        else:
                            proof_for_sound = True
        if proof_for_song:
            screen.blit(image_song_on, (160, HEIGHT - 40))
        else:
            screen.blit(image_song_off, (160, HEIGHT - 40))
        if proof_for_sound:
            screen.blit(image_sound_on, (160, HEIGHT - 80))
        else:
            screen.blit(image_sound_off, (160, HEIGHT - 80))
        pygame.display.flip()
        clock.tick(FPS)


def start_screen():
    fon = pygame.transform.scale(load_image('fon.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if (event.button == 1 and 105 <= pygame.mouse.get_pos()[0] <= 393 and
                        113 <= pygame.mouse.get_pos()[1] <= 397):
                    return
                elif event.button == 1 and pygame.mouse.get_pos()[0] <= 61 and pygame.mouse.get_pos()[1] <= 31:
                    info_screen()
                    screen.blit(fon, (0, 0))
                elif event.button == 1 and pygame.mouse.get_pos()[0] >= 337  and pygame.mouse.get_pos()[1] <= 29:
                    how_to_play_screen()
                    screen.blit(fon, (0, 0))
        pygame.display.flip()
        clock.tick(FPS)


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line for line in mapFile]
    max_width = max(map(len, level_map))
    level_map = list(map(lambda x: x.ljust(max_width, " "), level_map))
    return level_map


def generate_level(level):
    global laser_max_size, move_map
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall1', x, y)
                Tile('d_wall', x, y)
                if y != len(level) - 1 and level[y + 1][x] == '#':
                    Tile('wall1', x, y + 0.5)
            elif level[y][x] == "^":
                Weapon(2, 0, 1, 'colt2.png', x, y, 0, 'bullet')
                Tile('empty', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                px, py = x, y
    laser_max_size = int((len(max(level, key=lambda x: len(x))) ** 2 + len(level) ** 2) ** 0.5)
    new_player = Player(px, py)
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '#':
                Tile('wall', x, y)
    if not move_map:
        return new_player, px, py
    else:
        return new_player


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        if tile_type == 'wall1':
            walls_group.add(self)
            self.mask = pygame.mask.from_surface(self.image)
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
        self.coins = 0
        self.f = True
        self.regulator = 0
        self.regenerator = -1
        self.fire = True
        self.brake = 0
        self.imagedeath = player_death
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
        if self.health > 0:
            if pygame.mouse.get_pos()[0] > self.rect.x + 18:
                self.weapon.rect.topleft = (self.rect.x + WEAPON_X - self.weapon.butt, self.rect.y + WEAPON_Y)
                x_distance = pygame.mouse.get_pos()[0] - self.weapon.rect.x
                if x_distance == 0:
                    if pygame.mouse.get_pos()[1] > self.rect.y:
                        angle = 90
                    else:
                        angle = -90
                else:
                    angle = degrees(atan((self.weapon.rect.y - pygame.mouse.get_pos()[1]) / x_distance))
                    angle = degrees(atan((self.weapon.rect.y - (self.weapon.rect.h - self.weapon.rect.w) * sin(
                        radians(angle)) - pygame.mouse.get_pos()[1]) / x_distance))
                self.weapon.image = pygame.transform.rotate(self.weapon.main_image, angle)
                if pygame.mouse.get_pos()[1] < self.weapon.rect.y:
                    self.weapon.rect = self.weapon.rect.move(0, (self.weapon.rect.h - self.weapon.rect.w) * sin(
                        radians(angle)))
            else:
                self.weapon.rect.topright = (self.rect.x - WEAPON_X + self.weapon.butt + self.rect.w,
                                              self.rect.y + WEAPON_Y)
                x_distance = pygame.mouse.get_pos()[0] - self.weapon.rect.topright[0]
                if x_distance == 0:
                    if pygame.mouse.get_pos()[1] > self.rect.y:
                        angle = -90
                    else:
                        angle = 90
                else:
                    angle = degrees(atan((self.weapon.rect.y - pygame.mouse.get_pos()[1]) / x_distance))
                    angle = degrees(atan((self.weapon.rect.y - (self.weapon.rect.h - self.weapon.rect.w) * sin(
                        radians(angle)) - pygame.mouse.get_pos()[1]) / x_distance))
                self.weapon.image = pygame.transform.rotate(self.weapon.main_image1, angle)
                if pygame.mouse.get_pos()[1] < self.weapon.rect.y:
                    self.weapon.rect = self.weapon.rect.move(0, (self.weapon.rect.w - self.weapon.rect.h) * sin(
                        radians(angle)))
                    self.weapon.rect = self.weapon.rect.move(
                        -(self.weapon.rect.w - self.weapon.rect.h) * sin(radians(angle)), 0)
                else:
                    self.weapon.rect = self.weapon.rect.move(
                        (self.weapon.rect.w - self.weapon.rect.h) * sin(radians(angle)), 0)
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
        global move_map, open_start_screen, running, enemy_group
        if self.health > 0:
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
            if not self.fire:
                self.brake += 1
                if self.brake >= FPS // self.weapon.rate_of_fire:
                    self.fire = True
            for projectile in enemy_projectile:
                if pygame.sprite.collide_mask(self, projectile):
                    if projectile.type_of_projectile == 'bullet':
                        self.regenerator = -1
                        self.regulator = -1
                        self.health = max(0, min(self.health + self.protection - projectile.damage, HEALTH))
                        self.protection = max(0, self.protection - projectile.damage)
                        playing_sound("for_gun_1.ogg")
                        projectile.kill()
                    elif projectile.proof_for_damage:
                        self.regenerator = -1
                        self.regulator = -1
                        self.health = max(0, min(self.health + self.protection - projectile.damage, HEALTH))
                        self.protection = max(0, self.protection - projectile.damage)
            if self.regulator == 5 * FPS:
                self.regenerator = (self.regenerator + 1) % (2 * FPS)
            else:
                self.regulator += 1
            if self.regenerator == 2 * FPS - 1 and self.protection != PROTECTION:
                self.protection += 1
        else:
            if self.f:
                self.rect = self.rect.move(0, self.rect.h - self.imagedeath.get_rect().h)
                self.image = self.imagedeath
                self.f = False
        if pygame.sprite.spritecollideany(self, enemy_group):
            open_start_screen = False
            move_map = True
            running = False

    def shot(self):
        if self.health > 0:
            if self.bullets >= self.weapon.cost and self.fire:
                player.bullets -= player.weapon.cost
                self.brake = 0
                hero_projectile.add(Projectile(self.weapon.type_of_projectile, self.weapon.rect.center,
                                               pygame.mouse.get_pos(), self.weapon.color, self.weapon.damage))
                self.fire = False


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
        pygame.draw.rect(self.image, COLOR['blue'], (0, 0, 160, 80), 1)

        self.image.blit(load_image('heart.png', -1), (5, 5))
        pygame.draw.rect(self.image, COLOR['black'], (34, 4, 122, 22))
        pygame.draw.rect(self.image, (COLOR['red']), (35, 5, ceil(120 * player.health / HEALTH), 20))

        self.image.blit(load_image('shild.png', -1), (5, 30))
        pygame.draw.rect(self.image, COLOR['black'], (34, 29, 122, 22))
        pygame.draw.rect(self.image, COLOR['orange'], (35, 30, ceil(120 * player.protection / PROTECTION), 20))

        self.image.blit(load_image('bullets.png', -1), (5, 55))
        pygame.draw.rect(self.image, COLOR['black'], (34, 54, 122, 22))
        pygame.draw.rect(self.image, COLOR['magenta'], (35, 55, ceil(120 * player.bullets / BULLETS), 20))

        self.image.blit(text_health, (95 - text_health.get_width() // 2, 9))
        self.image.blit(text_protection, (95 - text_protection.get_width() // 2, 34))
        self.image.blit(text_bullets, (95 - text_bullets.get_width() // 2, 59))


class Projectile(pygame.sprite.Sprite):
    def __init__(self, type_of_projectile, initial_coords, final_coords, color, damage):
        super().__init__(all_sprites)
        self.damage = damage
        self.type_of_projectile = type_of_projectile
        self.initial_coords = initial_coords
        self.final_coords = final_coords
        if type_of_projectile == 'laser':
            self.c = 0
            self.proof_for_damage = True
            self.color = COLOR[color]
            if abs(self.initial_coords[0] - self.final_coords[0]) > abs(self.initial_coords[1] - self.final_coords[1]):
                self.initial_width = laser_max_size * tile_height
                self.initial_height = max(self.initial_width * abs(self.initial_coords[1] - self.final_coords[1]) /
                                          abs(self.initial_coords[0] - self.final_coords[0]), 3)
            else:
                self.initial_height = laser_max_size * tile_width
                self.initial_width = max(3, self.initial_height * abs(self.initial_coords[0] - self.final_coords[0]) /
                                         abs(self.initial_coords[1] - self.final_coords[1]))
            self.image = pygame.Surface((self.initial_width, self.initial_height))
            self.image.set_colorkey(self.image.get_at((0, 0)))
            if self.initial_coords[0] >= self.final_coords[0] and self.initial_coords[1] >= self.final_coords[1]:
                pygame.draw.line(self.image, self.color, (0, 0), (self.initial_width - 1, self.initial_height - 1), 3)
                self.mask = pygame.mask.from_surface(self.image)
                self.rect = self.image.get_rect()
                self.rect.bottomright = self.initial_coords
                self.coords = list()
                for sprite in walls_group:
                    if pygame.sprite.collide_mask(self, sprite):
                        self.coords.append(pygame.sprite.collide_mask(self, sprite))
                self.nearest_coord = max(self.coords)[0], max(self.coords, key=lambda x: x[1])[1]
                self.width = max(3, self.initial_width - self.nearest_coord[0])
                self.height = max(3, self.initial_height - self.nearest_coord[1])
                self.image = pygame.Surface((self.width, self.height))
                self.image.set_colorkey(self.image.get_at((0, 0)))
                pygame.draw.line(self.image, self.color, (0, 0), (self.width - 1, self.height - 1), 3)
                self.rect = self.image.get_rect()
                self.rect.bottomright = self.initial_coords
            elif self.initial_coords[0] <= self.final_coords[0] and self.initial_coords[1] <= self.final_coords[1]:
                pygame.draw.line(self.image, self.color, (0, 0), (self.initial_width - 1, self.initial_height - 1), 3)
                self.mask = pygame.mask.from_surface(self.image)
                self.rect = self.image.get_rect()
                self.rect.topleft = self.initial_coords
                self.coords = list()
                for sprite in walls_group:
                    if pygame.sprite.collide_mask(self, sprite):
                        self.coords.append(pygame.sprite.collide_mask(self, sprite))
                self.nearest_coord = min(self.coords)[0], min(self.coords, key=lambda x: x[1])[1]
                self.width = max(3, self.nearest_coord[0])
                self.height = max(3, self.nearest_coord[1])
                self.image = pygame.Surface((self.width, self.height))
                self.image.set_colorkey(self.image.get_at((0, 0)))
                pygame.draw.line(self.image, self.color, (0, 0), (self.width - 1, self.height - 1), 3)
                self.rect = self.image.get_rect()
                self.rect.topleft = self.initial_coords
            elif self.initial_coords[0] >= self.final_coords[0] and self.initial_coords[1] <= self.final_coords[1]:
                pygame.draw.line(self.image, self.color, (0, self.initial_height - 1), (self.initial_width - 1, 0), 3)
                self.mask = pygame.mask.from_surface(self.image)
                self.rect = self.image.get_rect()
                self.rect.topright = self.initial_coords
                self.coords = list()
                for sprite in walls_group:
                    if pygame.sprite.collide_mask(self, sprite):
                        self.coords.append(pygame.sprite.collide_mask(self, sprite))
                self.nearest_coord = max(self.coords)[0], min(self.coords, key=lambda x: x[1])[1]
                self.width = max(3, self.initial_width - self.nearest_coord[0])
                self.height = max(3, self.nearest_coord[1])
                self.image = pygame.Surface((self.width, self.height))
                self.image.set_colorkey(self.image.get_at((0, 0)))
                pygame.draw.line(self.image, self.color, (0, self.height - 1), (self.width - 1, 0), 3)
                self.rect = self.image.get_rect()
                self.rect.topright = self.initial_coords
            else:
                pygame.draw.line(self.image, self.color, (0, self.initial_height - 1), (self.initial_width - 1, 0), 3)
                self.mask = pygame.mask.from_surface(self.image)
                self.rect = self.image.get_rect()
                self.rect.bottomleft = self.initial_coords
                self.coords = list()
                for sprite in walls_group:
                    if pygame.sprite.collide_mask(self, sprite):
                        self.coords.append(pygame.sprite.collide_mask(self, sprite))
                self.nearest_coord = min(self.coords)[0], max(self.coords, key=lambda x: x[1])[1]
                self.width = max(3, self.nearest_coord[0])
                self.height = max(3, self.initial_height - self.nearest_coord[1])
                self.image = pygame.Surface((self.width, self.height))
                self.image.set_colorkey(self.image.get_at((0, 0)))
                pygame.draw.line(self.image, self.color, (0, self.height - 1), (self.width - 1, 0), 3)
                self.rect = self.image.get_rect()
                self.rect.bottomleft = self.initial_coords
        else:
            self.image = load_image('bullet.png')
            self.rect = self.image.get_rect()
            self.rect.center = self.initial_coords
            self.x = 0
            self.y = 0
            self.coefficient_x = abs(self.initial_coords[0] - self.final_coords[0])
            self.coefficient_y = abs(self.initial_coords[1] - self.final_coords[1])
            if self.rect.center[0] >= self.final_coords[0] and self.rect.center[1] >= self.final_coords[1]:
                self.unit_vector = 3 / (self.coefficient_x + self.coefficient_y)
                self.vector = (- self.unit_vector * self.coefficient_x, - self.unit_vector * self.coefficient_y)
            elif self.rect.center[0] <= self.final_coords[0] and self.rect.center[1] <= self.final_coords[1]:
                self.unit_vector = 3 / (self.coefficient_x + self.coefficient_y)
                self.vector = (self.unit_vector * self.coefficient_x, self.unit_vector * self.coefficient_y)
            elif self.rect.center[0] <= self.final_coords[0] and self.rect.center[1] >= self.final_coords[1]:
                self.unit_vector = 3 / (self.coefficient_x + self.coefficient_y)
                self.vector = (self.unit_vector * self.coefficient_x, - self.unit_vector * self.coefficient_y)
            elif self.rect.center[0] >= self.final_coords[0] and self.rect.center[1] <= self.final_coords[1]:
                self.unit_vector = 3 / (self.coefficient_x + self.coefficient_y)
                self.vector = (- self.unit_vector * self.coefficient_x, self.unit_vector * self.coefficient_y)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        if self.type_of_projectile == 'laser':
            if self.c == 0:
                playing_sound("lazer.ogg")
            elif self.c == 1:
                self.proof_for_damage = False
            self.c += 1
            if self.c == 10:
                self.kill()
        else:
            self.rect = self.rect.move(int(self.x + self.vector[0]) - int(self.x),
                                       int(self.y + self.vector[1]) - int(self.y))
            self.x += self.vector[0]
            self.y += self.vector[1]
            if pygame.sprite.spritecollideany(self, walls_group):
                playing_sound("for_gun_1.ogg")
                self.kill()


class Weapon(pygame.sprite.Sprite):
    def __init__(self, damage, cost, rate_of_fire, filename, pos_x, pos_y, butt, type_of_projectile, color=None):
        super().__init__(weapons_group, all_sprites)
        self.cost = cost
        self.damage = damage
        self.rate_of_fire = rate_of_fire
        self.image = load_image(filename, -1)
        self.main_image = self.image
        self.main_image1 = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect().move(pos_x * tile_width, pos_y * tile_height)
        self.butt = butt
        self.type_of_projectile = type_of_projectile
        self.color = color

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
                    player.weapon.image = player.weapon.main_image
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


class Enemy(pygame.sprite.Sprite):
    def __init__(self, health, pos_x, pos_y, filename, weapon, animation, animation1, death, brake):
        super().__init__(enemy_group, all_sprites)
        self.f = True
        self.imagedeath = load_image(death, -1)
        self.brake = brake
        self.image1 = load_image(filename, -1)
        self.image2 = pygame.transform.flip(self.image1, True, False)
        self.image = self.image1
        self.animation2 = (load_image(animation, -1), load_image(animation1, -1))
        self.animation1 = (pygame.transform.flip(load_image(animation, -1), True, False),
                             pygame.transform.flip(load_image(animation1, -1), True, False))
        self.health = health
        self.rect = self.image.get_rect()
        self.rect.topleft = (pos_x * tile_width, pos_y * tile_height)
        self.weapon = weapon
        enemy_weapon_group.add(self.weapon)
        self.weapon.remove(weapons_group)
        self.k = randint(0, 4 * FPS)
        self.c = 0
        self.regulator = 0

    def update(self):
        if self.health > 0:
            if player.rect.center[0] > self.rect.x + 15:
                self.weapon.rect.topleft = (self.rect.x + WEAPON_X - self.weapon.butt, self.rect.y + WEAPON_Y)
                x_distance = player.rect.center[0] - self.weapon.rect.x
                if -2 <= x_distance <= 2:
                    if player.rect.center[1] <= self.rect.center[1]:
                        angle = 90
                    else:
                        angle = -90
                else:
                    angle = degrees(atan((self.weapon.rect.y - player.rect.center[1]) / x_distance))
                    angle = degrees(atan((self.weapon.rect.y - (self.weapon.rect.h - self.weapon.rect.w) * sin(
                        radians(angle)) - player.rect.center[1]) / x_distance))
                self.weapon.image = pygame.transform.rotate(self.weapon.main_image, angle)
                if player.rect.center[1] < self.weapon.rect.y:
                    self.weapon.rect = self.weapon.rect.move(0, (self.weapon.rect.h - self.weapon.rect.w) * sin(
                        radians(angle)))
            else:
                self.weapon.rect.topright = (self.rect.x - WEAPON_X + self.weapon.butt + self.rect.w,
                                              self.rect.y + WEAPON_Y)
                x_distance = player.rect.center[0] - self.weapon.rect.topright[0]
                if -2 <= x_distance <= 2:
                    if player.rect.center[1] >= self.rect.center[1]:
                        angle = 90
                    else:
                        angle = -90
                else:
                    angle = degrees(atan((self.weapon.rect.y - player.rect.center[1]) / x_distance))
                    angle = degrees(atan((self.weapon.rect.y - (self.weapon.rect.h - self.weapon.rect.w) * sin(
                        radians(angle)) - player.rect.center[1]) / x_distance))
                self.weapon.image = pygame.transform.rotate(self.weapon.main_image1, angle)
                if player.rect.center[1] < self.weapon.rect.y:
                    self.weapon.rect = self.weapon.rect.move(0, (self.weapon.rect.w - self.weapon.rect.h) * sin(
                        radians(angle)))
                    self.weapon.rect = self.weapon.rect.move(
                        -(self.weapon.rect.w - self.weapon.rect.h) * sin(radians(angle)), 0)
                else:
                    self.weapon.rect = self.weapon.rect.move(
                        (self.weapon.rect.w - self.weapon.rect.h) * sin(radians(angle)), 0)
            for projectile in hero_projectile:
                if pygame.sprite.collide_mask(self, projectile):
                    if projectile.type_of_projectile == 'bullet':
                        self.regenerator = -1
                        self.regulator = -1
                        self.health = max(0, self.health - projectile.damage)
                        playing_sound("for_gun_1.ogg")
                        projectile.kill()
                    elif projectile.proof_for_damage:
                        self.health = max(0, self.health - projectile.damage)
        else:
            if self.f:
                player.coins += 2
                player.bullets = min(BULLETS, player.bullets + 2)
                self.weapon.image = self.weapon.main_image
                weapons_group.add(self.weapon)
                self.weapon.remove(enemy_weapon_group)
                self.rect = self.rect.move(0, self.rect.height - self.imagedeath.get_rect().height)
                self.image = self.imagedeath
                self.f = False

    def go(self):
        if self.regulator == 0:
            if player.rect.center[0] > self.rect.center[0]:
                self.rect.x += 1
                if pygame.sprite.spritecollideany(self, walls_group):
                    self.rect.x -= 1
            elif player.rect.center[0] < self.rect.center[0]:
                self.rect.x -= 1
                if pygame.sprite.spritecollideany(self, walls_group):
                    self.rect.x += 1
            if player.rect.center[1] > self.rect.center[1]:
                self.rect.y += 1
                if pygame.sprite.spritecollideany(self, walls_group):
                    self.rect.y -= 1
            elif player.rect.center[1] < self.rect.center[1]:
                self.rect.y -= 1
                if pygame.sprite.spritecollideany(self, walls_group):
                    self.rect.y += 1
            if self.c < 25:
                if player.rect.center[0] > self.rect.center[0]:
                    self.image = self.animation2[0]
                else:
                    self.image = self.animation1[0]
            elif self.c < 50:
                if player.rect.center[0] > self.rect.center[0]:
                    self.image = self.animation2[1]
                else:
                    self.image = self.animation1[1]
        self.regulator = (self.regulator + 1) % self.brake
        if self.c == 50:
            self.c = -1
        self.c += 1

    def stop(self):
        self.c = 0
        if self.rect.center[0] >= player.rect.center[0]:
            self.image = self.image2
        else:
            self.image = self.image1

    def shot(self):
        enemy_projectile.add(Projectile(self.weapon.type_of_projectile, self.weapon.rect.center, player.rect.center,
                                        self.weapon.color, self.weapon.damage))

    def behavior(self):
        if self.health > 0:
            if self.k < 2 * FPS:
                self.go()
            elif 2 * FPS <= self.k < 4 * FPS:
                self.stop()
            else:
                self.shot()
            self.k = (self.k + 1) % (4 * FPS + 1)
        else:
            self.death()

    def death(self):
        pass


move_map = False
open_start_screen = True
proof_for_song = True
proof_for_sound = True
FPS = 200
pygame.init()
WIDTH = 500
HEIGHT = 500
WEAPON_X = 18
WEAPON_Y = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill(pygame.Color('black'))
COLOR = {'black': pygame.Color('black'), 'white': pygame.Color('white'), 'red': pygame.Color('red'),
         'green': pygame.Color('green'), 'blue': pygame.Color('blue'), 'yellow': pygame.Color('yellow'),
         'cyan': pygame.Color('cyan'), 'magenta': pygame.Color('magenta'), 'azure': (150, 255, 255),
         'orange': pygame.Color('orange')}

tile_images = {'wall': load_image('wall.png'), 'empty': load_image('flour.png'),
               'd_wall': load_image('d_wall.png'), 'wall1': load_image('d_wall.png')}
potion_images = {"health1": load_image('health1.png', -1), "bullet1": load_image('bullet1.png', -1)}
player_image = load_image('hero.png', -1)
player_animation = (load_image('heromove1.png', -1), load_image('heromove2.png', -1))
player_image1 = pygame.transform.flip(load_image('hero.png', -1), True, False)
player_animation1 = (pygame.transform.flip(load_image('heromove1.png', -1), True, False),
                     pygame.transform.flip(load_image('heromove2.png', -1), True, False))
player_death = load_image('herodeath.png', -1)
image_sound_on = load_image('volume_on.png')
image_sound_off = load_image('volume_off.png')
image_song_on = load_image('song_on.png')
image_song_off = load_image('song_off.png')
tile_width = 32
tile_height = 32
clock = pygame.time.Clock()
HEALTH = 5
PROTECTION = 5
BULLETS = 200
HEALTH_POTION1 = 1
HEALTH_POTION2 = 2
HEALTH_POTION3 = 4
BULLET_POTION1 = 30
BULLET_POTION2 = 60
BULLET_POTION3 = 120


def game():
    global player, potion_group, weapons_group, hero_weapon_group, hero_projectile, enemy_group, \
        enemy_projectile, hwalls_group, walls_group, all_sprites, enemy_weapon_group, tiles_group, player_group, colt, \
        colt3, colt4, g_blaster, b_blaster, proof_for_song, proof_for_sound, running, enemy, enemy1, enemy2, h, d, l,\
        r, screen, clock, open_start_screen, move_map, colt

    volume_group = pygame.sprite.Group()
    potion_group = pygame.sprite.Group()
    weapons_group = pygame.sprite.Group()
    hero_weapon_group = pygame.sprite.GroupSingle()
    hero_projectile = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()
    enemy_projectile = pygame.sprite.Group()
    hwalls_group = pygame.sprite.Group()
    walls_group = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    enemy_weapon_group = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()

    if move_map:
        pllayer = player
        player = generate_level(load_level('map2.txt'))
        player.coins = pllayer.coins
        player.f = pllayer.f
        player.regulator = pllayer.regulator
        player.regenerator = pllayer.regenerator
        player.fire = pllayer.fire
        player.brake = pllayer.brake
        player.c = pllayer.c
        player.health = pllayer.health
        player.protection = pllayer.protection
        player.bullets = pllayer.bullets
        player.number_of_weapon = pllayer.number_of_weapon
        player.weapons = pllayer.weapons
        player.weapon = pllayer.weapons[pllayer.number_of_weapon]
        player.weapon.remove(weapons_group)
        hero_weapon_group.add(pllayer.weapon)
        pllayer = None
        enemy = Enemy(10, 22, 8, 'enemy1.png', Weapon(2, 0, 1, 'colt3.png', 1, 1, 0, 'bullet'),
                      'enemy1m1.png', 'enemy1m2.png', 'enemy1d.png', 3)
    else:
        colt = Weapon(2, 0, 1, 'colt.png', 1, 1, 0, 'bullet')
        colt3 = Weapon(2, 0, 1, 'colt3.png', 1, 1, 0, 'bullet')
        colt4 = Weapon(2, 0, 1, 'colt2.png', 1, 1, 0, 'bullet')
        g_blaster = Weapon(6, 2, 1, 'g_blaster.png', 4, 5, 4, 'laser', 'green')
        b_blaster = Weapon(6, 2, 1, 'b_blaster.png', 4, 6, 4, 'laser', 'blue')
        hero_weapon_group.add(colt)
        colt.remove(weapons_group)
        player, level_x, level_y = generate_level(load_level('map.txt'))
        enemy = Enemy(10, 13, 29, 'enemy1.png', colt3, 'enemy1m1.png', 'enemy1m2.png', 'enemy1d.png', 3)
        enemy1 = Enemy(10, 10, 25, 'enemy1.png', g_blaster, 'enemy1m1.png', 'enemy1m2.png', 'enemy1d.png', 3)
        enemy2 = Enemy(10, 12, 21, 'enemy1.png', colt4, 'enemy1m1.png', 'enemy1m2.png', 'enemy1d.png', 3)
    h = False
    d = False
    l = False
    r = False
    if open_start_screen:
        start_screen()
    camera = Camera()
    fire = False
    if proof_for_song:
        playing_song("song1.ogg")
    running = True
    while running:
        event = None
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause()
                elif event.key == pygame.K_a:
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
                if event.button == 1:
                    if 160 < pygame.mouse.get_pos()[0] < 200 and HEIGHT - 40 <= pygame.mouse.get_pos()[1] <= HEIGHT:
                        if proof_for_song:
                            pygame.mixer.music.pause()
                            proof_for_song = False
                        else:
                            pygame.mixer.music.unpause()
                            proof_for_song = True
                    elif 160 < pygame.mouse.get_pos()[0] < 200 \
                            and HEIGHT - 80 <= pygame.mouse.get_pos()[1] < HEIGHT - 40:
                        if proof_for_sound:
                            proof_for_sound = False
                        else:
                            proof_for_sound = True
                    elif pygame.mouse.get_pos()[0] >= 200 or HEIGHT - 80 > pygame.mouse.get_pos()[1]:
                        fire = True
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and not (pygame.mouse.get_pos()[0] < 50 and pygame.mouse.get_pos()[1] < 50):
                    fire = False
        if fire:
            player.shot()
        hero_projectile.update()
        for sprite in enemy_group:
            sprite.behavior()
            sprite.update()
        enemy_projectile.update()
        player.update()
        player.animation()
        camera.update(player)
        for sprite in all_sprites:
            camera.apply(sprite)
        tiles_group.draw(screen)
        potion_group.draw(screen)
        walls_group.draw(screen)
        weapons_group.draw(screen)
        enemy_group.draw(screen)
        enemy_projectile.draw(screen)
        enemy_weapon_group.draw(screen)
        player_group.draw(screen)
        hero_projectile.draw(screen)
        hero_weapon_group.draw(screen)
        hwalls_group.draw(screen)
        screen.blit(Panel().image, (0, HEIGHT - 80))
        clock.tick(FPS)
        if proof_for_song:
            screen.blit(image_song_on, (160, HEIGHT - 40))
        else:
            screen.blit(image_song_off, (160, HEIGHT - 40))
        if proof_for_sound:
            screen.blit(image_sound_on, (160, HEIGHT - 80))
        else:
            screen.blit(image_sound_off, (160, HEIGHT - 80))
        pygame.display.flip()
    if not running:
        game()


game()