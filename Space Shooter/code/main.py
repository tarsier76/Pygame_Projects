import pygame 
from random import randint
class Player(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = pygame.image.load('../images/player.png').convert_alpha()
        self.rect = self.image.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.direction = pygame.math.Vector2()
        self.speed = 300
        
        self.can_shoot = True 
        self.laser_shoot_time = 0
        self.cooldown_duration = 400 

    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if self.laser_shoot_time + self.cooldown_duration <= current_time:
                self.can_shoot = True 

    def update(self, delta):
        keys = pygame.key.get_pressed()

        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * delta * self.speed

        key = pygame.key.get_just_pressed()
        if key[pygame.K_SPACE] and self.can_shoot:
            Laser(laser_surf, self.rect.midtop, all_sprites)
            self.can_shoot = False 
            self.laser_shoot_time = pygame.time.get_ticks()

        self.laser_timer()
class Star(pygame.sprite.Sprite):
    def __init__(self, group, surf):
        super().__init__(group)
        self.width = 1280
        self.height = 720
        self.image = surf 
        self.rect = self.image.get_frect(center=(randint(0, self.width), randint(0, self.height)))
class Laser(pygame.sprite.Sprite):
    def __init__(self, surf, pos, group):
        super().__init__(group)
        self.image = surf
        self.rect = self.image.get_frect(midbottom=pos)

    def update(self, dt):
        self.rect.centery -= 400 * dt 
        if self.rect.bottom < 0:
            self.kill()
class Meteor(pygame.sprite.Sprite):
    def __init__(self, surf, pos, group):
        super().__init__(group)
        self.image = surf 
        self.rect = self.image.get_frect(center=pos)
        
    def update(self, dt):
        self.rect.centery += 400 * dt 

pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Space Shooter')
running = True 
clock = pygame.time.Clock()

star_surface = pygame.image.load('../images/star.png').convert_alpha()
meteor_surf = pygame.image.load('../images/meteor.png').convert_alpha()
laser_surf = pygame.image.load('../images/laser.png').convert_alpha() 

all_sprites = pygame.sprite.Group()
for time in range(20):
    Star(all_sprites, star_surface)
player = Player(all_sprites)

meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 100)

while running:
    dt = clock.tick() / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 
        if event.type == meteor_event:
            x, y = randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)
            Meteor(meteor_surf, (x,y), all_sprites)
            
    display_surface.fill(color='darkgray')

    all_sprites.update(dt)
    all_sprites.draw(display_surface)
    
    pygame.display.update()

pygame.quit()