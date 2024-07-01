from settings import * 
from player import Player
from sprites import * 
from random import randint 
from pytmx.util_pygame import load_pygame
from groups import AllSprites

class Game:
    def __init__(self):
        pygame.init()
        self.display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.title = pygame.display.set_caption('Monster Survivor')
        self.running = True 
        self.clock = pygame.time.Clock()
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.setup()
        self.load_images()

        self.can_shoot = True 
        self.shoot_time = 0 
        self.gun_cooldown = 600
        
    def load_images(self):
        self.bullet_surf = pygame.image.load('../images/gun/bullet.png').convert_alpha()

    def input(self):
        if pygame.mouse.get_pressed()[0] and self.can_shoot:
            pos = self.gun.rect.center + self.gun.player_direction * 50
            Bullet(self.bullet_surf, pos, self.gun.player_direction, (self.all_sprites, self.bullet_sprites))
            self.can_shoot = False 
            self.shoot_time = pygame.time.get_ticks()

    def gun_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time >= self.gun_cooldown:
                self.can_shoot = True 

    def setup(self):
        map = load_pygame('../data/maps/world.tmx')
        for x, y, image in map.get_layer_by_name('Ground').tiles():
            Sprite((x * TILE_SIZE ,y * TILE_SIZE), image, self.all_sprites)

        for obj in map.get_layer_by_name('Objects'):
            CollisionSprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))

        for obj in map.get_layer_by_name('Collisions'):
            img = pygame.Surface((obj.width, obj.height))
            img.set_colorkey('black')
            CollisionSprite((obj.x, obj.y), img, (self.all_sprites, self.collision_sprites))

        for obj in map.get_layer_by_name('Entities'):
            if obj.name == 'Player':
                self.player = Player(self.all_sprites, (obj.x, obj.y), self.collision_sprites)
                self.gun = Gun(self.player, self.all_sprites)
    
    def run(self):
        while self.running:
            dt = self.clock.tick() / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.display.fill('black')
            
            self.gun_timer()
            self.input()
            self.all_sprites.update(dt)
            self.all_sprites.draw(self.player.rect.center)
            
            pygame.display.update()
        pygame.quit()

if __name__ == '__main__':
    Game().run()





