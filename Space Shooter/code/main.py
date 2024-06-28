import pygame 
from random import randint, uniform
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
            Laser(laser_surf, self.rect.midtop, (all_sprites, laser_sprites))
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
        self.original_image = surf 
        self.image = surf
        self.rect = self.image.get_frect(center=pos)
        self.delay = 3000
        self.start_time = pygame.time.get_ticks()
        self.direction = pygame.Vector2(uniform(-0.5, 0.5),1)
        self.speed = randint(400, 500)
        self.rotation_speed = randint(40, 80)
        self.rotation = 0 
        
    def update(self, dt):
        self.rect.center += self.direction * dt * self.speed
        self.rotation += self.rotation_speed * dt
        self.image = pygame.transform.rotozoom(self.original_image, self.rotation, 1)
        self.rect = self.image.get_frect(center=self.rect.center)
        if pygame.time.get_ticks() - self.start_time >= self.delay:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, group, explosions_images, pos):
        super().__init__(group)
        self.explosions = explosions_images
        self.frame_index = 0 
        self.image = self.explosions[self.frame_index]
        self.rect = self.image.get_frect(center=pos)

    def update(self, dt):
        self.frame_index += 20 * dt
        if self.frame_index < len(self.explosions):
            self.image = self.explosions[int(self.frame_index) % len(self.explosions)]
        else:
            self.kill()

def collisions():
    global running
    if pygame.sprite.spritecollide(player, meteor_sprites, True, pygame.sprite.collide_mask):
        running = False
    for laser in laser_sprites:
        if pygame.sprite.spritecollide(laser, meteor_sprites, True):
            laser.kill()
            Explosion(all_sprites, explosions_list, laser.rect.midtop)

def display_score():
    current_time = pygame.time.get_ticks() // 10
    text_surf = font.render(str(current_time), True, (240,240,240))
    text_rect = text_surf.get_frect(midbottom=(WINDOW_WIDTH / 2, WINDOW_HEIGHT - 50))
    display_surface.blit(text_surf, text_rect)
    pygame.draw.rect(display_surface, (240,240,240), text_rect.inflate(20,10).move(0,-7), 5, 10)

pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Space Shooter')
running = True 
clock = pygame.time.Clock()

star_surface = pygame.image.load('../images/star.png').convert_alpha()
meteor_surf = pygame.image.load('../images/meteor.png').convert_alpha()
laser_surf = pygame.image.load('../images/laser.png').convert_alpha() 
explosions_list = [pygame.image.load(f'../images/explosion/{number}.png').convert_alpha() for number in range(21)]
font = pygame.font.Font('../images/Oxanium-Bold.ttf', 40)


all_sprites = pygame.sprite.Group()
meteor_sprites = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()
for time in range(20):
    Star(all_sprites, star_surface)
player = Player(all_sprites)

meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 400)


while running:
    dt = clock.tick() / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 
        if event.type == meteor_event:
            x,y = randint(0, WINDOW_WIDTH), randint(-200, -100)
            Meteor(meteor_surf, (x,y), (all_sprites, meteor_sprites))

    display_surface.fill(color='#3a2e3f')

    display_score()

    all_sprites.update(dt)
    
    collisions()

    all_sprites.draw(display_surface)
    
    pygame.display.update()

pygame.quit()