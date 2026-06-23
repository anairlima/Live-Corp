from player import Dandara
from enemy import Soldier
import random
from PPlay.window import *
from PPlay.sprite import *
from PPlay.mouse import *
from PPlay.sound import *
from functions import *


def generate_phase_1(window):
    random.seed(15)
    length_phase_1 = 5000

    # --- Floor 1 ---
    cover = 0
    enemies_spawn, boxes_spawn, spikes_spawn = 0.5, 0.6, 0.4
    first_floor_1, boxes_floor_1, spikes_floor_1, enemies_floor_1 = [], [], [], []
    get_coords = True

    while length_phase_1 > cover:
        new_floor = Sprite("images/phase_1_elements/phase_1_floor_1.png")
        new_floor.x = cover
        new_floor.y = window.height - (new_floor.height * 1.5)

        if get_coords:
            x_floor_1 = new_floor.x
            y_floor_1 = new_floor.y
            get_coords = False

        first_floor_1.append(new_floor)
        cover += random.randint(int(new_floor.width), int(new_floor.width * 2))

        if random.random() < enemies_spawn:
            ref = Sprite("images/enemies_images/soldier-idle.png", 7)
            enemy = Soldier(new_floor.x + new_floor.width / 2,
                            new_floor.y - ref.height, 
                            left_bound=new_floor.x,
                            right_bound=new_floor.x + new_floor.width)
            enemies_floor_1.append(enemy)

        if random.random() < boxes_spawn:
            box = Sprite("images/general_elements/box.png")
            box.x = new_floor.x + new_floor.width / 2
            box.y = new_floor.y - box.height
            boxes_floor_1.append(box)

        if random.random() < spikes_spawn:
            spike = Sprite("images/general_elements/spike.png")
            spike.x = new_floor.x + new_floor.width / random.randint(1, 5)
            spike.y = new_floor.y - spike.height
            spikes_floor_1.append(spike)

    # --- Floor 2 ---
    cover = 177
    enemies_spawn, boxes_spawn, spikes_spawn = 0.5, 0.6, 0.4
    first_floor_2, boxes_floor_2, spikes_floor_2, enemies_floor_2 = [], [], [], []

    while length_phase_1 > cover:
        new_floor = Sprite("images/phase_1_elements/phase_1_floor_2.png")
        new_floor.x = cover
        new_floor.y = window.height - (new_floor.height * 18)

        first_floor_2.append(new_floor)
        cover += random.randint(int(new_floor.width), int(new_floor.width * 2.5))

        if random.random() < enemies_spawn:
            ref = Sprite("images/enemies_images/soldier-idle.png", 7)
            enemy = Soldier(new_floor.x + new_floor.width / 2,
                            new_floor.y - ref.height,
                            left_bound=new_floor.x,
                            right_bound=new_floor.x + new_floor.width)
            enemies_floor_2.append(enemy)

        if random.random() < boxes_spawn:
            box = Sprite("images/general_elements/box.png")
            box.x = new_floor.x + new_floor.width / 2
            box.y = new_floor.y - box.height
            boxes_floor_2.append(box)

        if random.random() < spikes_spawn:
            spike = Sprite("images/general_elements/spike.png")
            spike.x = new_floor.x + new_floor.width / random.randint(1, 5)
            spike.y = new_floor.y - spike.height
            spikes_floor_2.append(spike)

    matrix_floor_1 = [first_floor_1, boxes_floor_1, spikes_floor_1, enemies_floor_1]
    matrix_floor_2 = [first_floor_2, boxes_floor_2, spikes_floor_2, enemies_floor_2]

    return matrix_floor_1, matrix_floor_2, y_floor_1, x_floor_1

# --- Som Fase 1 ---
som_fase_1 = Sound("sounds/som_fase_1.mp3")
som_fase_1.set_volume(20)

power_ready = Sprite("images/general_elements/poder_pronto.png")
power_ready.set_position(200, 20)  

