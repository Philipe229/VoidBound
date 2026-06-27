import pygame
from code.Const import LARGURA, ALTURA, AZUL, BRANCO, VERDE, VERMELHO


class Menu:
    def __init__(self, tela):
        self.tela = tela
        self.fonte_titulo = pygame.font.SysFont("Arial", 50, bold=True)
        self.fonte_texto = pygame.font.SysFont("Arial", 25)

    def desenhar_menu(self):
        # Título do jogo
        texto_titulo = self.fonte_titulo.render("VOIDBOUND", True, AZUL)
        self.tela.blit(texto_titulo, (LARGURA // 2 - texto_titulo.get_width() // 2, 100))

        # Instrução para iniciar
        texto_jogar = self.fonte_texto.render("Pressione [ ESPAÇO ] para Iniciar", True, BRANCO)
        self.tela.blit(texto_jogar, (LARGURA // 2 - texto_jogar.get_width() // 2, 250))

        # EXIGÊNCIA: Comandos de controle visíveis no menu
        texto_controles_titulo = self.fonte_texto.render("COMANDOS DE CONTROLE:", True, VERDE)
        texto_comando1 = self.fonte_texto.render("Seta para CIMA - Mover para Cima", True, BRANCO)
        texto_comando2 = self.fonte_texto.render("Seta para BAIXO - Mover para Baixo", True, BRANCO)

        self.tela.blit(texto_controles_titulo, (LARGURA // 2 - texto_controles_titulo.get_width() // 2, 400))
        self.tela.blit(texto_comando1, (LARGURA // 2 - texto_comando1.get_width() // 2, 440))
        self.tela.blit(texto_comando2, (LARGURA // 2 - texto_comando2.get_width() // 2, 470))

    def desenhar_vitoria(self):
        texto = self.fonte_titulo.render("VITÓRIA CONQUISTADA!", True, VERDE)
        self.tela.blit(texto, (LARGURA // 2 - texto.get_width() // 2, 200))
        self.desenhar_subtexto()

    def desenhar_derrota(self):
        texto = self.fonte_titulo.render("GAME OVER", True, VERMELHO)
        self.tela.blit(texto, (LARGURA // 2 - texto.get_width() // 2, 200))
        self.desenhar_subtexto()

    def desenhar_subtexto(self):
        texto_opcoes = self.fonte_texto.render("Pressione [ R ] para Reiniciar ou [ M ] para o Menu", True, BRANCO)
        self.tela.blit(texto_opcoes, (LARGURA // 2 - texto_opcoes.get_width() // 2, 350))