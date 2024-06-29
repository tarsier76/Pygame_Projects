from settings import * 
from player import Player
from sprites import * 
from random import randint 

class Game:
    def __init__(self):
        pygame.init()
        self.display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.title = pygame.display.set_caption('Monster Survivor')
        self.running = True 
        self.clock = pygame.time.Clock()
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()
        self.player = Player(self.all_sprites, (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2), self.collision_sprites)

        for sprite in range(6):
            x, y = randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)
            w, h = randint(60, 100), randint(50, 100)
            CollisionSprite((x,y), (w, h), (self.all_sprites, self.collision_sprites))
        
    def run(self):
        while self.running:
            dt = self.clock.tick() / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.display.fill('black')
            
            self.all_sprites.update(dt)
            self.all_sprites.draw(self.display)
            
            pygame.display.update()
        pygame.quit()

if __name__ == '__main__':
    Game().run()





