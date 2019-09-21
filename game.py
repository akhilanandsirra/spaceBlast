import math
import os
import random
import sys
from os import path
from random import randrange
import pygame as pg

img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')
HS_File = "highscore.txt"

pg.init()
height = 650
width = 1200

total = 3

os_x = 100
os_y = 45
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (os_x, os_y)

screen = pg.display.set_mode((width, height), pg.NOFRAME)
screen_rect = screen.get_rect()
background = pg.image.load('background.png').convert()
background = pg.transform.smoothscale(pg.image.load('background.png'), (width, height))
retry = pg.image.load('retry4.png').convert_alpha()
retry = pg.transform.smoothscale(pg.image.load('retry4.png'), (33, 33))
clock = pg.time.Clock()
running = True
moving = False

font_name = pg.font.match_font('Bahnschrift', bold=True)


def load_data():
    dir = path.dirname(__file__)
    with open(path.join(dir, HS_File), 'r') as f:
        try:
            highscore = int(f.read())
        except:
            highscore = 0
    return highscore


def draw_text(surf, text, size, x, y, color):
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    surf.blit(text_surface, text_rect)


class Mob(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load('enemy.png').convert_alpha()
        self.image = pg.transform.smoothscale(pg.image.load('enemy.png'), (33, 33))
        self.image_orig = self.image.copy()
        self.radius = int(29 * .80 / 2)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(width - self.rect.width)
        self.rect.y = (randrange(-100, -40), randrange(650, 670))[randrange(0, 2)]
        self.speed = 4
        self.rot = 0
        self.rot_speed = 5
        self.last_update = pg.time.get_ticks()

    def rotate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pg.transform.rotozoom(self.image_orig, self.rot, 1)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        dirvect = pg.math.Vector2(rotator.rect.x - self.rect.x,
                                  rotator.rect.y - self.rect.y)
        if dirvect.length_squared() > 0:
            dirvect = dirvect.normalize()

            # Move along this normalized vector towards the player at current speed.
        if dirvect.length_squared() > 0:
            dirvect.scale_to_length(self.speed)
        self.rect.move_ip(dirvect)


class Rotator(pg.sprite.Sprite):
    def __init__(self, screen_rect):
        pg.sprite.Sprite.__init__(self)
        self.screen_rect = screen_rect
        self.master_image = pg.image.load('spaceship.png').convert_alpha()
        self.master_image = pg.transform.smoothscale(pg.image.load('spaceship.png'), (33, 33))
        self.radius = 12
        self.image = self.master_image.copy()
        self.rect = self.image.get_rect(center=[width / 2, height / 2])
        self.delay = 10
        self.timer = 0.0
        self.angle = 0
        self.distance = 0
        self.angle_offset = 0

    def get_angle(self):
        mouse = pg.mouse.get_pos()
        offset = (self.rect.centerx - mouse[0], self.rect.centery - mouse[1])
        self.angle = math.degrees(math.atan2(*offset)) - self.angle_offset
        old_center = self.rect.center
        self.image = pg.transform.rotozoom(self.master_image, self.angle, 1)
        self.rect = self.image.get_rect(center=old_center)
        self.distance = math.sqrt((offset[0] * offset[0]) + (offset[1] * offset[1]))

    def update(self):
        self.get_angle()
        self.display = 'angle:{:.2f} distance:{:.2f}'.format(self.angle, self.distance)
        self.dx = 1
        self.dy = 1
        self.rect.clamp_ip(self.screen_rect)
        if moving:
            key = pg.key.get_pressed()
            dist = 4
            if key[pg.K_DOWN] or key[pg.K_s]:
                self.rect.y += dist  # move down
            elif key[pg.K_UP] or key[pg.K_w]:
                self.rect.y -= dist  # move up
            if key[pg.K_RIGHT] or key[pg.K_d]:
                self.rect.x += dist  # move right
            elif key[pg.K_LEFT] or key[pg.K_a]:
                self.rect.x -= dist  # move left

    def draw(self, surf):
        surf.blit(self.image, self.rect)

    def shoot(self, mousepos):
        dx = mousepos[0] - self.rect.centerx
        dy = mousepos[1] - self.rect.centery
        if abs(dx) > 0 or abs(dy) > 0:
            bullet = Bullet(self.rect.centerx, self.rect.centery, dx, dy)
            all_sprites.add(bullet)
            bullets.add(bullet)
            shoot_sound.play()


class Bullet(pg.sprite.Sprite):
    def __init__(self, x, y, dx, dy):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.smoothscale(pg.image.load('bullet.png').convert_alpha(), (10, 10))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 8
        self.pos = pg.math.Vector2(x, y)
        self.dir = pg.math.Vector2(dx, dy).normalize()

    def update(self):
        self.pos += self.dir * self.speed
        self.rect.center = (round(self.pos.x), round(self.pos.y))

        if self.rect.bottom < 0:
            self.kill()


class Explosion(pg.sprite.Sprite):
    def __init__(self, center, size):
        pg.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pg.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pg.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


shoot_sound = pg.mixer.Sound(path.join(snd_dir, 'pew3.wav'))
expl_sound = pg.mixer.Sound(path.join(snd_dir, 'expl3.wav'))
expl2_sound = pg.mixer.Sound(path.join(snd_dir, 'expl6.wav'))

explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['player'] = []
for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pg.image.load(path.join(img_dir, filename)).convert_alpha()
    img_lg = pg.transform.smoothscale(img, (75, 75))
    explosion_anim['lg'].append(img_lg)
    img_sm = pg.transform.smoothscale(img, (100, 100))
    explosion_anim['sm'].append(img_sm)
    filename = 'sonicExplosion0{}.png'.format(i)
    img = pg.image.load(path.join(img_dir, filename)).convert_alpha()
    explosion_anim['player'].append(img)


def show_go_screen():
    all_sprites = pg.sprite.Group()
    if not start:
        expl = Explosion(rotator.rect.center, 'player')
        all_sprites.add(expl)
        expl2_sound.play()

    spaceship = Rotator(screen_rect)
    # all_sprites.add(spaceship)

    waiting = True
    while waiting:
        screen.blit(background, [0, 0])
        highscore = load_data()

        if start:
            draw_text(screen, "SPACE BLAST", 64, width / 2 + 3.5, height / 4 + 3.5, [23, 22, 20])
            draw_text(screen, "SPACE BLAST", 64, width / 2, height / 4, [255, 255, 255])
            draw_text(screen, "PRESS SPACEBAR TO BEGIN", 15, width / 2, height / 4 + 75, [255, 255, 255])
            draw_text(screen, "PRESS ESC TO EXIT", 13, width / 2, height / 1.5, [255, 255, 255])
            draw_text(screen, "HIGH SCORE: " + str(highscore), 15, width - 65, 25, [255, 255, 255])

        else:
            highscore = load_data()
            if pg.time.get_ticks() - hide_timer > 1000:
                draw_text(screen, "GAME OVER", 64, width / 2 + 3.5, height / 4 + 75 + 3.5, [23, 22, 20])
                draw_text(screen, "GAME OVER", 64, width / 2, height / 4 + 75, [255, 255, 255])
                draw_text(screen, "PRESS SPACEBAR TO TRY AGAIN", 15, width / 2, height / 4 + 150, [255, 255, 255])
                screen.blit(retry, [width / 2 - 15, height / 2 + 15])
                draw_text(screen, "PRESS ESC TO EXIT", 13, width / 2, height / 2 + 75, [255, 255, 255])
                draw_text(screen, "HIGH SCORE: " + str(highscore), 15, width - 65, 25, [255, 255, 255])

        clock.tick(60)
        if start:
            all_sprites.add(spaceship)
        all_sprites.update()
        all_sprites.draw(screen)
        pg.display.update()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
                pygame.quit()
            if event.type == pg.KEYDOWN:
                if event.unicode == '\x1b':
                    sys.exit()
                    pygame.quit()
                if event.unicode == ' ':
                    waiting = False


game_over = True
start = True

while running:
    if game_over:
        show_go_screen()
        game_over = False
        moving = True
        clock.tick(60)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
                pygame.quit()

        all_sprites = pg.sprite.Group()
        bullets = pg.sprite.Group()
        mobs = pg.sprite.Group()
        rotator = Rotator(screen_rect)
        all_sprites.add(rotator)

        death = False
        score = 0
        level = 0

        if len(mobs) == 0:
            level += 1
            for i in range(level * 4):
                m = Mob()
                all_sprites.add(m)
                mobs.add(m)

    keys = pg.key.get_pressed()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
            pygame.quit()
        if event.type == pg.MOUSEBUTTONDOWN:
            rotator.shoot(event.pos)

    # screen.fill((0,0,0))
    screen.blit(background, [0, 0])
    # rotator.update(keys)
    all_sprites.update()
    # rotator.draw(screen)

    hits = pg.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        score += 1
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        expl_sound.play()

    # check to see if a mob hit the player
    hits = pg.sprite.spritecollide(rotator, mobs, False, pg.sprite.collide_circle)
    if hits:
        death = True
        hide_timer = pg.time.get_ticks()

    if death:
        start = False
        game_over = True
        moving = False

    highscore = load_data()
    all_sprites.draw(screen)
    draw_text(screen, str(score), 22, width / 2, 600, [255, 255, 255])

    if score > highscore:
        highscore = score
        draw_text(screen, "HIGH SCORE: " + str(highscore), 15, width - 65, 25, [255, 255, 255])
        f = open("highscore.txt", "w+")
        f.write(str(score))
    else:
        draw_text(screen, "HIGH SCORE: " + str(highscore), 15, width - 65, 25, [255, 255, 255])
    clock.tick(60)
    pg.display.update()
