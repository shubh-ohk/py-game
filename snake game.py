import pygame
import random
import os

pygame.mixer.init()

pygame.init()



screen_width = 900
screen_height = 600
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
org = (255,165,0)
bgimg = pygame.image.load("gree.jpg")
bgimg = pygame.transform.scale(bgimg, (screen_width , screen_height))

bimg = pygame.image.load("op.jpg")
bimg = pygame.transform.scale(bimg, (screen_width , screen_height))


gameWindow = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Snake game")
pygame.display.update()


clock = pygame.time.Clock()
font = pygame.font.SysFont(None,55)
def text_screen(text,color,x,y):
    screen_text = font.render(text,True,color)
    gameWindow.blit(screen_text,[x,y])

def plot_snake(gameWindow, color, snk_list, snake_size):
    for x,y in snk_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])

def welcome():
    exit_game = False
    while not exit_game:
        gameWindow.fill((233,210,229))
        text_screen("Welcome to Snakes", black, 260, 250)
        text_screen("Press Space Bar To Play", black, 232, 290)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    #pygame.mixer.music.load('Bg.mp3')
                    #pygame.mixer.music.play()
                    game_loop()

        pygame.display.update()
        clock.tick(49)

def game_loop():
    exit_game = False
    game_over = False
    score = 0
    snake_x = 45
    snake_y = 55
    snake_size = 12
    velocity_x = 0
    velocity_y = 0
    init_velocity = 5
    fps = 49
    food_x = random.randint(20, screen_width / 2)  # so that food lie inside perimeter
    food_y = random.randint(20, screen_height / 2)
    snk_list = []
    snk_length = 1
    # Check if hiscore file exists
    if (not os.path.exists("highscore.txt")):
        with open("highscore.txt.txt", "w") as f:
            f.write("0")
    with open("highscore.txt","r") as f:
        highscore = f.read()
    while not exit_game:
        if game_over:
            with open("highscore.txt","w") as f:
                f.write(str(highscore))
            gameWindow.fill(white)
            gameWindow.blit(bimg, (0, 0))
            text_screen("Game Over! Press enter to continue ",org,140, 290)
            text_screen("Score: "+ str(score), org, 300, 330)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        if velocity_x >= 0:
                            velocity_x = init_velocity
                            velocity_y = 0

                    if event.key == pygame.K_LEFT:
                        if velocity_x <=0:
                            velocity_x = -init_velocity
                            velocity_y = 0
                    if event.key == pygame.K_UP:
                        if velocity_y <= 0:
                            velocity_y = - init_velocity
                            velocity_x = 0
                    if event.key == pygame.K_DOWN:
                        if velocity_y >= 0:
                            velocity_y = init_velocity
                            velocity_x = 0

            snake_x = snake_x+ velocity_x
            snake_y = snake_y+ velocity_y
            if abs(snake_x - food_x) < 8 and abs(snake_y - food_y) < 8:      #this for eating the food
                score += 10
                food_x = random.randint(20, screen_width / 2)
                food_y = random.randint(20, screen_height / 2)
                snk_length += 3
                if score>int(highscore):
                    highscore= score

            gameWindow.fill(white)
            gameWindow.blit(bgimg, (0, 0))
            text_screen("Score: " + str(score)+ "                                    High Score: "+str(highscore), red, 5, 5)
            pygame.draw.rect(gameWindow, red, [food_x, food_y, snake_size, snake_size])

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            if len(snk_list) > snk_length:
                del snk_list[0]

            if head in snk_list[:-1]:
                game_over= True
                #pygame.mixer.music.load('Game Over.mp3')
                #pygame.mixer.music.play()

            if snake_x<0 or snake_y<0 or snake_x>screen_width or snake_y>screen_height:
                game_over = True
                #pygame.mixer.music.load('Game Over.mp3')
                #pygame.mixer.music.play()

            plot_snake(gameWindow, black, snk_list, snake_size)
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()

welcome()

