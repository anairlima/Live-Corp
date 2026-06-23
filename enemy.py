import random
import time
from PPlay.sprite import *
from PPlay.sound import *


class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hp = 1
        self.projectiles = []
        self.shoot_timer = random.uniform(1, 2)
        self.shooting = False

    def take_hit(self):
        self.hp -= 1
        return self.hp <= 0

    def is_dead(self):
        return self.hp <= 0


class Soldier(Enemy):
    SPEED = 60

    def __init__(self, x, y, left_bound = None, right_bound = None):
        super().__init__(x, y)

        self.idle = Sprite("images/enemies_images/soldier-idle.png", 7)
        self.idle.set_sequence_time(1, 7, 800)
        self.idle.x = x
        self.idle.y = y
        self.reset_sprite(self.idle)

        self.shot = Sprite("images/enemies_images/soldier-shot.png", 4)
        self.shot.set_sequence_time(1, 4, 100)
        self.shot.x = x
        self.shot.y = y
        self.reset_sprite(self.shot)

        self.current = self.idle

        self.weapon_sound = Sound("sounds/battle-rifle.mp3")
        self.weapon_sound.set_volume(5)

        # --- Patrulha ---
        self.left_bound = left_bound if left_bound is not None else x
        self.right_bound = right_bound if right_bound is not None else x
        self.direction = random.choice([-1, 1])

    def reset_sprite(self, sprite):
        sprite.curr_frame = 0
        sprite.last_time = int(round(time.time() * 1000))
        sprite.playing = True

    def safe_update(self, sprite):
        if len(sprite.frame_duration) == 0:
            return
        if sprite.curr_frame >= len(sprite.frame_duration):
            sprite.curr_frame = 0
        sprite.update()

    def apply_camera(self, camera_x):
        self.idle.x += camera_x
        self.shot.x += camera_x
        self.x += camera_x
        self.left_bound += camera_x
        self.right_bound += camera_x
        for proj in self.projectiles:
            proj.x += camera_x

    def update(self, dt, player, bullet_speed):
        # --- Movimento de patrulha ---
        self.idle.x += self.direction * self.SPEED * dt
        self.x = self.idle.x

        if self.idle.x <= self.left_bound:
            self.idle.x = self.left_bound
            self.direction = 1
        elif self.idle.x + self.idle.width >= self.right_bound:
            self.idle.x = self.right_bound - self.idle.width
            self.direction = -1
        
        self.shoot_timer -= dt
        dist_x = abs(self.idle.x - player.x)

        if self.shoot_timer <= 0 and not self.shooting and dist_x < 600:
            
            self.weapon_sound.play()
            self.shooting = True
            self.shoot_timer = random.randint(1, 2)

            proj = Sprite("images/general_elements/tiro.png")
            proj.x = self.idle.x
            proj.y = self.idle.y + self.idle.height / 2 - proj.height / 2
            self.projectiles.append(proj)

        novo = self.shot if self.shooting else self.idle
        if novo != self.current:
            self.reset_sprite(novo)
            self.current = novo

        if self.shooting:
            if self.current.curr_frame >= len(self.current.frame_duration) - 1:
                self.shooting = False

        self.shot.x = self.idle.x
        self.shot.y = self.idle.y

        for proj in self.projectiles:
            proj.x -= bullet_speed * dt

            px = proj.x < player.x + player.player.width and proj.x + proj.width > player.x
            py = proj.y < player.y + player.player.height and proj.y + proj.height > player.y
            if px and py:
                player.hurt_sound.play()
                player.take_damage()
                self.projectiles.remove(proj)
                continue

            if proj.x < 0:
                self.projectiles.remove(proj)

    def draw(self):
        self.current.draw()
        self.safe_update(self.current)
        for proj in self.projectiles:
            proj.draw()


