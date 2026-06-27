import pygame
import sys
from code.Const import LARGURA, ALTURA, BRANCO, MENU, JOGANDO, VITORIA, DERROTA
from code.Menu import Menu
from code.Player import Player
from code.Enemy import Enemy


class Game:
    def __init__(self):
        pygame.init()
        self.tela = pygame.display.set_mode((LARGURA, ALTURA))
        pygame.display.set_caption("VoidBound")
        self.clock = pygame.time.Clock()

        # Carrega e ajusta o fundo usando caminho relativo obrigatório
        fundo_original = pygame.image.load("assets/MenuBg.png").convert()
        self.fundo = pygame.transform.scale(fundo_original, (LARGURA, ALTURA))

        self.estado_atual = MENU
        self.menu_gerenciador = Menu(self.tela)
        self.player = Player()
        self.enemy = Enemy()

        self.pontos_vitoria = 5
        self.pontos_atuais = 0

    def reiniciar_jogo(self):
        self.player = Player()
        self.enemy = Enemy()
        self.pontos_atuais = 0
        self.estado_atual = JOGANDO

    def executar(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if self.estado_atual == MENU and event.key == pygame.K_SPACE:
                        self.reiniciar_jogo()
                    elif self.estado_atual in [VITORIA, DERROTA]:
                        if event.key == pygame.K_r:
                            self.reiniciar_jogo()
                        if event.key == pygame.K_m:
                            self.estado_atual = MENU

            if self.estado_atual == JOGANDO:
                self.player.mover()
                self.enemy.mover()

                if self.enemy.x < -40:
                    self.enemy.reiniciar()
                    self.pontos_atuais += 1
                    if self.pontos_atuais >= self.pontos_vitoria:
                        self.estado_atual = VITORIA

                if self.player.rect.colliderect(self.enemy.rect):
                    self.estado_atual = DERROTA

            # RENDERIZAÇÃO: Desenha o fundo em vez do preenchimento preto puro
            self.tela.blit(self.fundo, (0, 0))

            if self.estado_atual == MENU:
                self.menu_gerenciador.desenhar_menu()
            elif self.estado_atual == JOGANDO:
                self.player.desenhar(self.tela)
                self.enemy.desenhar(self.tela)

                fonte = pygame.font.SysFont("Arial", 25)
                texto_pontos = fonte.render(f"Score: {self.pontos_atuais} / {self.pontos_vitoria}", True, BRANCO)
                self.tela.blit(texto_pontos, (20, 20))
            elif self.estado_atual == VITORIA:
                self.menu_gerenciador.desenhar_vitoria()
            elif self.estado_atual == DERROTA:
                self.menu_gerenciador.desenhar_derrota()

            pygame.display.flip()
            self.clock.tick(60)