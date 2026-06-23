from player import Karma
from enemy import Soldier, Drone
import random
from PPlay.window import *
from PPlay.sprite import *
from PPlay.mouse import *
from PPlay.sound import *
from functions import *

def generate_phase_3(window):
    random.seed(50)
    length_phase_1 = 5000

    # --- Floor 1 ---
    cover = 0
    enemies_spawn, boxes_spawn, spikes_spawn, landmine_spawn = 0.5, 0.6, 0.4, 0.2
    first_floor_1, boxes_floor_1, spikes_floor_1, enemies_floor_1, landmines_floor_1 = [], [], [], [], []
    get_coords = True

    while length_phase_1 > cover:
        new_floor = Sprite("images/phase_3_elements/phase_3_floor_1.png")
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

        if random.random() < landmine_spawn:
            landmine = Sprite("images/general_elements/landmine.png")
            landmine.x = new_floor.x + new_floor.width / random.randint(1, 5)
            landmine.y = new_floor.y - landmine.height
            landmines_floor_1.append(landmine)

    # --- Floor 2 ---
    cover = 177
    enemies_spawn, boxes_spawn, spikes_spawn, landmine_spawn = 0.5, 0.6, 0.4, 0.2
    first_floor_2, boxes_floor_2, spikes_floor_2, enemies_floor_2, landmines_floor_2 = [], [], [], [], []

    while length_phase_1 > cover:
        new_floor = Sprite("images/phase_3_elements/phase_3_floor_2.png")
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

# --- Som fase 3 ---
som_fase_3 = Sound("sounds/som_fase_3.mp3")
som_fase_3.set_volume(20)

power_ready = Sprite("images/general_elements/poder_pronto.png")
power_ready.set_position(250, 20)  

