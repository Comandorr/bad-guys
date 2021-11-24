from pyengine import*
window = create_window(1920, 1080)
from pyengine import win_w, win_h, center_x, center_y, window

idle = [Image('images/idle1.png'), Image('images/idle3.png')]
wall_img = Image('images/wall.png', (256, 146))
wall2_img = Image('images/wall2.png', (24, 256))
enemy_img = [Image('images/enemy1.png'), Image('images/enemy2.png')]
b_up_img = Image('images/b_up.png', (32, 32))
b_down_img = Image('images/b_down.png', (32, 32))
b_left_img = Image('images/b_left.png', (32, 32))
b_right_img = Image('images/b_right.png', (32, 32))

floor_normal = \
    [Image('images/floor_normal/floor_tile_1.png', (128, 128))]*15 + \
    [Image('images/floor_normal/floor_tile_2.png', (128, 128)), Image('images/floor_normal/floor_tile_3.png', (128, 128)), Image('images/floor_normal/floor_tile_4.png', (128, 128))]
floor_danger = \
    [Image('images/floor_danger/floor_tile_1.png', (128, 128))]*15 + \
    [Image('images/floor_danger/floor_tile_2.png', (128, 128)), Image('images/floor_danger/floor_tile_3.png', (128, 128)), Image('images/floor_danger/floor_tile_4.png', (128, 128))]
floor = Group()
walls = Group()
enemies = Group()
bullets = Group()


class Tile(SimpleSprite):
    def __init__(self, x, y):
        self.nomer = randint(0, len(floor_normal)-1)
        img = floor_normal[self.nomer]
        super().__init__(img, x, y)
        self.danger = False

    def update(self):
        global FRAME
        if FRAME == 29:
            if self.danger:
                self.image = floor_normal[self.nomer]
            else:
                self.image = floor_danger[self.nomer]
            self.danger = not self.danger


class Player(SimpleSprite):
    def __init__(self, img, x, y, speed = 4.4):
        super().__init__(img, x, y)
        self.rect.center = (x, y)
        self.speed = speed
        self.direction = 'right'
        self.next_direction = 'right'

    def up(self):
        if self.rect.top > 0 and not sprite.spritecollide(self, walls, False):
            self.y -= self.speed
        for w in walls.sprites():
            if self.rect.colliderect(w.rect):
                self.y += self.speed*5
                self.direction = 'down'
                self.next_direction = 'down'
    def down(self):
        if self.rect.bottom < win_h and not sprite.spritecollide(self, walls, False):
            self.y += self.speed
        for w in walls.sprites():
            if self.rect.colliderect(w.rect):
                self.y -= self.speed*5
                self.direction = 'up'
                self.next_direction = 'up'
    def left(self):
        if self.rect.left > 0 and not sprite.spritecollide(self, walls, False):
            self.x -= self.speed
        for w in walls.sprites():
            if self.rect.colliderect(w.rect):
                self.x += self.speed*5
                self.direction = 'right'
                self.next_direction = 'right'
    def right(self):
        if not sprite.spritecollide(self, walls, False):
            self.x += self.speed
        if self.x >= win_w:
            new_floor()
            new_walls()
            new_enemy(5)
            self.x = 64
        for w in walls.sprites():
            if self.rect.colliderect(w.rect):
                self.x -= self.speed*5
                self.direction = 'left'
                self.next_direction = 'left'

    def update(self):
        global TACT, FRAME
        keys = key.get_pressed()
        if keys[K_SPACE] and FRAME == 29:
            Bullet(player.x-15, player.y-15, player.direction).add(bullets)
        if TACT:
            if keys[K_d] and self.next_direction != 'right':
                self.next_direction = 'right'
                TACT = False
            elif keys[K_a] and self.next_direction != 'left':
                self.next_direction = 'left'
                TACT = False
            elif keys[K_w] and self.next_direction != 'up':
                self.next_direction = 'up'
                TACT = False
            elif keys[K_s] and self.next_direction != 'down':
                self.next_direction = 'down'
                TACT = False
        self.direction = self.next_direction
        if self.direction == 'right':
            self.right()
        elif self.direction == 'up':
            self.up()
        elif self.direction == 'down':
            self.down()
        elif self.direction == 'left':
            self.left()
        if FRAME == 29:
            self.image = idle[(idle.index(self.image)+1)%len(idle)]

    def reset(self):
        self.rect.center = (self.x, self.y)
        self.screen.blit(self.image, self.rect.topleft)


class Enemy(Player):
    def right(self):
        if self.rect.right < win_w and not sprite.spritecollide(self, walls, False):
            self.x += self.speed
        for w in walls.sprites():
            if self.rect.colliderect(w.rect):
                self.x -= self.speed*5
                self.direction = 'left'
                self.next_direction = 'left'
    def update(self):
        global TACT, FRAME
        self.direction = self.next_direction
        if self.direction == 'right':
            self.right()
        elif self.direction == 'up':
            self.up()
        elif self.direction == 'down':
            self.down()
        elif self.direction == 'left':
            self.left()
        if FRAME == 29:
            self.image = enemy_img[(enemy_img.index(self.image)+1)%len(enemy_img)]
            self.direction = choice(['up', 'down', 'left', 'right'])
            self.next_direction = choice(['up', 'down', 'left', 'right'])

class Bullet(SimpleSprite):
    def __init__(self, x, y, direction):
        if direction == 'right':
            img = b_right_img
        elif direction == 'left':
            img = b_left_img
        elif direction == 'up':
            img = b_up_img
        elif direction == 'down':
            img = b_down_img
        super().__init__(img, x, y)
        self.direction = direction
    def update(self):
        if self.direction == 'right':
            self.x += 9.9
        elif self.direction == 'left':
            self.x -= 9.9
        elif self.direction == 'up':
            self.y -= 9.9
        elif self.direction == 'down':
            self.y += 9.9




def new_floor():
    floor.empty()
    for x in range(win_w//128+1):
        for y in range(win_h//128+1):
            Tile(x*128, y*128).add(floor)

def new_walls():
    walls.empty()
    for i in range(1, win_w//128):
        y = randint(0, win_h//128)
        SimpleSprite(choice([wall_img]), i*128, y*128 - 9).add(walls)
        y = randint(0, win_h//128)
        SimpleSprite(choice([wall2_img]), i*128-9, y*128).add(walls)

def new_enemy(x=1):
    enemies.empty()
    for i in range(x):
        e1 = Enemy(enemy_img[0], randint(0, win_w), randint(0, win_h), speed = 2.2)
        while sprite.spritecollide(e1, walls, False):
            e1 = Enemy(enemy_img[0], randint(0, win_w), randint(0, win_h), speed = 2.2)
        e1.add(enemies)

new_floor()
new_walls()
new_enemy(5)
player = Player(idle[0], 0, 128*5)
mixer.music.load('beat.mp3')
mixer.music.play(100)
run = True
FRAME = 0
TACT = False
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
    window.fill(white)
    floor.update()
    floor.reset()
    player.update()
    player.reset()
    walls.draw(window)
    enemies.update()
    enemies.reset()
    bullets.update()
    bullets.reset()
    sprite.groupcollide(bullets, walls, True, True)
    sprite.groupcollide(bullets, enemies, True, True)
    FRAME += 1
    if FRAME == 25:
        TACT = True
    elif FRAME == 30:
        FRAME = 0
    elif FRAME == 5:
        TACT = False
    display.update()
    clock.tick_busy_loop(60)
