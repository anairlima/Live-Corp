from PPlay.window import *
from PPlay.sprite import *
from PPlay.sound import *
from sprites import *
from player import Dandara, Ubirata, Karma, Martina
from enemy import Boss, DroneBoss


def generate_phase_5(window):

    # --- Floor 1: chão contínuo ---
    first_floor_1 = []
    tile_ref = Sprite("images/phase_5_elements/phase_5_floor_1.png")
    tile_w = tile_ref.width
    floor_y = window.height - tile_ref.height * 1.5

    cover = 0
    while cover < window.width + tile_w:
        tile = Sprite("images/phase_5_elements/phase_5_floor_1.png")
        tile.x = cover
        tile.y = floor_y
        first_floor_1.append(tile)
        cover += tile_w

    x_floor_1 = first_floor_1[0].x
    y_floor_1 = first_floor_1[0].y

    # --- Floor 2: 2 plataformas fixas ---
    first_floor_2 = []
    plat_ref = Sprite("images/phase_5_elements/phase_5_floor_2.png")
    plat_y = window.height - plat_ref.height * 18

    pos_plataformas = [150, 600]
    for px in pos_plataformas:
        plat = Sprite("images/phase_5_elements/phase_5_floor_2.png")
        plat.x = px
        plat.y = plat_y
        first_floor_2.append(plat)

    # --- Caixas de cura (em cima de cada plataforma) ---
    boxes = []
    box_ref = Sprite("images/general_elements/box.png")
    for plat in first_floor_2:
        box = Sprite("images/general_elements/box.png")
        box.x = plat.x + plat.width / 2 - box_ref.width / 2
        box.y = plat.y - box_ref.height
        boxes.append(box)

    matrix_floor_1 = [first_floor_1, boxes, [], []]
    matrix_floor_2 = [first_floor_2, [], [], []]

    return matrix_floor_1, matrix_floor_2, y_floor_1, x_floor_1

# --- Som fase 5 ---
som_fase_5 = Sound("sounds/som_fase_5.mp3")
som_fase_5.loop = True
som_fase_5.set_volume(5)

power_ready = Sprite("images/general_elements/poder_pronto.png")
power_ready.set_position(250, 20)  


