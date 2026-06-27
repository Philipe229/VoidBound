import pygame
import sys
from code.Const import LARGURA, ALTURA, PRETO, BRANCO, MENU, JOGANDO, FASE2, VITORIA, DERROTA
from code.Menu import Menu
from code.Player import Player
from code.Enemy import Enemy


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()  # Inicializa o sistema de áudio
        pygame.mixer.set_num_channels(32)

        self.tela = pygame.display.set_mode((LARGURA, ALTURA))
        pygame.display.set_caption("VoidBound")
        self.clock = pygame.time.Clock()

        try:
            # Carrega o fundo do jogo
            fundo_original = pygame.image.load("assets/MenuBg.png").convert()
            self.fundo = pygame.transform.scale(fundo_original, (LARGURA, ALTURA))
            self.usa_fundo = True
        except pygame.error:
            self.usa_fundo = False

        self.fundo_x = 0
        self.velocidade_fundo = 3  # Velocidade do movimento do cenário

        # Carrega o áudio de efeito de explosão/ponto
        try:
            self.som_score = pygame.mixer.Sound("Music/Score.mp3")
        except pygame.error:
            self.som_score = None

        self.estado_atual = MENU
        self.menu_gerenciador = Menu(self.tela)

        # Começa com a música do Menu Inicial
        self.tocar_musica_fundo("Music/MenuVoid.wav")

        # Carrega o som do tiro
        try:
            self.som_tiro = pygame.mixer.Sound("Music/tironave.wav")
        except pygame.error:
            self.som_tiro = None

    def tocar_musica_fundo(self, caminho):
        try:
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
            pygame.mixer.music.load(caminho)
            pygame.mixer.music.play(-1)
        except pygame.error:
            pass

    def reiniciar_jogo(self):
        pygame.mixer.stop()  # Limpa canais de efeitos

        self.player = Player()
        self.inimigos = [Enemy() for _ in range(4)]
        self.tiros = []

        self.pontos_vitoria = 15
        self.pontos_atuais = 0
        self.fundo_x = 0  # Reseta a posição do cenário
        self.estado_atual = JOGANDO

        self.tocar_musica_fundo("Music/Level1.wav")

    def executar(self):
        while True:
            # 1. CAPTURA DE EVENTOS
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    print(f"Tecla: {pygame.key.name(event.key)} | Estado: {self.estado_atual}")

                    if self.estado_atual == MENU and event.key == pygame.K_SPACE:
                        print("-> Iniciando o jogo (Fase 1)...")
                        self.reiniciar_jogo()
                    elif self.estado_atual in [JOGANDO, FASE2] and event.key == pygame.K_SPACE:
                        self.tiros.append(self.player.atirar())
                        if self.som_tiro:
                            self.som_tiro.stop()
                            self.som_tiro.play()
                    elif self.estado_atual in [VITORIA, DERROTA]:
                        if event.key == pygame.K_r:
                            self.reiniciar_jogo()
                        if event.key == pygame.K_m:
                            pygame.mixer.music.stop()
                            pygame.mixer.music.unload()
                            self.estado_atual = MENU
                            self.tocar_musica_fundo("Music/MenuVoid.wav")

            # 2. LÓGICA DA GAMEPLAY (Funciona tanto na Fase 1 quanto na Fase 2)
            if self.estado_atual in [JOGANDO, FASE2]:
                # Movimento do Fundo Infinito (Fica mais rápido na Fase 2!)
                if self.usa_fundo:
                    if self.estado_atual == FASE2:
                        self.fundo_x -= (self.velocidade_fundo + 2)  # Cenário corre mais rápido!
                    else:
                        self.fundo_x -= self.velocidade_fundo

                    if self.fundo_x <= -LARGURA:
                        self.fundo_x = 0

                # Mover o jogador
                self.player.mover()

                # Mover os tiros
                for tiro in self.tiros[:]:
                    tiro.mover()
                    if tiro.x > LARGURA:
                        self.tiros.remove(tiro)

                # Controlar os Inimigos e Colisões
                for enemy in self.inimigos:
                    enemy.mover()

                    if enemy.x < -40:
                        enemy.reiniciar()

                    # Colisão Inimigo x Jogador (Game Over)
                    if self.player.rect.colliderect(enemy.rect):
                        print("-> Game Over!")
                        pygame.mixer.stop()
                        pygame.mixer.music.stop()
                        pygame.mixer.music.unload()
                        self.estado_atual = DERROTA
                        self.tocar_musica_fundo("Music/MenuVoid.wav")

                    # Colisão Tiro x Inimigo
                    for tiro in self.tiros[:]:
                        if tiro.rect.colliderect(enemy.rect):
                            if tiro in self.tiros:
                                self.tiros.remove(tiro)
                            enemy.reiniciar()
                            self.pontos_atuais += 1

                            if self.som_score:
                                self.som_score.play()

                            # --- SISTEMA DE TRANSIÇÃO DE FASES ---
                            # Se chegou a 15 abates e estava na Fase 1, passa para a Fase 2
                            if self.estado_atual == JOGANDO and self.pontos_atuais >= 15:
                                print("-> Transição: Indo para a FASE 2!")
                                self.estado_atual = FASE2
                                self.tiros = []  # Limpa os tiros da tela
                                # Reseta a posição de todos os inimigos para virem de novo
                                for e in self.inimigos:
                                    e.reiniciar()
                                # Troca a música de fundo para a da Fase 2
                                self.tocar_musica_fundo("Music/Level2.mp3")

                                # Se chegou a 30 abates (15 da primeira + 15 da segunda), Tela de Vitória!
                            elif self.estado_atual == FASE2 and self.pontos_atuais >= 30:
                                print("-> Vitória Final Conquistada!")
                                pygame.mixer.stop()
                                pygame.mixer.music.stop()
                                pygame.mixer.music.unload()
                                self.estado_atual = VITORIA
                                self.tocar_musica_fundo("Music/MenuVoid.wav")

            # 3. RENDERIZAÇÃO
            if self.usa_fundo:
                if self.estado_atual in [JOGANDO, FASE2]:
                    self.tela.blit(self.fundo, (self.fundo_x, 0))
                    self.tela.blit(self.fundo, (self.fundo_x + LARGURA, 0))
                else:
                    self.tela.blit(self.fundo, (0, 0))
            else:
                self.tela.fill(PRETO)

            # Desenho das Camadas superiores
            if self.estado_atual == MENU:
                self.menu_gerenciador.desenhar_menu()
            elif self.estado_atual in [JOGANDO, FASE2]:
                self.player.desenhar(self.tela)
                for enemy in self.inimigos:
                    enemy.desenhar(self.tela)
                for tiro in self.tiros:
                    tiro.desenhar(self.tela)

                # Mostra a fase atual e os pontos acumulados
                fonte = pygame.font.SysFont("Arial", 25)
                fase_nome = "Fase 1" if self.estado_atual == JOGANDO else "FASE2"
                texto_pontos = fonte.render(f"{fase_nome} | Abates: {self.pontos_atuais} / 30", True, BRANCO)
                self.tela.blit(texto_pontos, (20, 20))

            elif self.estado_atual == VITORIA:
                self.menu_gerenciador.desenhar_vitoria()
            elif self.estado_atual == DERROTA:
                self.menu_gerenciador.desenhar_derrota()

            pygame.display.flip()
            self.clock.tick(60)