class Boss(Enemy):
    SPEED = 40
    LEFT_LIMIT = 80
    RIGHT_LIMIT = 850

    def __init__(self, x, y):
        super().__init__(x, y)
        self.hp = 20
        self.direction = -1

        self.idle = Sprite("images/enemies_images/boss-idle.png", 1)
        self.idle.x = x
        self.idle.y = y
        self.reset_sprite(self.idle)

        self.shot = Sprite("images/enemies_images/boss-shot.png", 3)
        self.shot.set_sequence_time(1, 3, 400)
        self.shot.x = x
        self.shot.y = y
        self.reset_sprite(self.shot)

        self.current = self.idle
        self.shoot_timer = random.uniform(0.5, 1)

        self.weapon_sound = Sound("sounds/battle-rifle.mp3")
        self.weapon_sound.set_volume(5)

    def reset_sprite(self, sprite):
        sprite.curr_frame = 0
        sprite.last_time = int(round(time.time() * 1000))
        sprite.playing = True

    def safe_update(self, sprite):
        if len(sprite.frame_duration) == 0:
            return
        if sprite.curr_frame >= len(sprite.frame_duration):
            sprite.curr_frame = 0
        sprite.update()

    def update(self, dt, player, bullet_speed):
        # --- Movimento vai e vem ---
        self.idle.x += self.direction * self.SPEED * dt
        self.x = self.idle.x

        if self.idle.x <= self.LEFT_LIMIT:
            self.idle.x = self.LEFT_LIMIT
            self.direction = 1
        elif self.idle.x + self.idle.width >= self.RIGHT_LIMIT:
            self.idle.x = self.RIGHT_LIMIT - self.idle.width
            self.direction = -1

        # --- Tiro do Boss ---
        self.shoot_timer -= dt
        if self.shoot_timer <= 0:
            self.weapon_sound.play()
            self.shooting = True
            self.shoot_timer = random.uniform(1, 2)

            proj = Sprite("images/general_elements/tiro.png")
            proj.x = self.idle.x - proj.width - 10
            proj.y = self.idle.y + self.idle.height / 2 - proj.height / 2
            proj.vx = -bullet_speed
            self.projectiles.append(proj)

        # --- Troca sprite ---
        novo = self.shot if self.shooting else self.idle
        if novo != self.current:
            self.reset_sprite(novo)
            self.current = novo

        if self.shooting:
            if self.current.curr_frame >= len(self.current.frame_duration) - 1:
                self.shooting = False

        self.shot.x = self.idle.x
        self.shot.y = self.idle.y

        # --- Move e colide projéteis ---
        for proj in self.projectiles:
            proj.x += proj.vx * dt
            if proj.collided(player.player):
                player.hurt_sound.play()
                player.take_damage()
                self.projectiles.remove(proj)
                continue

            if proj.x > 1100 or proj.x + proj.width < -100:
                self.projectiles.remove(proj)

    def draw(self):
        self.current.draw()
        self.safe_update(self.current)
        for proj in self.projectiles:
            proj.draw()


class DroneBoss(Enemy):
    SPEED = 250
    LEFT_LIMIT = 50
    RIGHT_LIMIT = 950

    def __init__(self, x, y):
        super().__init__(x, y)
        self.hp = 2
        self.direction = -1

        self.walk = Sprite("images/enemies_images/drone-walk.png", 8)
        self.walk.set_sequence_time(1, 8, 300)
        self.walk.x = x
        self.walk.y = y
        self.reset_sprite(self.walk)

        self.shoot_timer = random.uniform(0.2, 1)

        self.weapon_sound = Sound("sounds/battle-rifle.mp3")  # TROCAR
        self.weapon_sound.set_volume(5)

    def reset_sprite(self, sprite):
        sprite.curr_frame = 0
        sprite.last_time = int(round(time.time() * 1000))
        sprite.playing = True

    def safe_update(self, sprite):
        if len(sprite.frame_duration) == 0:
            return
        if sprite.curr_frame >= len(sprite.frame_duration):
            sprite.curr_frame = 0
        sprite.update()

    def update(self, dt, player, bullet_speed):
        # --- Movimento vai e vem ---
        self.walk.x += self.direction * self.SPEED * dt
        self.x = self.walk.x

        if self.walk.x <= self.LEFT_LIMIT:
            self.walk.x = self.LEFT_LIMIT
            self.direction = 1
        elif self.walk.x + self.walk.width >= self.RIGHT_LIMIT:
            self.walk.x = self.RIGHT_LIMIT - self.walk.width
            self.direction = -1

        # --- Disparo para baixo ---
        self.shoot_timer -= dt
        if self.shoot_timer <= 0:
            self.weapon_sound.play()
            self.shoot_timer = random.uniform(1, 3)

            proj = Sprite("images/general_elements/tiro.png")
            proj.x = self.walk.x + self.walk.width / 2 - proj.width / 2
            proj.y = self.walk.y + self.walk.height
            proj.vx = 0
            proj.vy = bullet_speed
            self.projectiles.append(proj)

        # --- Move e colide projéteis ---
        for proj in self.projectiles:
            proj.y += proj.vy * dt

            px = proj.x < player.x + player.player.width and proj.x + proj.width > player.x
            py = proj.y < player.y + player.player.height and proj.y + proj.height > player.y
            if px and py:
                player.hurt_sound.play()
                player.take_damage()
                self.projectiles.remove(proj)
                continue

            if proj.y > 800:
                self.projectiles.remove(proj)

    def draw(self):
        self.walk.draw()
        self.safe_update(self.walk)
        for proj in self.projectiles:
            proj.draw()