def run_phase_5(keyboard, mouse, window, matrix_floor_1, matrix_floor_2, y_floor_1, x_floor_1, player):

    window.set_title("FASE 5: EUA")
    backview = Sprite("images/phase_5_elements/phase_5_backview.png")
    som_fase_5.play()

    # Posiciona o player no início
    player.y = y_floor_1 - player.idle.height
    player.x = x_floor_1 + 50

    # Boss começa no lado direito
    boss_ref = Sprite("images/enemies_images/boss-idle.png", 1)
    boss_x = window.width - boss_ref.width - 50
    boss_y = y_floor_1 - boss_ref.height
    boss = Boss(boss_x, boss_y)

    # Drone no céu
    drone = DroneBoss(100, 70)

    heart_full = Sprite("images/general_elements/vida.png")
    heart_spacing = heart_full.width + 5
    heart_y = 10
    tiro_cooldown = 0
    bullet_speed = 400
    end_game = False
    win = False
    box_respawn_cooldown = 0

    while True:
        dt = window.delta_time()
        backview.draw()

        # Desenha chão e plataformas
        for tile in matrix_floor_1[0]:
            tile.draw()
        for tile in matrix_floor_2[0]:
            tile.draw()

        # Desenha caixas de cura
        for box in matrix_floor_1[1]:
            box.draw()

        
        player.damage_cooldown -= dt
        player.especial_cooldown -= dt

        try:
            player.varias_flechas_timer -= dt
        except AttributeError:
            pass

        tiro_cooldown -= dt
        box_respawn_cooldown -= dt

        andando = False
        atirando = False

        if player.especial_cooldown <= 0:
            power_ready.draw()

        # --- Movimento do player ---
        if keyboard.key_pressed("D"):
            andando = True
            player.x += player.speed * dt
        if keyboard.key_pressed("A"):
            andando = True
            player.x -= player.speed * dt

        player.x = max(0, min(player.x, window.width - player.player.width))

        # --- Habilidade especial ---
        try:
            player.especial(keyboard)
        except TypeError:
            pass

        # --- Pulo ---
        if keyboard.key_pressed("space") and player.on_ground and not player.pulando:
            player.vy = player.jump_force
            player.pulando = True

        # --- Tiro do player ---
        if mouse.is_button_pressed(1):
            atirando = True

            if tiro_cooldown <= 0:
                tiro_cooldown = player.tiro_cooldown
                player.weapon_sound.play()

                proj = Sprite(player.proj)
                proj.x = player.x + player.player.width
                proj.vx = bullet_speed
                proj.y = player.y + player.player.height / 3 - proj.height / 2

                player.tiros.append(proj)

                if type(player) == Ubirata and player.varias_flechas_timer > 0:
                    proj2 = Sprite(player.proj)
                    proj2.x = player.x + player.player.width
                    proj2.vx = bullet_speed
                    proj2.y = proj.y - proj2.height
                    player.tiros.append(proj2)

        # --- Colisão player/chão ---
        player.on_ground = False
        ground_y = None
        player_cx = player.x + player.player.width / 2

        for floor_matrix in [matrix_floor_1, matrix_floor_2]:
            for tile in floor_matrix[0]:
                x_ok = tile.x < player_cx < tile.x + tile.width
                pb = player.y + player.player.height
                y_ok = pb >= tile.y and pb <= tile.y + tile.height + max(abs(player.vy * dt) + 10, 20)
                if x_ok and y_ok and player.vy >= 0:
                    player.on_ground = True
                    ground_y = tile.y - player.player.height
                    break
            if player.on_ground:
                break

        # --- Gravidade ---
        if player.on_ground and not player.pulando:
            player.vy = 0
            player.y = ground_y
        else:
            player.vy += player.gravity * dt
            player.y  += player.vy * dt
        if player.on_ground and player.vy >= 0:
            player.pulando = False

        # --- Caixas de cura ---
        if player.hp < player.max_hp:
            for box in matrix_floor_1[1][:]:
                if box.collided(player.player):
                    matrix_floor_1[1].remove(box)
                    player.heal()

                    if len(matrix_floor_1[1]) == 0:
                        box_respawn_cooldown = 2
        
        if len(matrix_floor_1[1]) == 0 and box_respawn_cooldown <= 0:

            box_ref = Sprite("images/general_elements/box.png")

            for plat in matrix_floor_2[0]:
                box = Sprite("images/general_elements/box.png")
                box.x = plat.x + plat.width / 2 - box_ref.width / 2
                box.y = plat.y - box_ref.height

                matrix_floor_1[1].append(box)

        # --- Tiros do player ---
        for proj in player.tiros:
            proj.x += proj.vx * dt
            proj.draw()

            if proj.collided(boss.current):
                boss.take_hit()
                player.tiros.remove(proj)
                continue

            if proj.collided(drone.walk):
                drone.take_hit()
                player.tiros.remove(proj)
                continue

            if proj.x > window.width or proj.x + proj.width < 0:
                player.tiros.remove(proj)

        # --- Animação do player ---
        novo_player = player.shoot if atirando else (player.walk if andando else player.idle)
        if novo_player != player.player:
            player.reset_sprite(novo_player)
            player.player = novo_player

        player.player.x = player.x
        player.player.y = player.y
        player.player.draw()
        player.safe_update(player.player)

        # --- Boss ---
        if not boss.is_dead():
            boss.update(dt, player, bullet_speed)
            boss.draw()

            # Colisão corpo a corpo
            bx = boss.idle.x < player.x + player.player.width and boss.idle.x + boss.idle.width > player.x
            by = boss.idle.y < player.y + player.player.height and boss.idle.y + boss.idle.height > player.y
            if bx and by and player.damage_cooldown <= 0:
                player.hurt_sound.play()
                player.take_damage()
                player.damage_cooldown = 1.5

            window.draw_text(f"BOSS HP: {boss.hp}", window.width / 2 - 60, 10, size=22, color=(255, 50, 50))

        # --- Drone ---
        if not drone.is_dead():
            drone.update(dt, player, bullet_speed)
            drone.draw()

        # --- HUD: corações do player ---
        for i in range(player.hp):
            heart_full.x = 10 + i * heart_spacing
            heart_full.y = heart_y
            heart_full.draw()

        # --- Condições de fim ---
        # --- sair manualmente ---
        if keyboard.key_pressed('esc'):
            end_game = True
            
        if player.hp <= 0:
            end_game = True
        if boss.is_dead():
            end_game = True
            win = True

        if end_game:
            som_fase_5.stop()
            return True, win

        window.update()