from settings import * 
from player import Player
from sprites import * 
from random import randint, choice 
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
        self.enemy_sprites = pygame.sprite.Group()
        
        self.can_shoot = True 
        self.shoot_time = 0 
        self.gun_cooldown = 100

        self.enemy_event = pygame.event.custom_type()
        pygame.time.set_timer(self.enemy_event, 300)
        self.spawn_positions = []
        self.load_images()
        self.setup()
        
    def load_images(self):
        self.bullet_surf = pygame.image.load('../images/gun/bullet.png').convert_alpha()

        folders = list(walk('../images/enemies'))[0][1]
        self.enemy_frames = {}
        for folder in folders:
            for folder_path, _, file_names in walk(f'../images/enemies/{folder}'):
                self.enemy_frames[folder] = []
                for file_name in sorted(file_names, key = lambda name: int(name.split('.')[0])):
                    full_path = f"{folder_path}/{file_name}"
                    surf = pygame.image.load(full_path).convert_alpha()
                    self.enemy_frames[folder].append(surf)

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
            if obj.name == 'Enemy':
                self.spawn_positions.append((obj.x, obj.y))
    
    def player_collision(self):
        if pygame.sprite.spritecollide(self.player, self.enemy_sprites, False, pygame.sprite.collide_mask):
            self.running = False

    def bullet_collision(self):
        if self.bullet_sprites:
            for bullet in self.bullet_sprites:
                collision_sprites = pygame.sprite.spritecollide(bullet, self.enemy_sprites, False, pygame.sprite.collide_mask)
                if collision_sprites:
                    for sprite in collision_sprites:
                        sprite.destroy()
                    bullet.kill()

    def run(self):
        while self.running:
            dt = self.clock.tick() / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == self.enemy_event:
                    Enemy(choice(self.spawn_positions), choice(list(self.enemy_frames.values())), (self.all_sprites, self.enemy_sprites), self.player, self.collision_sprites)

            self.display.fill('black')
            
            self.gun_timer()
            self.input()
            self.all_sprites.update(dt)
            self.bullet_collision()
            self.player_collision()
            self.all_sprites.draw(self.player.rect.center)
            
            pygame.display.update()
        pygame.quit()

if __name__ == '__main__':
    Game().run()





