import pygame
import random
from code.Const import LARGURA, ALTURA, VERMELHO


class Enemy:
    def __init__(self):
        # Spawna fora da tela à direita
        self.x = LARGURA + random.randint(0, 300)
        self.y = random.randint(50, ALTURA - 90)
        self.velocidade = random.randint(4, 8)

        try:
            imagem_original = pygame.image.load("assets/Enemy1.png").convert_alpha()
            self.image = pygame.transform.scale(imagem_original, (45, 45))
            self.usa_imagem = True
        except pygame.error:
            self.usa_imagem = False

        self.rect = pygame.Rect(self.x, self.y, 45, 45)

    def mover(self):
        self.x -= self.velocidade
        self.rect.topleft = (self.x, self.y)

    # ESTE É O MÉTODO QUE ESTAVA FALTANDO:
    def reiniciar(self):
        self.x = LARGURA + random.randint(0, 200)
        self.y = random.randint(50, ALTURA - 90)
        self.velocidade = random.randint(4, 8)
        self.rect.topleft = (self.x, self.y)

    def desenhar(self, tela):
        if self.usa_imagem:
            tela.blit(self.image, self.rect)
        else:
            pygame.draw.rect(tela, VERMELHO, self.rect)