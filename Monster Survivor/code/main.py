from settings import * 

class Game:
    def __init__(self):
        pygame.init()
        self.display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Monster Survivor')
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

        if not self.running:
            pygame.quit()

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

all_sprites = pygame.sprite.Group()

Game().run()





