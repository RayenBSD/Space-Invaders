import pygame as pg
import random as rand
import os

class Ship:
    #Constructor
    def __init__(self, X, Y):
        self.X = X
        self.Y = Y
    #setter
    def setX(self, X):
        self.X = X
    def setY(self, Y):
        self.Y = Y
    #getter
    def getX(self):
        return self.X
    def getY(self):
        return self.Y
    #adder
    def addX(self, X):
        self.X += X
    def addY(self, Y):
        self.Y += Y

class Laser(Ship):
    pass

pg.init()
screenX, screenY = 700, 700
screen = pg.display.set_mode((screenX, screenY))
pg.display.set_caption("Space Invaders")
icon = pg.image.load(os.path.join("assets", "pixel_ship_yellow.png"))
pg.display.set_icon(icon)

score = 0
isFired = False
number = 5
level = 1
health = 10

#green
isReady = False
ship = []
shipPos = []
laser = []
laserPos = []
fired = []

#Back Ground
bg = pg.transform.scale(pg.image.load(os.path.join("assets", "background_black.png")), (700, 700))

#Characters
psy = pg.image.load(os.path.join("assets", "pixel_ship_yellow.png"))

#Laser
ply = pg.image.load(os.path.join("assets", "pixel_laser_yellow.png"))

#SET Characters
pixel_ship_yellow = Ship(305, 550)

#SET Laser
pixel_laser_yellow = Laser(0, -100)

def green():
    ship.append(pg.image.load(os.path.join("assets", "pixel_ship_green_small.png")))
    laser.append(pg.image.load(os.path.join("assets", "pixel_laser_green.png")))

def blue():
    ship.append(pg.transform.scale(pg.image.load(os.path.join("assets", "pixel_ship_blue_small.png")), (70, 50)))
    laser.append(pg.image.load(os.path.join("assets", "pixel_laser_blue.png")))

def red():
    ship.append(pg.image.load(os.path.join("assets", "pixel_ship_red_small.png")))
    laser.append(pg.image.load(os.path.join("assets", "pixel_laser_red.png")))

def move():
    global isFired

    #MAIN Character
    stepYellow = 10
    keys = pg.key.get_pressed()

    if keys[pg.K_z] and pixel_ship_yellow.getY() - stepYellow >= 0:
        pixel_ship_yellow.addY(-stepYellow)
    if keys[pg.K_s] and pixel_ship_yellow.getY() + 90 + stepYellow < screenY:
        pixel_ship_yellow.addY(stepYellow)
    if keys[pg.K_q] and pixel_ship_yellow.getX() - stepYellow >= 0:
        pixel_ship_yellow.addX(-stepYellow)
    if keys[pg.K_d] and pixel_ship_yellow.getX() + 90 + stepYellow < screenX:
        pixel_ship_yellow.addX(stepYellow)
    if keys[pg.K_SPACE] and not isFired:
        isFired = True
        pixel_laser_yellow.setY(pixel_ship_yellow.getY())
        pixel_laser_yellow.setX(pixel_ship_yellow.getX())
    if isFired:
        if pixel_laser_yellow.getY() >= 0:
            pixel_laser_yellow.addY(-stepYellow)
        else:
            pixel_laser_yellow.setX(screenX+50)
            isFired = False

def stage():
    global isReady, number, score, screen, isFired, level, health

    shipStep = 1

    if not isReady:
        for i in range(number):
            rand.choice([green(),red(),blue()])
            shipPos.append(Ship(rand.randint(70, 630), rand.randint(number*-100, 0)))
            laserPos.append(Laser(0, -100))
            fired.append(isFired)
        isReady = True
    if isReady:
        for i in range(number):
            shipPos[i].addY(shipStep)
            if not fired[i]:
                laserPos[i].setX(shipPos[i].getX() - 15)
                laserPos[i].setY(shipPos[i].getY() - 15)
                fired[i] = True
            if fired[i]:
                if laserPos[i].getY() + 90 + shipStep <= screenY + 100:
                    laserPos[i].addY(shipStep+2)
                else:
                    fired[i] = False
            screen.blit(ship[i], (shipPos[i].getX(), shipPos[i].getY()))
            screen.blit(laser[i], (laserPos[i].getX(), laserPos[i].getY()))
            if (shipPos[i].getX() <= pixel_laser_yellow.getX()+50 <= shipPos[i].getX()+70) and (shipPos[i].getY() < pixel_laser_yellow.getY() <= shipPos[i].getY() + 50):
                score += 1
                shipPos[i].setX(rand.randint(70, 630))
                shipPos[i].setY(rand.randint(number*-100, 0))
                pixel_laser_yellow.setX(screenX + 50)
                isFired = False
            if (pixel_ship_yellow.getX() <= laserPos[i].getX()+50 <= pixel_ship_yellow.getX()+100) and (pixel_ship_yellow.getY() <= laserPos[i].getY() <= pixel_ship_yellow.getY() + 90):
                health -= 1
                laserPos[i].setX(screenX + 50)
                fired[i] = False
            if (((shipPos[i].getX() < pixel_ship_yellow.getX() < shipPos[i].getX() + 70) or (shipPos[i].getX() > pixel_ship_yellow.getX() > shipPos[i].getX() + 70))
                and ((shipPos[i].getY() < pixel_ship_yellow.getY() < shipPos[i].getY() + 70) or (shipPos[i].getY() > pixel_ship_yellow.getY() > shipPos[i].getY() + 70))):
                health -= 1
                shipPos[i].setX(rand.randint(70, 630))
                shipPos[i].setY(rand.randint(number*-100, 0))
            if (shipPos[i].getY() > 700):
                shipPos[i].setX(rand.randint(70, 630))
                shipPos[i].setY(rand.randint(number*-100, 0))
                score += 1
            if score == number:
                isReady = False
                number += 1
                level += 1
            if health == 0:
                quit()

def redraw():
    #Back Ground
    screen.blit(bg, (0, 0))
    # Characters
    screen.blit(psy, (pixel_ship_yellow.getX(), pixel_ship_yellow.getY()))
    # Laser
    screen.blit(ply, (pixel_laser_yellow.getX(), pixel_laser_yellow.getY()))
    #info
    showScore = pg.font.Font("freesansbold.ttf", 32).render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(showScore, (0, 0))

    showLevel = pg.font.Font("freesansbold.ttf", 32).render(f"Level: {level}", True, (255, 255, 255))
    screen.blit(showLevel, (550, 0))

    showHealth = pg.font.Font("freesansbold.ttf", 32).render(f"Health: {health}", True, (255, 255, 255))
    screen.blit(showHealth, (0, 650))

def main():
    while True:
        pg.time.Clock().tick(60)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                quit()
        pg.display.update()
        redraw()
        move()
        stage()

if __name__ == "__main__":
    main()