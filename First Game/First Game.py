import pygame
import random
import math
from pygame import mixer

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("arcade-game.png")
pygame.display.set_icon(icon)
mixer.music.load("cyberpunk-2099-10701.mp3")
mixer.music.play(-1)

background = pygame.image.load("Background.jpg")

# Redline
Red_Line = pygame.Surface([800, 10])
Red_Line.fill((255, 0, 0))

# Player
playerImage = pygame.image.load("spaceship.png")
PlayerX = 460
PlayerY = 450
player_Xchange = 0
player_Ychange = 0

# Enemy
EnemyImage = []
EnemyX = []
EnemyY = []
Enemy_Xchange = []
Enemy_Ychange = []
Num_Enemies = 5
Max_Enemies = 30
Add_Enemies = False

for i in range(Num_Enemies):
    EnemyImage.append(pygame.image.load("alien.png"))
    EnemyX.append(random.randint(0, 740))
    EnemyY.append(random.randint(50, 240))
    Enemy_Xchange.append(0.4)
    Enemy_Ychange.append(20)
# Score

Score_Val = 0
font = pygame.font.Font("scoreboard.ttf", 32)
ScoreX = 10
ScoreY = 10


def ShowScore(x, y):
    score = font.render("Score: " + str(Score_Val), True, (255, 255, 255))
    screen.blit(score, (x, y))


# Bullet
class BulletClass:
    def __init__(self):
        self.__BulletImage = pygame.image.load("bullet.png")
        self.__BulletX = 460
        self.__BulletY = 380
        self.__Bullet_Xchange = 0
        self.__Bullet_Ychange = -0.1
        self.__State = False

    def SetStateTrue(self):
        self.__State = True

    def SetStateFalse(self):
        self.__State = False

    def ChangeY(self):
        self.__BulletY += self.__Bullet_Ychange

    def GetState(self):
        return self.__State

    def SetBulletX(self, X):
        self.__BulletX = X

    def SetBulletY(self, Y):
        self.__BulletY = Y

    def GetBulletImage(self):
        return self.__BulletImage

    def GetBulletX(self):
        return self.__BulletX

    def GetBulletY(self):
        return self.__BulletY


BulletList = list(enumerate([BulletClass() for i in range(3)]))


def Player(x, y):
    screen.blit(playerImage, (x, y))


def Enemy(x, y, i):
    screen.blit(EnemyImage[i], (x, y))


def Bullet(x, y, Index):
    screen.blit(BulletList[Index][1].GetBulletImage(), (x, y))


def CheckCollision(BulletX, BulletY, EnemyX, EnemyY):
    Distance = math.sqrt(
        (math.pow(BulletX - EnemyX, 2)) + (math.pow(BulletY - EnemyY, 2))
    )
    if Distance <= 48:
        return True
    else:
        return False


over_Game = pygame.font.Font("game_over.ttf", 64)


def game_over_text():
    over_text = font.render("GAME OVER", True, ((0, 0, 0)))
    screen.blit(over_text, (310, 250))
    ShowScore(310, 300)


running = True
Game_End = False  # Remove Score from Top


