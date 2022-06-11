import pygame as pg
from sys import exit
from random import seed, uniform
from math import cos, sin, radians

# TO-DO LATER
'''
1. Fix control panel aesthetic
2. Animate clouds & add color gradient to water & sky
3. Add intro slide & help slide
4. Add general classes
5. Shift control panel down
6. Add units
7. Add buoyancy
8. Replace COM symbol
'''

####################### INITIAL SETUP #######################

pg.init()

# setting up the screen
WIDTH = 1200
HEIGHT = 800
CAPTION = "Super Duper Ultra Incredible Absolutely Amazing BoatGame!"
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption(CAPTION)

# physical constants
GRAVITY = 9.81
# 1/2 * density of water * drag coefficient * area dimensions
DRAG_COEFFICIENT = 4.7856e-02  # .5 * 997* .0003 * .4 * .8

# colors
WHITE = (255, 255, 255)
WATER_BLUE = (58, 213, 199)
BLACK = (0, 0, 0)
GREY = (127, 127, 127)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GOLD = (255, 215, 0)
color_inactive = pg.Color(GREY)
color_active = pg.Color(BLACK)

# used for frame per second control
clock = pg.time.Clock()

# sky
sky = pg.image.load("assets/sky.jpeg")
skySize = (1200, 500)
sky = pg.transform.scale(sky, skySize)

# water
waterSize = (1200, 300)
waterColor = pg.Color(48, 213, 200)
water = pg.Surface(waterSize)
pg.draw.rect(water, waterColor, water.get_rect())

# goal
targetSize = (10, 10)
targetColor = pg.Color(255, 0, 0)
target = pg.Surface(targetSize)

# COM
comSize = (10, 10)
comColor = pg.Color(255, 0, 0)
com = pg.Surface(comSize)

# boat
boat = pg.image.load("assets/boat.png")
boatSize = (150, 100)
boat = pg.transform.scale(boat, boatSize)

# cannon
cannon = pg.image.load("assets/cannon.png")
cannonSize = (50, 50)
cannon = pg.transform.scale(cannon, cannonSize)
cannon = pg.transform.rotate(cannon, -60)

# sailor
sailor = pg.image.load("assets/sailor.png")
sailorSize = (40, 30)
sailor = pg.transform.scale(sailor, sailorSize)

# ball
ball = pg.image.load("assets/ball.png")
ballSize = (10, 10)
ball = pg.transform.scale(ball, ballSize)

####################### END INITIAL SETUP #######################

####################### VARIABLE SETUP #######################

# User-Dependent Variables
fired = False # whether simulation has started
angle = 0 # launch angle in degrees
ballVelocity = 0 # initial ball launch velocity
xBoat = 700
yBoat = 440
xBall = 800
yBall = 460
xVelocity = 0 # ball x-velocity
yVelocity = 0 # ball y-velocity
boatVelocity = 0 # boat x-velocity

# Randomly Generated Variables
seed()

# makes random ball mass
def makeBallMass():
    return round(uniform(.45, 23), 2)
ballMass = makeBallMass()

# makes random boat mass
def makeBoatMass():
    return round(uniform(20, 30), 2)
boatMass = makeBoatMass()
actualMass = boatMass - ballMass # actual boat mass removing wait of cannonball

# distance of goal from x = 0
def makeGoal():
    return round(uniform(20, 600), 2)
goal = makeGoal()
dist_from_goal = xBoat - goal # distance of boat from goal

# updates drag force
def getDrag():
    return DRAG_COEFFICIENT * (boatVelocity ** 2)
drag = getDrag()

# remaining Variables (75, 60) account for boat sprite dimensions
def getXCOM():
    return ((xBoat+75) * actualMass + xBall * ballMass) / (actualMass + ballMass)
xCOM = getXCOM()

def getYCOM():
    return ((yBoat+60) * actualMass + yBall * ballMass)  / (actualMass + ballMass)
yCOM = getYCOM()

####################### END VARIABLE SETUP #######################

####################### TEXT SETUP #######################

largeFont = pg.font.Font(None, 64)
bigFont = pg.font.Font(None, 20)
smallFont = pg.font.Font(None, 16)

# control panel
CPS = "Control Panel: "
control_panel = bigFont.render(CPS, True, BLACK, WHITE)
cpRect = control_panel.get_rect()
cpRect.center = (50, 600)

# Cannonball Mass
MS = "Cannonball Mass: " + str(ballMass)
massText = smallFont.render(MS, True, BLACK, WHITE)
massRect = massText.get_rect()
massRect.center = (64, 620)

