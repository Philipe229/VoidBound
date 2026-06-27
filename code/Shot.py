import pygame


class Shot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocidade = 12  # Velocidade do laser

        # Carrega a imagem do tiro da tua pasta assets
        try:
            imagem_original = pygame.image.load("assets/Player1Shot.png").convert_alpha()
            self.image = pygame.transform.scale(imagem_original, (20, 10))
            self.usa_image = True
        except pygame.error:
            self.usa_image = False

        # Define a caixa de colisão do tiro
        self.rect = pygame.Rect(self.x, self.y, 20, 10)

    def mover(self):
        self.x += self.velocidade
        self.rect.topleft = (self.x, self.y)

    def desenhar(self, tela):
        if self.usa_image:
            tela.blit(self.image, self.rect)
        else:
            pygame.draw.rect(tela, (255, 255, 0), self.rect)  # Amarelo caso falte imagem