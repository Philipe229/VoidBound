import pygame
from code.Const import ALTURA, AZUL
from code.Shot import Shot


class Player:
    def __init__(self):
        self.x = 100
        self.y = ALTURA // 2
        self.velocidade = 6

        try:
            imagem_original = pygame.image.load("assets/Player1.png").convert_alpha()
            self.image = pygame.transform.scale(imagem_original, (50, 50))
            self.usa_imagem = True
        except pygame.error:
            self.usa_imagem = False

        self.rect = pygame.Rect(self.x, self.y, 50, 50)

    def mover(self):
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_UP] and self.y > 50:
            self.y -= self.velocidade
        if teclas[pygame.K_DOWN] and self.y < ALTURA - 90:
            self.y += self.velocidade

        self.rect.topleft = (self.x, self.y)

    def atirar(self):
        # Cria um tiro saindo da ponta direita central da nave
        return Shot(self.x + 50, self.y + 20)

    def desenhar(self, tela):
        if self.usa_imagem:
            tela.blit(self.image, self.rect)
        else:
            pygame.draw.rect(tela, AZUL, self.rect)