# Boat Mass
BS = "Boat Mass: " + str(boatMass)
boatText = smallFont.render(BS, True, BLACK, WHITE)
bRect = boatText.get_rect()
bRect.center = (47, 640)

# Target Distance
TDS = "Target Distance: " + str(dist_from_goal)
targetText = smallFont.render(TDS, True, BLACK, WHITE)
tRect = targetText.get_rect()
tRect.center = (64, 660)

# Velocity Text
VS = "Input Velocity: "
vText = smallFont.render(VS, True, BLACK, WHITE)
vRect = vText.get_rect()
vRect.center = (44, 680)

# Angle Text
AS = "Input Launch Angle (Degrees): "
aText = smallFont.render(AS, True, BLACK, WHITE)
aRect = aText.get_rect()
aRect.center = (56, 700)

# COM TEXT
COMS = "COM"
comText = smallFont.render(COMS, True, BLACK)
comRect = aText.get_rect()
comRect.topleft = (xCOM, yCOM+10)

# goal TEXT
GS = "GOAL"
goalText = smallFont.render(GS, True, GOLD)
goalRect = aText.get_rect()
goalRect.topleft = (goal, 510)
# Lost Text
LS = "You Lost!"
lostText = largeFont.render(LS, True, RED)

# Won Text
WS = "You Won!"
wonText = largeFont.render(WS, True, RED)

####################### END TEXT SETUP #######################

####################### INPUT SETUP #######################
# Velocity Input
velocityRect = pg.Rect(85, 673, 20, 15)
vColor = color_inactive
vActive = False
userVelocity = ''

# Angle Input
angleRect = pg.Rect(137, 693, 20, 15)
aColor = color_inactive
aActive = False
userAngle = ''

# Enter Button
ES = "Fire!"
buttonText = bigFont.render(ES, True, BLACK, RED)
buttonRect = buttonText.get_rect()
buttonRect.center = (17, 720)

# Restart Button
resS = "Reset Game"
resText = bigFont.render(resS, True, BLACK, GREY)
resRect = resText.get_rect()
resRect.center = (640, 670)
res2Rect = resText.get_rect()
res2Rect.center = (595, 670)

# Replay Button
repS = "Replay Level"
repText = bigFont.render(repS, True, BLACK, GREY)
repRect = repText.get_rect()
repRect.center = (550, 670)

####################### END INPUT SETUP #######################

####################### RENDERING SETUP #######################

# Always rendered
def render():
    screen.blit(sky, (0, 0))
    screen.blit(water, (0, 500))
    screen.blit(boat, (xBoat, yBoat))
    screen.blit(sailor, (xBoat + 60, 460))
    pg.draw.rect(screen, WHITE , pg.Rect(0,580,200,150))
    screen.blit(control_panel, cpRect)
    screen.blit(massText, massRect)
    screen.blit(boatText, bRect)
    screen.blit(targetText, tRect)
    screen.blit(comText,  (xCOM, yCOM+10))
    screen.blit(goalText,  (goal, 500+10))
    screen.blit(vText, vRect)
    screen.blit(aText, aRect)
    screen.blit(buttonText, buttonRect)
    pg.draw.rect(screen, BLACK , pg.Rect(0,580,200,150),  2)


    if fired and xBall>xBoat+50:
        screen.blit(ball, (xBall, yBall))

    if angle > 0:
        blitRotateCenter(screen, cannon, (xBoat+80,435), angle)
    else:
        screen.blit(cannon, (xBoat + 80, 435))

    # target drawing
    pg.draw.rect(target, targetColor, target.get_rect())
    screen.blit(target, (goal, 500))

    # COM drawing
    pg.draw.rect(com, comColor, com.get_rect())
    screen.blit(com, (xCOM, yCOM))

    # velocity input rendering
    velocitySurface = smallFont.render(userVelocity, True, vColor)
    velocityRect.w = max(50, velocitySurface.get_width() + 10)
    screen.blit(velocitySurface, (velocityRect.x + 5, velocityRect.y + 5))
    pg.draw.rect(screen, vColor, velocityRect, 1)

    # angle input rendering
    angleSurface = smallFont.render(userAngle, True, aColor)
    angleRect.w = max(50, angleSurface.get_width() + 10)
    screen.blit(angleSurface, (angleRect.x + 5, angleRect.y + 5))
    pg.draw.rect(screen, aColor, angleRect, 1)

# Rendered if player lost
def lostRender():
    screen.blit(lostText, (500, 600))
    screen.blit(repText, repRect)
    screen.blit(resText, resRect)

def wonRender():
    screen.blit(wonText, (500, 600))
    screen.blit(resText, res2Rect)

# Update screen
def frame():
    # update
    pg.display.update()
    clock.tick(60)

