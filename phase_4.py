from player import Martina
from enemy import Soldier, Drone
import random
from PPlay.window import *
from PPlay.sprite import *
from PPlay.mouse import *
from PPlay.sound import *
from functions import *


def generate_phase_4(window):
    random.seed(38)
    length_phase_1 = 5000

    # --- Floor 1 ---
    cover = 0
    enemies_spawn, boxes_spawn, spikes_spawn, landmine_spawn = 0.5, 0.6, 0.4, 0.2
    first_floor_1, boxes_floor_1, spikes_floor_1, enemies_floor_1, landmines_floor_1 = [], [], [], [], []
    get_coords = True

    while length_phase_1 > cover:
        new_floor = Sprite("images/phase_4_elements/phase_4_floor_1.png")
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
            if abs(spike.x - x_floor_1) > 150:
                spikes_floor_1.append(spike)

        if random.random() < landmine_spawn:
            landmine = Sprite("images/general_elements/landmine.png")
            landmine.x = new_floor.x + new_floor.width / random.randint(1, 5)
            landmine.y = new_floor.y - landmine.height
            if abs(landmine.x - x_floor_1) > 150:
                landmines_floor_1.append(landmine)

    # --- Floor 2 ---
    cover = 177
    enemies_spawn, boxes_spawn, spikes_spawn, landmine_spawn = 0.5, 0.6, 0.4, 0.2
    first_floor_2, boxes_floor_2, spikes_floor_2, enemies_floor_2, landmines_floor_2 = [], [], [], [], []

    while length_phase_1 > cover:
        new_floor = Sprite("images/phase_4_elements/phase_4_floor_2.png")
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

        
        if random.random() < landmine_spawn:
            landmine = Sprite("images/general_elements/landmine.png")
            landmine.x = new_floor.x + new_floor.width / random.randint(1, 5)
            landmine.y = new_floor.y - landmine.height
            landmines_floor_2.append(landmine)

    matrix_floor_1 = [first_floor_1, boxes_floor_1, spikes_floor_1, enemies_floor_1, landmines_floor_1]
    matrix_floor_2 = [first_floor_2, boxes_floor_2, spikes_floor_2, enemies_floor_2, landmines_floor_2]

    return matrix_floor_1, matrix_floor_2, y_floor_1, x_floor_1

# --- Som fase 4 ---
som_fase_4 = Sound("sounds/som_fase_4.mp3")
som_fase_4.set_volume(20)

power_ready = Sprite("images/general_elements/poder_pronto.png")
power_ready.set_position(250, 20)  

