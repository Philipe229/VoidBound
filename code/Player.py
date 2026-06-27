import pygame
from code.Const import ALTURA


class Player:
    def __init__(self):
        self.x = 100
        self.y = ALTURA // 2
        self.velocidade = 5

        # Caminho relativo voltando um nível.
        imagem_original = pygame.image.load("assets/player1.png").convert_alpha()
        # Redimensiona a imagem para o tamanho da colisão (40x40)
        self.image = pygame.transform.scale(imagem_original, (40, 40))

        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)

    def mover(self):
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_UP] and self.y > 0:
            self.y -= self.velocidade
        if teclas[pygame.K_DOWN] and self.y < ALTURA - 40:
            self.y += self.velocidade

        self.rect.topleft = (self.x, self.y)

    def desenhar(self, tela):
        # Desenha a imagem na tela na posição do retângulo de colisão
        tela.blit(self.image, self.rect)