class Drone(Enemy):
    SPEED = 180
    Y_POS = 50

    def __init__(self, x, y=Y_POS):
        super().__init__(x, y)

        self.hp = 1
        self.direction = 1

        self.walk = Sprite("images/enemies_images/drone-walk.png", 8)
        self.walk.set_sequence_time(1, 8, 300)
        self.walk.x = x
        self.walk.y = y

        self.shoot_timer = random.uniform(2, 4)

        self.weapon_sound = Sound("sounds/battle-rifle.mp3")
        self.weapon_sound.set_volume(5)

    def reset_sprite(self, sprite):
        sprite.curr_frame = 0
        sprite.last_time = int(round(time.time() * 1000))
        sprite.playing = True

    def safe_update(self, sprite):
        if len(sprite.frame_duration) == 0:
            return
        if sprite.curr_frame >= len(sprite.frame_duration):
            sprite.curr_frame = 0
        sprite.update()

    def apply_camera(self, camera_x):
        self.walk.x += camera_x
        self.x += camera_x

        for proj in self.projectiles:
            proj.x += camera_x

    def update(self, dt, player, bullet_speed):

        # Mantém o drone no topo
        self.walk.y = self.Y_POS

        # Patrulha horizontal
        self.walk.x += self.direction * self.SPEED * dt

        if self.walk.x <= 0:
            self.walk.x = 0
            self.direction = 1

        elif self.walk.x + self.walk.width >= 1000:
            self.walk.x = 1000 - self.walk.width
            self.direction = -1

        self.x = self.walk.x

        centro_drone = self.walk.x + self.walk.width / 2
        centro_player = player.x + player.player.width / 2

        # Tiro apenas quando estiver próximo do jogador
        self.shoot_timer -= dt

        if self.shoot_timer <= 0 and abs(centro_drone - centro_player) < 20:

            self.weapon_sound.play()
            self.shoot_timer = random.uniform(2, 4)

            proj = Sprite("images/general_elements/tiro.png")

            proj.x = self.walk.x + self.walk.width / 2 - proj.width / 2
            proj.y = self.walk.y + self.walk.height

            proj.vx = 0
            proj.vy = bullet_speed

            self.projectiles.append(proj)

        # Atualiza projéteis
        for proj in self.projectiles[:]:

            proj.y += proj.vy * dt

            px = proj.x < player.x + player.player.width and proj.x + proj.width > player.x
            py = proj.y < player.y + player.player.height and proj.y + proj.height > player.y

            if px and py:
                player.hurt_sound.play()
                player.take_damage()
                self.projectiles.remove(proj)
                continue

            if proj.y > 800:
                self.projectiles.remove(proj)

    def draw(self):
        self.walk.draw()
        self.safe_update(self.walk)

        for proj in self.projectiles:
            proj.draw()

