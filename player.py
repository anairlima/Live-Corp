from PPlay.window import *
from PPlay.sprite import *
from PPlay.mouse import *
from PPlay.sound import *
from PPlay.keyboard import *

import time

class Player:
    def __init__(self, x, y):
        # posição no mundo
        self.x = x
        self.y = y

        self.max_hp = 3 # vida base
        self.hp = self.max_hp

        # movimento
        self.speed = 250  # velocidade base
        self.vy = 0
        self.jump_force = -800
        self.gravity = 1200

        self.pulando = False
        self.on_ground = False
        self.andando = False

        # projéteis disparados pelo personagem
        self.tiros = []
        self.proj = "images/general_elements/tiro.png" # pra fase 5

        # cooldowns
        self.damage_cooldown = 0
        self.especial_cooldown = 0
        self.tiro_cooldown = 0.8

    def is_dead(self):
        return self.hp <= 0

    def take_damage(self):
        self.hp -= 1

    def heal(self):
        if self.hp < self.max_hp:
            self.hp += 1


    def reset_sprite(self, sprite):
        """Reinicia a animação de um sprite do zero."""
        sprite.curr_frame = 0
        sprite.last_time = int(round(time.time() * 1000))
        sprite.playing = True

    def safe_update(self, sprite):
        if len(sprite.frame_duration) == 0:
            return
        if sprite.curr_frame >= len(sprite.frame_duration):
            sprite.curr_frame = 0
        sprite.update()


class Dandara(Player):

    def __init__(self, x, y):
        super().__init__(x, y)
        # atributos base
        self.max_hp = 2
        self.hp = self.max_hp
        self.speed *= 2  # 2 unidades de velocidade

        # sprites de animação
        self.idle = Sprite("images/player/dandara-idle.png", 8)
        self.walk = Sprite("images/player/dandara-walk.png", 8)
        self.shoot = Sprite("images/player/dandara-shot.png", 4)

        self.idle.set_sequence_time(1, 8, 800)
        self.walk.set_sequence_time(1, 8, 300)
        self.shoot.set_sequence_time(1, 4, 400)

        self.reset_sprite(self.idle)
        self.reset_sprite(self.walk)
        self.reset_sprite(self.shoot)

        # sprite ativo no momento
        self.player = self.idle

        # sons
        self.weapon_sound = Sound("sounds/standard_rifle.mp3")
        self.weapon_sound.set_volume(5)

        self.hurt_sound = Sound("sounds/hurt.mp3")
        self.hurt_sound.set_volume(5)

    def especial(self, keyboard):
        if keyboard.key_pressed("E") and self.especial_cooldown <= 0 and self.hp < self.max_hp:
            self.heal_sound = Sound("sounds/heal_dandara.mp3")
            self.heal_sound.set_volume(40)
            self.heal_sound.play()
            self.heal()
            self.especial_cooldown = 10


class Ubirata(Player):
    def __init__(self, x, y):
        super().__init__(x, y)
        # atributos base
        self.max_hp = 2
        self.hp = self.max_hp
        self.speed *= 3

        # sprites de animação
        self.idle = Sprite("images/player/ubirata-idle.png")
        self.walk = Sprite("images/player/ubirata-walk.png", 6)
        self.shoot = Sprite("images/player/ubirata-shot.png", 3)

        self.walk.set_sequence_time(1, 6, 300)
        self.shoot.set_sequence_time(1, 3, 300)
        
        self.reset_sprite(self.walk)
        self.reset_sprite(self.shoot)

        # sprite ativo no momento
        self.player = self.idle
        self.proj = "images/general_elements/flecha.png" # pra fase 5

        # sons
        self.weapon_sound = Sound("sounds/arrow_ubirata.mp3")
        self.weapon_sound.set_volume(10)

        self.hurt_sound = Sound("sounds/hurt.mp3")
        self.hurt_sound.set_volume(5)

        # pro poder especial 
        self.varias_flechas_timer = 0
        self.especial_cooldown = 0

    # --- Poder: Várias flechas ---
    def especial(self, keyboard):
        if keyboard.key_pressed("E") and self.especial_cooldown <= 0:
            self.arrow_power_sound = Sound("sounds/arrowpower_ubirata.mp3")
            self.arrow_power_sound.set_volume(10)
            self.arrow_power_sound.play()
            self.varias_flechas_timer = 5
            self.especial_cooldown = 10
            pass

class Karma(Player):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.max_hp = 3
        self.hp = self.max_hp
        self.speed *= 1

        # sprites de animação
        self.idle = Sprite("images/player/karma-idle.png")
        self.walk = Sprite("images/player/karma-walk.png", 6)
        self.shoot = Sprite("images/player/karma-shot.png", 3)

        self.walk.set_sequence_time(1, 6, 300)
        self.shoot.set_sequence_time(1, 3, 600)
        
        self.reset_sprite(self.walk)
        self.reset_sprite(self.shoot)

        # sprite ativo no momento
        self.player = self.idle

        # sons
        self.weapon_sound = Sound("sounds/shotgun_karma.mp3")
        self.weapon_sound.set_volume(30)

        self.hurt_sound = Sound("sounds/hurt.mp3")
        self.hurt_sound.set_volume(5)

        self.tiro_cooldown = 2.0
        
        # poder especial
        self.especial_cooldown = 0

    def especial(self, keyboard, enemies_1, enemies_2):
        if keyboard.key_pressed("E") and self.especial_cooldown <= 0:
            self.push_sound = Sound("sounds/push_karma.mp3")
            self.push_sound.set_volume(20)
            self.push_sound.play()
            for enemy_list in [enemies_1, enemies_2]:
                for enemy in enemy_list:
                    ex = enemy.idle.x
                    ey = enemy.idle.y
                    ew = enemy.idle.width
                    eh = enemy.idle.height
                    px = self.x < ex + ew and self.x + self.player.width > ex
                    py = self.y < ey + eh and self.y + self.player.height > ey
                    if px and py:
                        enemy_list.remove(enemy)
            self.especial_cooldown = 5


class Martina(Player):
    def __init__(self, x, y):
        super().__init__(x, y)
        # atributos base
        self.max_hp = 2
        self.hp = self.max_hp
        self.speed *= 1

        self.idle  = Sprite("images/player/martina-idle.png", 2) 
        self.walk  = Sprite("images/player/martina-walk.png", 5)
        self.shoot = Sprite("images/player/martina-shot.png", 3)

        self.idle.set_sequence_time(1, 2, 600)
        self.walk.set_sequence_time(1, 5, 500)
        self.shoot.set_sequence_time(1, 3, 400)

        self.reset_sprite(self.idle)
        self.reset_sprite(self.walk)
        self.reset_sprite(self.shoot)

        # sprite ativo no momento
        self.player = self.idle

        # sons
        self.weapon_sound = Sound("sounds/standard_rifle.mp3")
        self.weapon_sound.set_volume(5)

        self.hurt_sound = Sound("sounds/hurt.mp3")
        self.hurt_sound.set_volume(5)

        # pro poder especial
        self.invencivel_timer = 0
        self.especial_cooldown = 0

    # invencivel contra espinhos e a mina por 10s
    def especial(self, keyboard):
        if keyboard.key_pressed("E") and self.especial_cooldown <= 0:
            self.powerup_sound = Sound("sounds/powerup_martina.mp3")
            self.powerup_sound.set_volume(10)
            self.powerup_sound.play()
            self.invencivel_timer = 10
            self.especial_cooldown = 20