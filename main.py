import textwrap
from PPlay.window import *
from PPlay.sprite import *
from sprites import *
from phase_1 import *
from phase_2 import *
from phase_3 import *
from phase_4 import *
from phase_5 import *
from player import Dandara, Ubirata, Karma, Martina



window = Window(1000, 700)
window.set_background_color((0, 0, 0))

keyboard = Window.get_keyboard()
mouse = Window.get_mouse()
menu_design = Sprite("images/menu/menu.png")

# fase 5 só aparece quando todas as 4 forem vencidas (true)
fase1_completa = False
fase2_completa = False
fase3_completa = False
fase4_completa = False
fase5_completa = False

def fase5_liberada():
    return fase1_completa and fase2_completa and fase3_completa and fase4_completa


def fim_fase(fase5_completa):
    mouse.set_position(window.width/2, window.height/1.5)

    while True:
        
        fundo_fases.draw()
        sair.draw()

        if win:
            if fase5_completa:
                window.draw_text("PARABÉNS! VOCÊ COMPLETOU TODAS AS FASES!", 200, window.height/2.5, size=28, color=(255, 255, 255))
                window.draw_text("OBRIGADO POR JOGAR !!!", 340, window.height/2, size=28, color=(255, 255, 255))
            else:
                window.draw_text("VOCÊ GANHOU!", 420, window.height/2.5, size=28, color=(255, 255, 255))
                window.draw_text("JOGUE A PROXIMA FASE!", 360, window.height/2, size=28, color=(255, 255, 255))
        else:
            window.draw_text("VOCÊ PERDEU!", 420, window.height/2.5, size=28, color=(255, 255, 255))
            

        if mouse.is_over_object(sair) and mouse.is_button_pressed(1):
            mouse.set_position(window.width/2, window.height/1.5)
            break

        window.update()


def selecao_personagem():
    fundo = Sprite("images/menu/menu_fundo.png", 1)

    # Sprites de preview de cada personagem (idle deles)
    prev_dandara  = Sprite("images/player/dandara-idle.png", 8)
    prev_ubirata  = Sprite("images/player/ubirata-idle.png")
    prev_karma    = Sprite("images/player/karma-idle.png")
    prev_martina  = Sprite("images/player/martina-idle.png", 2)

    prev_dandara.set_position(150, 250)
    prev_ubirata.set_position(320, 250)
    prev_karma.set_position(540, 250)
    prev_martina.set_position(750, 250)


    while True:
        fundo.draw()

        # Desenha os previews
        prev_dandara.draw()
        prev_ubirata.draw()
        prev_karma.draw()
        prev_martina.draw()
        voltar.draw()

        # Textos com o nome de cada personagem
        window.draw_text("Dandara",  135, 370, size=22, color=(255,255,255))
        window.draw_text("Ubiratã",  335, 370, size=22, color=(255,255,255))
        window.draw_text("Karma",    545, 370, size=22, color=(255,255,255))
        window.draw_text("Martina",  740, 370, size=22, color=(255,255,255))
        window.draw_text("Escolha seu personagem", 330, 150, size=32, color=(255,220,0))

        # Cliques nos personagens
        if mouse.is_over_object(prev_dandara) and mouse.is_button_pressed(1):
            mouse.set_position(window.width/2, window.height/2)
            return Dandara(100, 300)

        elif mouse.is_over_object(prev_ubirata) and mouse.is_button_pressed(1):
            mouse.set_position(window.width/2, window.height/2)
            return Ubirata(100, 300)

        elif mouse.is_over_object(prev_karma) and mouse.is_button_pressed(1):
            mouse.set_position(window.width/2, window.height/2)
            return Karma(100, 300)

        elif mouse.is_over_object(prev_martina) and mouse.is_button_pressed(1):
            mouse.set_position(window.width/2, window.height/2)
            return Martina(100, 300)

        elif mouse.is_over_object(voltar) and mouse.is_button_pressed(1):
            mouse.set_position(window.width/2, window.height/1.5)
            return None

        window.update()



def mostrar_historia():
    def desenhar_historia():
        y = 80
        for paragrafo in historia_texto:
            linhas = textwrap.wrap(paragrafo, width=100)

            for linha in linhas:
                window.draw_text(
                    linha,
                    60,
                    y,
                    size=22,
                    color=(255, 255, 255),
                    font_name="Arial"
                )
                y += 28

    historia_texto = [

        "Houve um tempo em que a terra ainda respirava. Os rios corriam "
        "livres, as montanhas guardavam seus segredos em silêncio, e o céu "
        "não tinha o gosto amargo da poeira industrial.",

        "Esse tempo acabou.",

        "A LIVE Corporation chegou prometendo progresso e cumpriu, à sua "
        "maneira. Suas perfuradoras rasgaram o solo em busca de minério, "
        "deixando atrás de si crateras, rios secos e cidades inteiras "
        "sufocadas pela poeira de suas minas. Quem ousou levantar a voz "
        "contra a empresa descobriu rápido o preço da dissidência: "
        "jornalistas silenciados, comunidades despejadas, vidas apagadas "
        "dos registros como se nunca tivessem existido.",

        "Mas toda opressão tem um ponto de ruptura.",

        "Da raiva engolida por anos, nasceram os núcleos rebeldes, grupos "
        "espalhados pelos quatro cantos do planeta, unidos não por uma "
        "bandeira, mas por uma sede comum de justiça. Eles não têm o poder "
        "de exércitos, nem a riqueza de corporações. Têm apenas a "
        "determinação de quem não tem mais nada a perder.",

        "Agora, em meio às dunas escaldantes do primeiro grande complexo "
        "minerador, uma nova resistente entra em cena. Seu objetivo é "
        "claro: infiltrar-se, sabotar, destruir, e provar que mesmo o "
        "império mais poderoso pode ruir, uma instalação de cada vez.",

        "O deserto está prestes a testemunhar o início do fim da LIVE Corporation.",

    ]

    mouse.set_position(window.width/2, window.height/4)

    while True:
        window.set_title("HISTÓRIA")

        fundo_fases.draw()
        voltar.draw()

        window.draw_text(
            "O MUNDO",
            window.width/2.2,
            window.height/20,
            size=28,
            color=(255,255,255)
        )
        
        desenhar_historia()

        if mouse.is_over_object(voltar) and mouse.is_button_pressed(1):
            mouse.set_position(window.width/2, window.height/1.2)
            break

        window.update()