def run_phase_4(keyboard, mouse, window, matrix_floor_1, matrix_floor_2, y_floor_1, x_floor_1):
    window.set_title("FASE 3: EUROPA")
    backview = Sprite("images/phase_4_elements/phase_4_backview.png")
    som_fase_4.loop = True
    som_fase_4.play()
    martina = Martina(x_floor_1, y_floor_1)
    martina.y = y_floor_1 - martina.idle.height
    martina.x = x_floor_1

    heart_full = Sprite("images/general_elements/vida.png")
    heart_spacing = heart_full.width + 5
    heart_y = 10

    world_x = x_floor_1
    bullet_speed = 400
    tiro_cooldown = 0
    end_game = False
    win = False
    explosions = []

    drone = Drone(300)

    drone_respawn_timer = 0


    # Game Loop
    while True:
        dt = window.delta_time()

        backview.draw()
        draw_floor(matrix_floor_1)
        draw_floor(matrix_floor_2)

        martina.damage_cooldown -= dt
        tiro_cooldown -= dt
        martina.invencivel_timer -= dt
        martina.especial_cooldown -= dt

        camera_x = 0
        andando = False
        atirando = False

        if drone is None:

            drone_respawn_timer -= dt

            if drone_respawn_timer <= 0:
                drone = Drone(martina.x)
        
        if martina.especial_cooldown <= 0:
            power_ready.draw()

        # Teclado player
        if keyboard.key_pressed("D"):
            andando = True
            world_x += martina.speed * dt
            if martina.x < window.width / 2 - martina.player.width / 2:
                martina.x += martina.speed * dt
            else:
                camera_x = -martina.speed * dt

        if keyboard.key_pressed("A"):
            andando = True
            world_x -= martina.speed * dt
            if martina.x > window.width / 2 - martina.player.width / 2:
                martina.x -= martina.speed * dt
            else:
                camera_x = martina.speed * dt

        martina.especial(keyboard)

        if keyboard.key_pressed("space") and martina.on_ground and not martina.pulando:
            martina.vy = martina.jump_force
            martina.pulando = True

        # Mouse player
        if mouse.is_button_pressed(1):
            atirando = True
            if tiro_cooldown <= 0:
                martina.weapon_sound.play()
                tiro_cooldown = 0.8
                proj = Sprite("images/general_elements/tiro.png")
                proj.x = martina.x + martina.player.width
                proj.vx = bullet_speed
                proj.y = martina.y + (martina.player.height / 3) - (proj.height / 2)
                martina.tiros.append(proj)

        # --- Move elementos do mundo com a câmera ---
        for floor_matrix in [matrix_floor_1, matrix_floor_2]:
            for row in floor_matrix:
                for element in row:
                    if isinstance(element, Soldier):
                        element.apply_camera(camera_x)
                    else:
                        element.x += camera_x

        if drone:
            drone.apply_camera(camera_x)

        for proj in martina.tiros:
            proj.x += camera_x

        # --- Colisão player/chão ---
        martina.on_ground = False
        ground_y = None
        player_screen_center = martina.x + martina.player.width / 2

        for floor_matrix in [matrix_floor_1, matrix_floor_2]:
            for tile in floor_matrix[0]:
                x_overlap = tile.x < player_screen_center < tile.x + tile.width
                player_bottom = martina.y + martina.player.height
                y_overlap = (
                    player_bottom >= tile.y and
                    player_bottom <= tile.y + tile.height + max(abs(martina.vy * dt) + 10, 20)
                )
                if x_overlap and y_overlap and martina.vy >= 0:
                    martina.on_ground = True
                    ground_y = tile.y - martina.player.height
                    break
            if martina.on_ground:
                break

        # --- Dano por espinhos ---
        if martina.damage_cooldown <= 0 and martina.invencivel_timer <= 0:
            for floor_matrix in [matrix_floor_1, matrix_floor_2]:
                for spike in floor_matrix[2]:
                    if spike.collided(martina.player):
                        martina.hurt_sound.play()
                        martina.take_damage()
                        martina.damage_cooldown = 1.5
                        break
        
        # Mina
        for explosion in explosions:
            explosion[1] -= dt
            explosion[0].x += camera_x
            explosion[0].draw()
            if explosion[1] <= 0:
                explosions.remove(explosion)

        # dano pela mina
        if martina.damage_cooldown <= 0 and martina.invencivel_timer <= 0:
            for floor_matrix in [matrix_floor_1, matrix_floor_2]:
                for i, landmine in enumerate(floor_matrix[4]):
                    sx = landmine.x < martina.x + martina.player.width and landmine.x + landmine.width > martina.x
                    sy = landmine.y < martina.y + martina.player.height and landmine.y + landmine.height > martina.y
                    if sx and sy:
                        explosion = Sprite("images/general_elements/explosion.png")
                        explosion_sound = Sound("sounds/landmine_explosion.mp3")
                        explosion.x = landmine.x
                        explosion.y = landmine.y
                        explosions.append([explosion, 0.5])
                        # colocar som de explosão aqui: explosion_sound.play()
                        explosion_sound.play()
                        floor_matrix[4].pop(i)
                        martina.hurt_sound.play()
                        martina.take_damage()
                        martina.damage_cooldown = 1.5
                        break

        # --- Gravidade ---
        if martina.on_ground and not martina.pulando:
            martina.vy = 0
            martina.y = ground_y
        else:
            martina.vy += martina.gravity * dt
            martina.y += martina.vy * dt
        if martina.on_ground and martina.vy >= 0:
            martina.pulando = False

        # --- Condições de fim ---
        # --- sair manualmente ---
        if keyboard.key_pressed('esc'):
            end_game = True

        if martina.y > window.height:
            end_game = True
        if martina.hp <= 0:
            end_game = True
        if not matrix_floor_1[3] and not matrix_floor_2[3]:
            end_game = True
            win = True

        # --- Animação do martina ---
        novo_player = martina.shoot if atirando else (martina.walk if andando else martina.idle)
        if novo_player != martina.player:
            martina.reset_sprite(novo_player)
            martina.player = novo_player

        martina.player.x = martina.x
        martina.player.y = martina.y
        martina.player.draw()
        martina.safe_update(martina.player)

        # --- Tiros ---
        for proj in martina.tiros:
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

            if drone and not hit:

                dx = drone.walk.x
                dy = drone.walk.y
                dw = drone.walk.width
                dh = drone.walk.height

                px = proj.x < dx + dw and proj.x + proj.width > dx
                py = proj.y < dy + dh and proj.y + proj.height > dy

                if px and py:

                    if drone.take_hit():
                        drone = None
                        drone_respawn_timer = 10

                    hit = True

            if hit:
                martina.tiros.remove(proj)
                continue

            if proj.x > window.width or proj.x + proj.width < 0:
                martina.tiros.remove(proj)

        # --- Lógica dos inimigos ---
        for floor_matrix in [matrix_floor_1, matrix_floor_2]:
            for enemy in floor_matrix[3]:
                enemy.update(dt, martina, bullet_speed)
                enemy.draw()

        # --- HUD: corações ---
        for i in range(martina.hp):
            heart_full.x = 10 + i * heart_spacing
            heart_full.y = heart_y
            heart_full.draw()

        if drone:
            drone.update(dt, martina, bullet_speed)
            drone.draw()

        # --- Caixas de cura ---
        if martina.hp < martina.max_hp:
            for floor_matrix in [matrix_floor_1, matrix_floor_2]:
                for box in floor_matrix[1]:
                    if box.collided(martina.player):
                        floor_matrix[1].remove(box)
                        martina.heal()

        if end_game:
            som_fase_4.stop()
            return True, win

        window.update()