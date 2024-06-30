from settings import * 

class Player(pygame.sprite.Sprite):
    def __init__(self, group, pos, collision_sprites):
        super().__init__(group)
        self.image = pygame.image.load('../images/player/down/0.png').convert_alpha()
        self.rect = self.image.get_frect(center=pos)
        self.hitbox_rect = self.rect.inflate(-60, -90)

        self.direction = pygame.math.Vector2()
        self.speed = 400
        self.collision_sprites = collision_sprites

    def input(self):
        pressed_button = pygame.key.get_pressed()
        self.direction.x = pressed_button[pygame.K_RIGHT] - pressed_button[pygame.K_LEFT]
        self.direction.y = pressed_button[pygame.K_DOWN] - pressed_button[pygame.K_UP]
        self.direction = self.direction.normalize() if self.direction else self.direction

    def move(self, dt):
        self.hitbox_rect.x += self.speed * dt * self.direction.x
        self.collision('horizontal')
        self.hitbox_rect.y += self.speed * dt * self.direction.y
        self.collision('vertical')
        self.rect.center = self.hitbox_rect.center

    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if direction == 'horizontal':
                    if self.direction.x > 0: self.hitbox_rect.right = sprite.rect.left
                    if self.direction.x < 0: self.hitbox_rect.left = sprite.rect.right
                else:
                    if self.direction.y > 0: self.hitbox_rect.bottom = sprite.rect.top 
                    if self.direction.y < 0: self.hitbox_rect.top = sprite.rect.bottom

    def update(self, dt):
        self.input()
        self.move(dt)
        
    