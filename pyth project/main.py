import pygame
import random
import os

pygame.mixer.init()
pygame.init()

# colours
white = (255, 255, 255)
black = (0, 0, 0)
green = (50, 70, 50)
red = (200, 0, 0)
yellow = (200, 200, 0)

# screen window
screen_width = 700
screen_height = 500
gameWindow = pygame.display.set_mode((screen_width, screen_height))

bgimg = pygame.image.load('snake.jpg.png')
bgimg = pygame.transform.scale(bgimg, (screen_width, screen_height)).convert_alpha()

# to display title
pygame.display.set_caption("Snakes With Ashii...")
# to update any changes
pygame.display.update()

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 45)


def text_in_screen(text, colour, x, y):
    screen_text = font.render(text, True, colour)
    gameWindow.blit(screen_text, [x, y])


def plot_snake(gameWindow, colour, snk_lst, snake_size):
    for x, y in snk_lst:
        pygame.draw.rect(gameWindow, colour, [x, y, snake_size, snake_size])


def welcome():
    exit_game = False
    while not exit_game:
        gameWindow.fill((233, 220, 70))
        text_in_screen("Welcome To The Game", black, 190, 180)
        text_in_screen("Press SPACEBAR to start", red, 170, 240)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.load('bgmusic.mp3')
                    pygame.mixer.music.play()
                    gameLoop()

        clock.tick(40)
        pygame.display.update()

    pygame.quit()
    quit()


def gameLoop():
    # game specific variables
    init_velocity = 7
    exitGame = False
    gameOver = False
    snake_size = 20
    snake_x = 110
    snake_y = 100
    velocity_x = 0
    velocity_y = 0
    fps = 30
    score = 0
    snk_lst = []
    snk_length = 1
    # check if file exists
    if not os.path.exists("hiscore.txt"):
        with open("hiscore.txt", "w") as f:
            f.write("0")
    with open("hiscore.txt", "r") as f:
        hiscore = f.read()

    food_x = random.randint(50, screen_width - 50)
    food_y = random.randint(50, screen_height - 50)

    while not exitGame:
        if gameOver:
            with open("hiscore.txt", "w") as f:
                f.write(str(hiscore))

            gameWindow.fill(white)
            text_in_screen("GAME OVER! Press ENTER to continue", red, 80, 200)
            text_in_screen("Your HighScore is " + str(score), black, 200, 250)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exitGame = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        pygame.mixer.music.load('beep.mp3')
                        pygame.mixer.music.play()
                        welcome()

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exitGame = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_LEFT:
                        velocity_x = -init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_UP:
                        velocity_y = -init_velocity
                        velocity_x = 0
                    if event.key == pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0

                    if event.key == pygame.K_m:
                        score += 20

                    # if event.key == pygame.K_p:

            snake_x = snake_x + velocity_x
            snake_y = snake_y + velocity_y

            if abs(snake_x - food_x) < 6 and abs(snake_y - food_y) < 6:
                score += 10
                food_x = random.randint(50, screen_width - 50)
                food_y = random.randint(50, screen_height - 50)
                snk_length += 5

                if score > int(hiscore):
                    hiscore = score

            gameWindow.fill(green)
            gameWindow.blit(bgimg, (0, 0))
            text_in_screen("Score = " + str(score) + "  HighScore = " + str(hiscore), yellow, 10, 10)
            plot_snake(gameWindow, white, snk_lst, snake_size)
            pygame.draw.rect(gameWindow, red, [food_x, food_y, snake_size, snake_size])

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_lst.append(head)

            if len(snk_lst) > snk_length:
                del snk_lst[0]

            if snake_x < 0 or snake_x > screen_width or snake_y < 0 or snake_y > screen_height:
                gameOver = True
                pygame.mixer.music.load('gameOver.mp3')
                pygame.mixer.music.play()

            if head in snk_lst[:-1]:
                gameOver = True
                pygame.mixer.music.load('gameOver.mp3')
                pygame.mixer.music.play()

        clock.tick(fps)
        pygame.display.update()

    print("Your score is ", score)
    pygame.quit()
    quit()


pygame.mixer.music.load('beep.mp3')
pygame.mixer.music.play()
welcome()