def main():
    global PlayerX, PlayerY, player_Xchange, player_Ychange, EnemyImage, EnemyX, EnemyY, Enemy_Xchange, Enemy_Ychange
    global BulletList, Num_Enemies, Score_Val, Add_Enemies, Max_Enemies, Game_End
    while True:
        screen.fill((45, 125, 105))
        screen.blit(background, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    if Num_Enemies <= 15:
                        player_Xchange = -1.1
                    else:
                        player_Xchange = -2.2
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    if Num_Enemies <= 10:
                        player_Xchange = 1.1
                    else:
                        player_Xchange = 2.2
                if event.key == pygame.K_SPACE:
                    for Index, Bullets in BulletList:
                        if Bullets.GetState() == False:
                            Bullet_Sound = mixer.Sound("Gun.mp3")
                            Bullet_Sound.play()
                            BulletX = PlayerX
                            Bullets.SetBulletX(BulletX)
                            Bullet(Bullets.GetBulletX(), PlayerY, Index)
                            Bullets.SetStateTrue()
                            break

            if event.type == pygame.KEYUP:
                if (
                    event.key == pygame.K_LEFT
                    or event.key == pygame.K_RIGHT
                    or event.key == pygame.K_d
                    or event.key == pygame.K_a
                ):
                    player_Xchange = 0

        # Enemy
        for i in range(Num_Enemies):
            if EnemyY[i] >= 400:  # Game Over
                for j in range(Num_Enemies):
                    EnemyY[j] = 2000
                Game_End = True
                game_over_text()
                break

            EnemyX[i] += Enemy_Xchange[i]
            if Num_Enemies <= 15:
                if EnemyX[i] <= 0:
                    EnemyX[i] = 0
                    Enemy_Xchange[i] = 0.4
                    EnemyY[i] += Enemy_Ychange[i]
                elif EnemyX[i] >= 740:
                    EnemyX[i] = 740
                    Enemy_Xchange[i] = -0.4
                    EnemyY[i] += Enemy_Ychange[i]
                Enemy(EnemyX[i], EnemyY[i], i)
            else:  # inc speed
                if EnemyX[i] <= 0:
                    EnemyX[i] = 0
                    Enemy_Xchange[i] = 1.1
                    EnemyY[i] += Enemy_Ychange[i]
                elif EnemyX[i] >= 740:
                    EnemyX[i] = 740
                    Enemy_Xchange[i] = -1.1
                    EnemyY[i] += Enemy_Ychange[i]
                Enemy(EnemyX[i], EnemyY[i], i)

        # Bullet
        for Index, Bullets in BulletList:
            if Bullets.GetState() == True:
                if Num_Enemies <= 15:
                    Bullets.SetBulletY(Bullets.GetBulletY() - 0.8)  # Speed of Bullet
                    Bullet(Bullets.GetBulletX(), Bullets.GetBulletY(), Index)
                else:
                    Bullets.SetBulletY(Bullets.GetBulletY() - 1.7)  # Speed of Bullet
                    Bullet(Bullets.GetBulletX(), Bullets.GetBulletY(), Index)

                if Bullets.GetBulletY() <= 0:
                    Bullets.SetBulletY(PlayerY)
                    Bullets.SetStateFalse()

        # Collisions
        for Index, Bullets in BulletList:
            for i in range(Num_Enemies):
                if Bullets.GetState() == True:
                    Collision = CheckCollision(
                        Bullets.GetBulletX(), Bullets.GetBulletY(), EnemyX[i], EnemyY[i]
                    )
                    if Collision:
                        Die_Sound = mixer.Sound("Die.mp3")
                        Die_Sound.play()
                        Bullets.SetBulletY(PlayerY)  # Reset Bullet
                        Bullets.SetStateFalse()

                        EnemyX[i] = random.randint(0, 740)  # ResetEnemy
                        EnemyY[i] = random.randint(250, 360)

                        Score_Val += 1
                        Add_Enemies = True
                        break
        if Add_Enemies and (Num_Enemies <= Max_Enemies):
            Num_Enemies += 1
            EnemyImage.append(pygame.image.load("alien.png"))
            EnemyX.append(random.randint(0, 740))
            EnemyY.append(random.randint(50, 240))
            Enemy_Xchange.append(0.4)
            Enemy_Ychange.append(20)
            Add_Enemies = False

        # Player
        PlayerX += player_Xchange
        if PlayerX <= 0:
            PlayerX = 0
        elif PlayerX >= 740:
            PlayerX = 740

        if not Game_End:
            ShowScore(ScoreX, ScoreY)

        Player(PlayerX, PlayerY)
        screen.blit(Red_Line, (0, 425))
        pygame.display.update()


main()