# restart will play the same level
def restart():

    xBoat = 700

    dist_from_goal = xBoat - goal

    xBall = 800
    yBall = 460
    xVelocity = 0
    yVelocity = 0

    xCOM = getXCOM()
    yCOM = getYCOM()

    fired = False
    done = True

# reset will start the game anew
def reset():

    restart()
    goal = makeGoal()

    ballMass = makeBallMass()
    boatMass = makeBoatMass()
    actualMass = boatMass - ballMass

# display iamge as rotated
def blitRotateCenter(surf, image, topleft, degrees):

    rotated_image = pg.transform.rotate(image, degrees)
    new_rect = rotated_image.get_rect(center = image.get_rect(topleft = topleft).center)

    surf.blit(rotated_image, new_rect)

####################### END RENDERING SETUP #######################

####################### DRIVER LOOP #######################

# game driver loop (rounds loop within)

counter = 0

while True:

    if not fired:

        for event in pg.event.get(): # grab events
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            # handler for clicking
            if event.type == pg.MOUSEBUTTONDOWN:
                # handler for clicking on input
                if buttonRect.collidepoint(event.pos):
                    #debugging
                    #print(userAngle)
                    # handle clicking on enter
                    fired = not fired
                    try:
                        angle = float(userAngle.strip())
                    except ValueError:
                        continue
                    try:
                        ballVelocity = float(userVelocity.strip())
                    except:
                        continue
                    xVelocity = cos(radians(angle)) * ballVelocity
                    yVelocity = sin(radians(angle)) * ballVelocity
                    boatVelocity = (ballMass * xVelocity) / actualMass
                    drag = getDrag()
                if velocityRect.collidepoint(event.pos):
                    vActive = not vActive
                else:
                    vActive = False
                if angleRect.collidepoint(event.pos):
                    aActive = not aActive
                else:
                    aActive = False
                vColor = color_active if vActive else color_inactive
                aColor = color_active if aActive else color_inactive
            # handler for saving user input to screen
            if event.type == pg.KEYDOWN:
                # handler for velocity input rendering
                if vActive:
                    if event.key == pg.K_BACKSPACE:
                        userVelocity = userVelocity[:-1]
                    else:
                        userVelocity += event.unicode
                # handler for angle input rendering
                if aActive:
                    if event.key == pg.K_BACKSPACE:
                        userAngle = userAngle[:-1]
                    else:
                        userAngle += event.unicode
        render()
        frame()

    else:

        while boatVelocity >= 1 and xBoat > 0:

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()

            drag = getDrag()
            if yBall < 490:
                xBall += xVelocity
                if (yBall - yVelocity) >= 490:
                    yBall = 490
                else:
                    yBall -= yVelocity
                yVelocity -= GRAVITY
            xBoat -= boatVelocity
            dist_from_goal -= boatVelocity
            boatVelocity -= drag / actualMass

            xCOM = getXCOM()
            yCOM = getYCOM()

            render()
            frame()

        boatVelocity = 0

        if abs(dist_from_goal) < 5:
            while fired:

                for event in pg.event.quit():
                    if event.type == pg.QUIT:
                        pg.quit()
                        exit()
                    if event.type == pg.MOUSEBUTTONDOWN:

                        if resRect.collidepoint(event.pos):

                            xBoat = 700
                            goal = makeGoal()
                            dist_from_goal = xBoat - goal

                            xBall = 800
                            yBall = 460
                            xVelocity = 0
                            yVelocity = 0

                            ballMass = makeBallMass()
                            boatMass = makeBoatMass()
                            actualMass = boatMass - ballMass

                            xCOM = getXCOM()
                            yCOM = getYCOM()

                            fired = False

                render()
                wonRender()
                frame()

        else:
            while fired:

                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        pg.quit()
                        exit()
                    if event.type == pg.MOUSEBUTTONDOWN:
                        if repRect.collidepoint(event.pos):
                            xBoat = 700

                            dist_from_goal = xBoat - goal

                            xBall = 800
                            yBall = 460
                            xVelocity = 0
                            yVelocity = 0

                            xCOM = getXCOM()
                            yCOM = getYCOM()

                            fired = False

                        if resRect.collidepoint(event.pos):

                            xBoat = 700
                            goal = makeGoal()
                            dist_from_goal = xBoat - goal

                            xBall = 800
                            yBall = 460
                            xVelocity = 0
                            yVelocity = 0

                            ballMass = makeBallMass()
                            boatMass = makeBoatMass()
                            actualMass = boatMass - ballMass

                            xCOM = getXCOM()
                            yCOM = getYCOM()

                            fired = False

                render()
                lostRender()
                frame()

####################### END DRIVER LOOP #######################