def run_phase_3(keyboard, mouse, window, matrix_floor_1, matrix_floor_2, y_floor_1, x_floor_1):
    window.set_title("FASE 3: ÁSIA")
    backview = Sprite("images/phase_3_elements/phase_3_backview.png")
    som_fase_3.loop = True
    som_fase_3.play()

    karma = Karma(x_floor_1, y_floor_1)
    karma.y = y_floor_1 - karma.idle.height
    karma.x = x_floor_1

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

        karma.damage_cooldown -= dt
        karma.especial_cooldown -= dt
        tiro_cooldown -= dt

        camera_x = 0
        andando = False
        atirando = False

        if drone is None:

            drone_respawn_timer -= dt

            if drone_respawn_timer <= 0:
                drone = Drone(karma.x)

        if karma.especial_cooldown <= 0:
            power_ready.draw()

        # Teclado player
        if keyboard.key_pressed("D"):
            andando = True
            world_x += karma.speed * dt
            if karma.x < window.width / 2 - karma.player.width / 2:
                karma.x += karma.speed * dt
            else:
                camera_x = -karma.speed * dt

        if keyboard.key_pressed("A"):
            andando = True
            world_x -= karma.speed * dt
            if karma.x > window.width / 2 - karma.player.width / 2:
                karma.x -= karma.speed * dt
            else:
                camera_x = karma.speed * dt

        karma.especial(keyboard, matrix_floor_1[3], matrix_floor_2[3])

        if keyboard.key_pressed("space") and karma.on_ground and not karma.pulando:
            karma.vy = karma.jump_force
            karma.pulando = True

        # Mouse player
        if mouse.is_button_pressed(1):
            atirando = True
            if tiro_cooldown <= 0:
                karma.weapon_sound.play()
                tiro_cooldown = 2.0
                proj = Sprite("images/general_elements/tiro.png")
                proj.x = karma.x + karma.player.width
                proj.vx = bullet_speed
                proj.y = karma.y + (karma.player.height / 3) - (proj.height / 2)
                karma.tiros.append(proj)

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

        for proj in karma.tiros:
            proj.x += camera_x

        # --- Colisão player/chão ---
        karma.on_ground = False
        ground_y = None
        player_screen_center = karma.x + karma.player.width / 2

        for floor_matrix in [matrix_floor_1, matrix_floor_2]:
            for tile in floor_matrix[0]:
                x_overlap = tile.x < player_screen_center < tile.x + tile.width
                player_bottom = karma.y + karma.player.height
                y_overlap = (
                    player_bottom >= tile.y and
                    player_bottom <= tile.y + tile.height + max(abs(karma.vy * dt) + 10, 20)
                )
                if x_overlap and y_overlap and karma.vy >= 0:
                    karma.on_ground = True
                    ground_y = tile.y - karma.player.height
                    break
            if karma.on_ground:
                break

        # --- Dano por espinhos ---
        if karma.damage_cooldown <= 0:
            for floor_matrix in [matrix_floor_1, matrix_floor_2]:
                for spike in floor_matrix[2]:
                    if spike.collided(karma.player):
                        karma.hurt_sound.play()
                        karma.take_damage()
                        karma.damage_cooldown = 1.5
                        break
        
        # Mina

        for explosion in explosions:
            explosion[1] -= dt
            explosion[0].x += camera_x
            explosion[0].draw()
            if explosion[1] <= 0:
                explosions.remove(explosion)

        # dano pela mina
        if karma.damage_cooldown <= 0:
            for floor_matrix in [matrix_floor_1, matrix_floor_2]:
                for i, landmine in enumerate(floor_matrix[4]):
                    sx = landmine.x < karma.x + karma.player.width and landmine.x + landmine.width > karma.x
                    sy = landmine.y < karma.y + karma.player.height and landmine.y + landmine.height > karma.y
                    if sx and sy:
                        explosion = Sprite("images/general_elements/explosion.png")
                        explosion_sound = Sound("sounds/landmine_explosion.mp3")
                        explosion.x = landmine.x
                        explosion.y = landmine.y
                        explosions.append([explosion, 0.5])
                        # colocar som de explosão aqui: explosion_sound.play()
                        explosion_sound.play()
                        floor_matrix[4].pop(i)
                        karma.hurt_sound.play()
                        karma.take_damage()
                        karma.damage_cooldown = 1.5
                        break

        # --- Gravidade ---
        if karma.on_ground and not karma.pulando:
            karma.vy = 0
            karma.y = ground_y
        else:
            karma.vy += karma.gravity * dt
            karma.y += karma.vy * dt
        if karma.on_ground and karma.vy >= 0:
            karma.pulando = False

        # --- Condições de fim ---
        # --- sair manualmente ---
        if keyboard.key_pressed('esc'):
            end_game = True

        if karma.y > window.height:
            end_game = True
            
        if karma.hp <= 0:
            end_game = True
        if not matrix_floor_1[3] and not matrix_floor_2[3]:
            end_game = True
            win = True

        # --- Animação do karma ---
        novo_player = karma.shoot if atirando else (karma.walk if andando else karma.idle)
        if novo_player != karma.player:
            karma.reset_sprite(novo_player)
            karma.player = novo_player

        karma.player.x = karma.x
        karma.player.y = karma.y
        karma.player.draw()
        karma.safe_update(karma.player)

        # --- Tiros ---
        for proj in karma.tiros:
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
                karma.tiros.remove(proj)
                continue

            if proj.x > window.width or proj.x + proj.width < 0:
                karma.tiros.remove(proj)

        # --- Lógica dos inimigos ---
        for floor_matrix in [matrix_floor_1, matrix_floor_2]:
            for enemy in floor_matrix[3]:
                enemy.update(dt, karma, bullet_speed)
                enemy.draw()
        
        if drone:
            drone.update(dt, karma, bullet_speed)
            drone.draw()

        # --- HUD: corações ---
        for i in range(karma.hp):
            heart_full.x = 10 + i * heart_spacing
            heart_full.y = heart_y
            heart_full.draw()

        # --- Caixas de cura ---
        if karma.hp < karma.max_hp:
            for floor_matrix in [matrix_floor_1, matrix_floor_2]:
                for box in floor_matrix[1]:
                    if box.collided(karma.player):
                        floor_matrix[1].remove(box)
                        karma.heal()

        if end_game:
            som_fase_3.stop()
            return True, win

        window.update()