import pygame
import random
import math
import os

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Setup screen
wn = pygame.display.set_mode((470, 690))
pygame.display.set_caption('Car Gaming')
logo = pygame.image.load('block.jpg')
pygame.display.set_icon(logo)

# Scoring part
score = 0
high_score_file = "high_score.txt"

# Load high score from file
if os.path.exists(high_score_file):
    with open(high_score_file, "r") as file:
        high_score = int(file.read())
else:
    high_score = 0

font = pygame.font.Font(None, 36)

# Variable
game_exit = False
bg = pygame.image.load("bg.jpg")

# Adding main car
mainCar = pygame.image.load('car7.jpg')
mainCarImgX = 220
mainCarImgY = 480
mainCarImgXchange = 0

# Adding other cars
car_images = ['car.jpg', 'car2.jpg', 'car4.jpg', 'car5.jpg']
cars = []
for img in car_images:
    car = pygame.image.load(img)
    car_X = random.randint(0, 414)
    car_Y = random.randint(-300, -100)
    cars.append([car, car_X, car_Y, 1])

# Adding coins
coin_img = 'block.jpg'
coins = []
for _ in range(3):
    coin = pygame.image.load(coin_img)
    coin_X = random.randint(0, 414)
    coin_Y = random.randint(-300, -100)
    coins.append([coin, coin_X, coin_Y, 1])

# Function to display images
def display_image(img, x, y):
    wn.blit(img, (x, y))

# Function for collision detection
def isCollision(mainCar_x, mainCar_y, obj_x, obj_y, distance_threshold):
    distance = math.sqrt((math.pow(mainCar_x - obj_x, 2) + math.pow(mainCar_y - obj_y, 2)))
    return distance < distance_threshold

# Function to save high score to file
def save_high_score(high_score):
    with open(high_score_file, "w") as file:
        file.write(str(high_score))

# Function to play background music
def playBackground():
    try:
        pygame.mixer.music.load("bg.mp3")
        pygame.mixer.music.play(-1, 0)  # Play endlessly from the beginning
    except pygame.error as e:
        print(f"Error loading background music: {e}")

# Function to play sound effects
def playSound(sound):
    try:
        if sound == "ding":
            sound_effect = pygame.mixer.Sound("ding.mp3")
        elif sound == "crash":
            sound_effect = pygame.mixer.Sound("crash.mp3")
        pygame.mixer.Sound.play(sound_effect)
    except pygame.error as e:
        print(f"Error loading sound: {e}")

# Function to display game over screen
def showGameOver(score, high_score):
    font = pygame.font.SysFont('arial', 36)
    wn.fill((0, 0, 0))  # Clear screen with black color
    line1 = font.render(f"GAME OVER!! Score:{score}", True, (200, 200, 200))
    wn.blit(line1, (50, 200))
    line2 = font.render("To play again", True, (200, 200, 200))
    wn.blit(line2, (30, 300))
    line3 = font.render("Press Enter, else ESC", True, (200, 200, 200))
    wn.blit(line3, (30,400))
    pygame.display.flip()
    pygame.mixer.music.pause()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(1)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return True
                if event.key == pygame.K_ESCAPE:
                    return False

# Start background music
playBackground()

# Main loop
while not game_exit:
    wn.blit(bg, (0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_exit = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:    
                mainCarImgXchange = 2
            if event.key == pygame.K_LEFT:
                mainCarImgXchange = -2
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit(1)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                mainCarImgXchange = 0

    mainCarImgX += mainCarImgXchange

    # Boundaries for main car
    if mainCarImgX <= 0:
        mainCarImgX = 0
    elif mainCarImgX >= 414:    
        mainCarImgX = 414

    # Move and display other cars
    for car in cars:
        car[2] += car[3]
        display_image(car[0], car[1], car[2])
        if car[2] > 690:
            car[1] = random.randint(0, 414)
            car[2] = random.randint(-300, -100)

        if isCollision(mainCarImgX, mainCarImgY, car[1], car[2], 27):
            if score > high_score:
                high_score = score
                save_high_score(high_score)
            playSound("crash")
            if not showGameOver(score, high_score):
                game_exit = True
            else:
                score = 0
                mainCarImgX = 220
                mainCarImgY = 480
                for c in cars:
                    c[1] = random.randint(0, 414)
                    c[2] = random.randint(-300, -100)
                for c in coins:
                    c[1] = random.randint(0, 414)
                    c[2] = random.randint(-300, -100)
                pygame.mixer.music.unpause()

    # Move and display coins
    for coin in coins:
        coin[2] += coin[3]
        display_image(coin[0], coin[1], coin[2])
        if coin[2] > 690:
            coin[1] = random.randint(0, 414)
            coin[2] = random.randint(-300, -100)

        if isCollision(mainCarImgX, mainCarImgY, coin[1], coin[2], 15):
            score += 1
            coin[1] = random.randint(0, 414)
            coin[2] = random.randint(-300, -100)
            playSound("ding")

    # Display main car
    display_image(mainCar, mainCarImgX, mainCarImgY)

    # Display score
    score_text = font.render("Score: " + str(score), True, (255, 255, 255))
    wn.blit(score_text, (10, 10))

    # Display high score
    high_score_text = font.render("High Score: " + str(high_score), True, (255, 255, 255))
    wn.blit(high_score_text, (10, 40))

    pygame.display.update()

pygame.quit()