# --- Som menu --- 
som_menu = Sound("sounds/som_menu.mp3")
som_menu.loop = True
som_menu.set_volume(20)
som_menu.play()

mostrar_historia()

while True:
    window.set_title("LIVE CORP")
    menu_design.draw()
    jogar.draw()
    historia.draw()
    sair.draw()

    if mouse.is_over_object(jogar) and mouse.is_button_pressed(1):
        mouse.set_position(window.width/2, window.height/4)

        while True:
            window.set_title("LIVE CORP")
            fundo_fases.draw()

            fase1.draw()
            fase2.draw()
            fase3.draw()
            fase4.draw()
            fase5_block.draw()

            # O botão fase 5 só funciona quando todas as anteriores foram vencidas
            if fase5_liberada():
                fase5.draw()

            # easter egg (atalho) pra liberar a fase 5:
            if keyboard.key_pressed("5"):
                fase1_completa = True
                fase2_completa = True
                fase3_completa = True
                fase4_completa = True
                fase5.draw()

            voltar.draw()

            # --- Fase 1 ---
            if mouse.is_over_object(fase1) and mouse.is_button_pressed(1):
                floor_1, floor_2, y_floor_1, x_floor_1 = generate_phase_1(window)
                som_menu.stop()
                window_end, win = run_phase_1(keyboard, mouse, window, floor_1, floor_2, y_floor_1, x_floor_1)
                if window_end:
                    if win:
                        fase1_completa = True
                    som_menu.play()
                    fim_fase(fase5_completa)
                    

            # --- Fase 2 ---
            elif mouse.is_over_object(fase2) and mouse.is_button_pressed(1):
                floor_1, floor_2, y_floor_1, x_floor_1 = generate_phase_2(window)
                som_menu.stop()
                window_end, win = run_phase_2(keyboard, mouse, window, floor_1, floor_2, y_floor_1, x_floor_1)
                if window_end:
                    if win:
                        fase2_completa = True
                    som_menu.play()
                    fim_fase(fase5_completa)
                    

            # --- Fase 3 ---
            elif mouse.is_over_object(fase3) and mouse.is_button_pressed(1):
                floor_1, floor_2, y_floor_1, x_floor_1 = generate_phase_3(window)
                som_menu.stop()
                window_end, win = run_phase_3(keyboard, mouse, window, floor_1, floor_2, y_floor_1, x_floor_1)
                if window_end:
                    if win:
                        fase3_completa = True
                    som_menu.play()
                    fim_fase(fase5_completa)
                    

            # --- Fase 4 ---
            elif mouse.is_over_object(fase4) and mouse.is_button_pressed(1):
                floor_1, floor_2, y_floor_1, x_floor_1 = generate_phase_4(window)
                som_menu.stop()
                window_end, win = run_phase_4(keyboard, mouse, window, floor_1, floor_2, y_floor_1, x_floor_1)
                if window_end:
                    if win:
                        fase4_completa = True
                    som_menu.play()
                    fim_fase(fase5_completa)
                    

            # --- Fase 5 ---
            elif fase5_liberada() and mouse.is_over_object(fase5) and mouse.is_button_pressed(1):
                mouse.set_position(window.width/2, window.height/2)
                
                personagem_escolhido = selecao_personagem()
                
                if personagem_escolhido is not None:
                    floor_1, floor_2, y_floor_1, x_floor_1 = generate_phase_5(window)
                    som_menu.stop()
                    window_end, win = run_phase_5(keyboard, mouse, window, floor_1, floor_2, y_floor_1, x_floor_1, personagem_escolhido)
                    if window_end:
                        som_menu.play()
                        if win:
                            fase5_completa = True
                            fim_fase(fase5_completa)
                        else:
                            while True:
                                fundo_fases.draw()
                                sair.draw()    
                                window.draw_text("VOCÊ PERDEU!", 420, window.height/2.5, size=28, color=(255, 255, 255))
            
                                if mouse.is_over_object(sair) and mouse.is_button_pressed(1):
                                    mouse.set_position(window.width/2, window.height/1.5)
                                    break

                                window.update()

            
            elif mouse.is_over_object(fase5_block) and mouse.is_button_pressed(1):
                window.draw_text("Complete as 4 fases anteriores para desbloquear", (window.width/2)-160, window.height/1.5, size=20, color=(255, 255, 255))

            elif mouse.is_over_object(voltar) and mouse.is_button_pressed(1):
                mouse.set_position(window.width/2, window.height/1.2)
                break

            window.update()

    if mouse.is_over_object(historia) and mouse.is_button_pressed(1):
        mostrar_historia()

    elif mouse.is_over_object(sair) and mouse.is_button_pressed(1):
        break

    window.update()