def run_phase_1(keyboard, mouse, window, matrix_floor_1, matrix_floor_2, y_floor_1, x_floor_1):
    window.set_title("FASE 1: DESERTO")
    backview = Sprite("images/phase_1_elements/phase_1_backview.png")
    som_fase_1.loop = True
    som_fase_1.play()
    dandara = Dandara(x_floor_1, y_floor_1)
    dandara.y = y_floor_1 - dandara.idle.height
    dandara.x = x_floor_1

    heart_full = Sprite("images/general_elements/vida.png")
    heart_spacing = heart_full.width + 5
    heart_y = 10

    world_x = x_floor_1
    bullet_speed = 400
    tiro_cooldown = 0
    end_game = False
    win = False

    # Game Loop
    while True:
        
        dt = window.delta_time()

        backview.draw()
        draw_floor(matrix_floor_1)
        draw_floor(matrix_floor_2)

        dandara.damage_cooldown -= dt
        dandara.especial_cooldown -= dt
        tiro_cooldown -= dt

        camera_x = 0
        andando = False
        atirando = False

        if dandara.especial_cooldown <= 0:
            power_ready.draw()

        if keyboard.key_pressed("D"):
            andando = True
            world_x += dandara.speed * dt
            if dandara.x < window.width / 2 - dandara.player.width / 2:
                dandara.x += dandara.speed * dt
            else:
                camera_x = -dandara.speed * dt

        if keyboard.key_pressed("A"):
            andando = True
            world_x -= dandara.speed * dt
            if dandara.x > window.width / 2 - dandara.player.width / 2:
                dandara.x -= dandara.speed * dt
            else:
                camera_x = dandara.speed * dt

        dandara.especial(keyboard)

        if keyboard.key_pressed("space") and dandara.on_ground and not dandara.pulando:
            dandara.vy = dandara.jump_force
            dandara.pulando = True

        if mouse.is_button_pressed(1):
            atirando = True
            if tiro_cooldown <= 0:
                dandara.weapon_sound.play()
                tiro_cooldown = 0.8
                proj = Sprite("images/general_elements/tiro.png")
                proj.x = dandara.x + dandara.player.width
                proj.vx = bullet_speed
                proj.y = dandara.y + (dandara.player.height / 3) - (proj.height / 2)
                dandara.tiros.append(proj)
                
        # --- Move elementos do mundo com a câmera ---
        for floor_matrix in [matrix_floor_1, matrix_floor_2]:
            for row in floor_matrix:
                for element in row:
                    if isinstance(element, Soldier):
                        element.apply_camera(camera_x)
                    else:
                        element.x += camera_x

        for proj in dandara.tiros:
            proj.x += camera_x

        # --- Colisão player/chão ---
        dandara.on_ground = False
        ground_y = None
        player_screen_center = dandara.x + dandara.player.width / 2

        for floor_matrix in [matrix_floor_1, matrix_floor_2]:
            for tile in floor_matrix[0]:
                x_overlap = tile.x < player_screen_center < tile.x + tile.width
                player_bottom = dandara.y + dandara.player.height
                y_overlap = (
                    player_bottom >= tile.y and
                    player_bottom <= tile.y + tile.height + max(abs(dandara.vy * dt) + 10, 20)
                )
                if x_overlap and y_overlap and dandara.vy >= 0:
                    dandara.on_ground = True
                    ground_y = tile.y - dandara.player.height
                    break
            if dandara.on_ground:
                break

        # --- Dano por espinhos ---
        if dandara.damage_cooldown <= 0:
            for floor_matrix in [matrix_floor_1, matrix_floor_2]:
                for spike in floor_matrix[2]:
                    if spike.collided(dandara.player):
                        dandara.hurt_sound.play()
                        dandara.take_damage()
                        dandara.damage_cooldown = 1.5
                        break

        # --- Gravidade ---
        if dandara.on_ground and not dandara.pulando:
            dandara.vy = 0
            dandara.y = ground_y
        else:
            dandara.vy += dandara.gravity * dt
            dandara.y += dandara.vy * dt
        if dandara.on_ground and dandara.vy >= 0:
            dandara.pulando = False

        # --- Condições de fim ---
        # --- sair manualmente ---
        if keyboard.key_pressed('esc'):
            end_game = True
            
        if dandara.y > window.height:
            end_game = True
        if dandara.hp <= 0:
            end_game = True
        if not matrix_floor_1[3] and not matrix_floor_2[3]:
            end_game = True
            win = True

        # --- Animação da Dandara ---
        novo_player = dandara.shoot if atirando else (dandara.walk if andando else dandara.idle)
        if novo_player != dandara.player:
            dandara.reset_sprite(novo_player)
            dandara.player = novo_player

        dandara.player.x = dandara.x
        dandara.player.y = dandara.y
        dandara.player.draw()
        dandara.safe_update(dandara.player)

        # --- Tiros da Dandara  ---
        for proj in dandara.tiros:
            proj.x += proj.vx * dt
            proj.draw()

            hit = False
            for floor_matrix in [matrix_floor_1, matrix_floor_2]:
                for enemy in floor_matrix[3]:
                    ex = enemy.idle.x
                    ey = enemy.idle.y
                    ew = enemy.idle.width
                    eh = enemy.idle.height
                    px = proj.x < ex + ew and proj.x + proj.width > ex
                    py = proj.y < ey + eh and proj.y + proj.height > ey
                    if px and py:
                        if enemy.take_hit():
                            floor_matrix[3].remove(enemy)
                        hit = True
                        break
                if hit:
                    break

            if hit:
                dandara.tiros.remove(proj)
                continue

            if proj.x > window.width or proj.x + proj.width < 0:
                dandara.tiros.remove(proj)

        # --- Lógica dos inimigos ---
        for floor_matrix in [matrix_floor_1, matrix_floor_2]:
            for enemy in floor_matrix[3]:
                enemy.update(dt, dandara, bullet_speed)
                enemy.draw()

        # --- HUD: corações ---
        for i in range(dandara.hp):
            heart_full.x = 10 + i * heart_spacing
            heart_full.y = heart_y
            heart_full.draw()

        # --- Caixas de cura ---
        if dandara.hp < dandara.max_hp:
            for floor_matrix in [matrix_floor_1, matrix_floor_2]:
                for box in floor_matrix[1]:
                    if box.collided(dandara.player):
                        floor_matrix[1].remove(box)
                        dandara.heal()
        
    
        if end_game:
            som_fase_1.stop()
            return True, win

        window.update()