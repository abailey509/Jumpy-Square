#Andrew Bailey
#CS246

import pygame
from random import randrange

pygame.init()

#Screen parameters
window_width = 1200
window_height = 600
window = pygame.display.set_mode((window_width,window_height))
window_rect = pygame.Surface.get_rect(window)
window_center = window_rect.center

#Other setups
pygame.display.set_caption("Jumpy Square")
fps = pygame.time.Clock()

purp = (90,0,170)
grey = (40,40,40)
red = (255,0,0)

#Game setup
closed = False
game_started = False
died = False
score = 0

#Text initialization
font1 = pygame.sysfont.SysFont("Comic Sans",50)
start_text = font1.render("Press space to start...",True,purp)
start_text_size = start_text.get_rect()
#Score 
font2 = pygame.sysfont.SysFont("Arial",30)
score_text = font2.render("Score:",True,purp)
score_text_size = score_text.get_rect()
scoreNumber_text = font2.render(str(score),True,purp)
scoreNumber_text_size = scoreNumber_text.get_rect()
#Game over 
gameOver_text = font1.render("GAME OVER",True,purp)
gameOver_text_size = gameOver_text.get_rect()


#Music
pygame.mixer.music.load("music/Danse-macabre.mp3")
pygame.mixer.music.play()

gravity = 0.34
player = pygame.Rect(80,420,40,40)
player_gravity = 0
floor = pygame.Rect(0,500,window_width,10)

#Walls
generate_time = 0
generate_range = 200
movement_speed = 3
gapSize = 300
walls = []
class Wall:
    def __init__(self,sort : int,which : int = 0,wall3_height : int = 80):
        #2 walls at once
        if sort == 2:
            if which == 0:
                self.rect = pygame.Rect(window_width,500-wall3_height,15,wall3_height)
            elif which == 1:
                self.rect = pygame.Rect(window_width,0,15,500-(wall3_height+gapSize))
        #Stalagmites
        elif sort == 1:
            height = randrange(50,100,10)
            self.rect = pygame.Rect(window_width,0,15,500-height)
        #Stalagtites
        elif sort == 0:
            height = randrange(80,180,10)
            self.rect = pygame.Rect(window_width,500-height,15,height)
    def draw(self):
        pygame.draw.rect(window,purp,self.rect)
    def move(self):
        self.rect.x -= movement_speed

#Game loop
while not closed:
    fps.tick(60)
    window.fill(grey)
    keys = pygame.key.get_pressed()

    if not game_started:
        window.blit(start_text,(window_center[0]-start_text_size.width//2,window_center[1]-start_text_size.height//2))
        if keys[pygame.K_SPACE]:
            game_started = True

    elif game_started:
        score += 0.2

        #Draw figures
        pygame.draw.rect(window,purp,floor)
        pygame.draw.rect(window,red,player)
        window.blit(score_text, (10, 10))
        scoreNumber_text = font2.render(str(int(score)), True, purp)
        window.blit(scoreNumber_text, (95, 10))

        #enable gravity
        player_gravity += gravity
        player.y += int(player_gravity)
        if player.colliderect(floor):
            if keys[pygame.K_DOWN]:
                player_gravity = -5
            else:
                player_gravity = -8
        else:
            if keys[pygame.K_DOWN]:
                player_gravity += 0.6

        #Generate walls 
        if 300 < score < 601:
            movement_speed = 4
            generate_range = 180
            gapSize = 290
        elif 600 < score < 901:
            movement_speed = 5
            generate_range = 160
            gapSize = 280
        elif 900 < score < 1201:
            movement_speed = 7
            generate_range = 120
            gapSize = 260
        elif 1200 < score < 1501:
            movement_speed = 9
            generate_range = 80
            gapSize = 240
        elif 1500 < score < 1801:
            movement_speed = 11
            generate_range = 60
            gapSize = 220
        elif 1800 < score:
            movement_speed = 12
            generate_range = 55
            gapSize = 210
            
        generate_time += 1
        if generate_time >= generate_range:
            generate_time = 0
            which_wall = randrange(0,3)
            if which_wall == 2:
                #Dual wall generator
                w3 = randrange(80, 180, 10)
                for tb in range(2):
                    new_wall = Wall(2,tb,w3)
                    walls.append(new_wall)
            else:
                new_wall = Wall(which_wall)
                walls.append(new_wall)

        #revive wall clones
        for wall in walls:
            wall.draw()
            wall.move()
            if player.colliderect(wall):
                died = True
                closed = True

    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            closed = True
        if game_started:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if player.y > 370:
                        player_gravity -= 8

closed = False
#Game over screen
if died:
    while not closed:
        window.fill(grey)
        window.blit(gameOver_text,((window_center[0]-gameOver_text_size.width//2),(window_center[1]-gameOver_text_size.height//2)-50))
        window.blit(score_text,((window_center[0]-score_text_size.width//2)-80,(window_center[1]-score_text_size.height//2)+30))
        window.blit(scoreNumber_text,((window_center[0]-scoreNumber_text_size.width//2)+0,(window_center[1]-scoreNumber_text_size.height//2)+30))

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                closed = True

#Close program
pygame.quit()
quit()
