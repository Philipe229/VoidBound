import pygame
from code.Const import LARGURA, ALTURA


class Enemy:
    def __init__(self):
        self.x = LARGURA - 50
        self.y = ALTURA // 2
        self.velocidade = 7

        # Caminho relativo voltando um nível.
        imagem_original = pygame.image.load("assets/enemy1.png").convert_alpha()
        self.image = pygame.transform.scale(imagem_original, (40, 40))

        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)

    def mover(self):
        self.x -= self.velocidade
        self.rect.topleft = (self.x, self.y)

    def reiniciar(self):
        self.x = LARGURA

    def desenhar(self, tela):
        tela.blit(self.image, self.rect)