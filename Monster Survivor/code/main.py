from settings import * 
from player import * 

class Game:
    def __init__(self):
        pygame.init()
        self.display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.title = pygame.display.set_caption('Monster Survivor')
        self.running = True 
        self.clock = pygame.time.Clock()
        self.player = Player(all_sprites, (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

    def run(self):
        while self.running:
            dt = self.clock.tick() / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.display.fill('gray')
            
            all_sprites.update(dt)
            all_sprites.draw(self.display)
            
            pygame.display.update()
        pygame.quit()

all_sprites = pygame.sprite.Group()

if __name__ == '__main__':
    Game().run()





