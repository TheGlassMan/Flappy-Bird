import pygame
from sys import exit
import random

pygame.init()
clock = pygame.time.Clock()
#Window Settings
win_height = 720
win_width = 551
window = pygame.display.set_mode((win_width, win_height))

#Images
cat_image = pygame.image.load('assets/cat.png')
bg_image = pygame.image.load('assets/background.png')
ground_image = pygame.image.load('assets/ground.png')
bottom_pipe_image = pygame.image.load('assets/pipe_bottom.png')
top_pipe_image = pygame.image.load('assets/pipe_top.png')
start_image = pygame.image.load('assets/start.png')
game_over_image = pygame.image.load('assets/game_over.png')

#Game Variables
scroll_speed = 1
cat_start_position = (100,250)
score = 0
font = pygame.font.SysFont('Segoe', 26)
game_stopped = True

class Cat(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = cat_image
        self.rect = self.image.get_rect()
        self.rect.center = cat_start_position
        self.vel = 0
        self.flap = False
        self.alive = True
    def update(self,user_input):
        self.vel += 0.5
        if self.vel > 7:
            self.vel = 7
        if self.rect.y < 500:
            self.rect.y += int(self.vel)
        if self.vel == 0:
            self.flap = False
        
        #Rotate Cat
        #self.image = pygame.transform.rotate(self.image, self.vel * -1)
        
        if user_input[pygame.K_SPACE] and not self.flap and self.rect.y > 0 and self.alive:
            self.flap = True
            self.vel = -7


class Pipe(pygame.sprite.Sprite):
    def __init__(self,x,y,image, pipe_type):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x,y
        self.enter, self.exit, self.passed = False, False, False
        self.pipe_type = pipe_type
    
    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.x <= -win_width:
            self.kill()
        
        global score
        if self.pipe_type == 'bottom':
            if cat_start_position[0] > self.rect.topleft[0] and not self.passed:
                self.enter = True
            if cat_start_position[0] > self.rect.topright[0] and not self.passed:
                self.exit = True
            if self.enter and self.exit and not self.passed:
                self.passed = True
                score += 1




class Ground(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = ground_image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x,y
    
    def update(self):
        #Move Ground
        self.rect.x -= scroll_speed
        if self.rect.x <= -win_width:
            self.kill()

def quit_game():
    #Exit Game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

def main():
    global score
    #Init Cat
    cat = pygame.sprite.GroupSingle()
    cat.add(Cat())
    #Set Pipes
    pipe_timer = 0
    pipes = pygame.sprite.Group()

    #Init Ground
    x_pos_ground, y_pos_ground = 0, 520
    ground = pygame.sprite.Group()
    ground.add(Ground(x_pos_ground, y_pos_ground))
    run = True
    while run:
        quit_game()
        window.fill((0,0,0))

        user_input = pygame.key.get_pressed()

        #Draw bg
        window.blit(bg_image, (0,0))

        #Spawn Ground
        if len(ground) <= 2:
            ground.add(Ground(win_width, y_pos_ground))


        #Draw Pipes, Ground, Cat
        
        pipes.draw(window)
        ground.draw(window)
        cat.draw(window)

        #Score
        score_text = font.render('Score: ' + str(score), True, pygame.Color(255,255,255))
        window.blit(score_text, (20,20))

        #Update Pipes, Ground, Cat
        if cat.sprite.alive:
            pipes.update()
            ground.update()
            cat.update(user_input)
        
        #Collision
        collision_pipes = pygame.sprite.spritecollide(cat.sprites()[0], pipes, False)
        collision_ground = pygame.sprite.spritecollide(cat.sprites()[0], ground, False)
        if collision_ground or collision_pipes:
            cat.sprite.alive = False
            if collision_ground or collision_pipes:
                window.blit(game_over_image, (win_width // 2 - game_over_image.get_width() // 2,
                                              win_height // 2 - game_over_image.get_height() // 2))
                if user_input[pygame.K_r]:
                    score = 0
                    main()
                    break

        #Spawn pipes
        if pipe_timer <= 0 and cat.sprite.alive:
            x_top, x_bottom = 550, 550
            y_top = random.randint(-600, -480)
            y_bottom = y_top + random.randint(90,130) + bottom_pipe_image.get_height()
            pipes.add(Pipe(x_top,y_top,top_pipe_image, 'top'))
            pipes.add(Pipe(x_bottom,y_bottom,bottom_pipe_image, 'bottom'))
            pipe_timer = random.randint(180,250)
        pipe_timer -= 1  

        clock.tick(60)
        pygame.display.update()

def menu():
    global game_stopped
    while game_stopped:
        quit_game()
        window.fill((0,0,0))
        window.blit(bg_image, (0,0))
        window.blit(ground_image,Ground(0,520))
        window.blit(cat_image, (100,250))
        window.blit(start_image, (win_width // 2 - start_image.get_width() // 2,
                                              win_height // 2 - start_image.get_height() // 2))
         
        user_input = pygame.key.get_pressed()
        if user_input[pygame.K_SPACE]:
            main()

        pygame.display.update()
menu()
