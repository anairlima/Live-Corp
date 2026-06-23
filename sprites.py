from PPlay.sprite import *
from PPlay.window import *

'''SPRITE DOS MENUS'''
#janela
janela = Window(1000,700)
janela.set_background_color((0,0,0))


#botao historia
historia = Sprite("images/menu/menu_historia.png", 1)
historia.x = janela.width/2 - historia.width/2
historia.y = (janela.height/2 - historia.height)

#botao jogar
jogar = Sprite("images/menu/menu_jogar.png", 1) #300x100
jogar.x = janela.width/2 - jogar.width/2
jogar.y = janela.height/2 + 40

#botao fase1 
fase1 = Sprite("images/menu/menu_phase_1.png", 1) 
fase1.x = janela.width/2 - jogar.width/2
fase1.y = (janela.height/2) - 120

# botao fase 2
fase2 = Sprite("images/menu/menu_phase_2.png", 1) 
fase2.x = janela.width/2 - jogar.width/2
fase2.y = janela.height/2 - 80

# botao fase 3
fase3 = Sprite("images/menu/menu_phase_3.png", 1) 
fase3.x = janela.width/2 - jogar.width/2
fase3.y = janela.height/2 - 40

# botao fase 4
fase4 = Sprite("images/menu/menu_phase_4.png", 1) 
fase4.x = janela.width/2 - jogar.width/2
fase4.y = janela.height/2

# botao fase 5
fase5 = Sprite("images/menu/menu_phase_5.png", 1)
fase5.x = janela.width/2 - jogar.width/2
fase5.y = janela.height/2 + 40

# botao fase 5 block
fase5_block = Sprite("images/menu/menu_phase_5_block.png", 1)
fase5_block.x = janela.width/2 - jogar.width/2
fase5_block.y = janela.height/2 + 40

#fundo menu fases
fundo_fases = Sprite("images/menu/menu_fundo.png", 1)

#botao sair
sair = Sprite("images/menu/sair.png", 1)
sair.x = janela.width/2 - sair.width/2
sair.y = janela.height/1.5

#botao voltar
voltar = Sprite("images/menu/voltar.png", 1)
voltar.x = janela.width/2 - voltar.width/2
voltar.y = janela.height/1.5 + 150