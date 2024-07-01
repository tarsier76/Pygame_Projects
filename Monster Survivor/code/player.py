from settings import * 

class Player(pygame.sprite.Sprite):
    def __init__(self, group, pos, collision_sprites):
        super().__init__(group)
        self.load_images()
        self.state, self.frame_index = 'down', 0
        self.image = pygame.image.load('../images/player/down/0.png').convert_alpha()
        self.rect = self.image.get_frect(center=pos)
        self.hitbox_rect = self.rect.inflate(-60, -90)

        self.direction = pygame.math.Vector2()
        self.speed = 400
        self.collision_sprites = collision_sprites

    def load_images(self):
        self.frames = {'left': [], 'right': [], 'up': [], 'down': []}

        for state in self.frames.keys():
            for folder_path, sub_folders, file_names in walk(f'../images/player/{state}'):
                if file_names:
                    for file in sorted(file_names, key = lambda name: int(name.split('.')[0])):
                        full_path = folder_path + '/' + file
                        surf = pygame.image.load(full_path).convert_alpha()
                        self.frames[state].append(surf)
        

    def input(self):
        pressed_button = pygame.key.get_pressed()
        self.direction.x = int(pressed_button[pygame.K_RIGHT] or pressed_button[pygame.K_d])  - int(pressed_button[pygame.K_LEFT] or pressed_button[pygame.K_a])
        self.direction.y = int(pressed_button[pygame.K_DOWN] or pressed_button[pygame.K_s]) - int(pressed_button[pygame.K_UP] or pressed_button[pygame.K_w])
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

    def animate(self, dt):
        if self.direction.x != 0:
            self.state = 'right' if self.direction.x > 0 else 'left'
        if self.direction.y != 0:
            self.state = 'down' if self.direction.y > 0 else 'up'
        if self.direction == (0,0):
            self.frame_index = 0
        
        self.frame_index += 5 * dt
        self.image = self.frames[self.state][int(self.frame_index) % len(self.frames[self.state])]

    def update(self, dt):
        self.input()
        self.move(dt)
        self.animate(dt)
        
    