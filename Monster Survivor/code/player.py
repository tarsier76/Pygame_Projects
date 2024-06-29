from settings import * 

class Player(pygame.sprite.Sprite):
    def __init__(self, group, pos):
        super().__init__(group)
        self.image = pygame.image.load('../images/player/down/0.png').convert_alpha()
        self.rect = self.image.get_frect(center=pos)
        self.direction = pygame.math.Vector2()
        self.speed = 400

    def update(self, dt):
        pressed_button = pygame.key.get_pressed()

        self.direction.x = pressed_button[pygame.K_RIGHT] - pressed_button[pygame.K_LEFT]
        self.direction.y = pressed_button[pygame.K_DOWN] - pressed_button[pygame.K_UP]
        self.direction = self.direction.normalize() if self.direction else self.direction
        
        self.rect.center += self.speed * dt * self.direction