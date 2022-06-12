import subprocess
import importlib.util
from sys import executable

package_name = "pygame"

spec = importlib.util.find_spec(package_name)
if spec is None:
    print(package_name + " is not installed. Installing.")
    subprocess.check_call([executable, "-m", "pip", "install", package_name])

import pygame as pg
from sys import exit
from time import sleep
from sys import modules
from random import seed, uniform
from math import cos, sin, radians

# TO-DO LATER
'''
1. Fix control panel aesthetic
2. Animate clouds & add color gradient to water & sky
3. Add intro slide & help slide
4. Add general classes
5. Shift control panel down
7. Add buoyancy
8. Replace COM symbol
9. Make win/lose screen nicer
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

# help icon
help = pg.image.load("assets/help.png")
helpSize = (60, 40)
help = pg.transform.scale(help, helpSize)
helpRect = help.get_rect()
helpRect.topleft = (1140, 10)

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

# win meme
win = pg.image.load("assets/win.jpg")
winSize = (400, 400)
win = pg.transform.scale(win, winSize)

# lose meme
lose = pg.image.load("assets/lose.png")
loseSize = (400, 400)
lose = pg.transform.scale(lose, loseSize)
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
dist_from_goal = round(xBoat + 75 - goal, 2) # distance of boat from goal

# updates drag force
def getDrag():
    return DRAG_COEFFICIENT * (boatVelocity ** 2)
drag = getDrag()

# centers of mass (75, 60) account for boat sprite dimensions
def getXCOM():
    return ((xBoat+75) * actualMass + xBall * ballMass) / (actualMass + ballMass)
xCOM = getXCOM()

def getYCOM():
    return ((490) * actualMass + yBall * ballMass)  / (actualMass + ballMass)
yCOM = getYCOM()

####################### END VARIABLE SETUP #######################

####################### TEXT SETUP #######################

smallFont = pg.font.Font(None, 16)
bigFont = pg.font.Font(None, 20)
largeFont = pg.font.Font(None, 64)

# Welcome Text 1
W1S = "Welcome to the BoatGame!"
W1Text = largeFont.render(W1S, True, BLACK)
W1Rect = W1Text.get_rect()
W1Rect.topleft = (355, 550)

# Welcome Text 2
W2S = "Click on Start to start game, or"
W2Text = largeFont.render(W2S, True, BLACK)
W2Rect = W2Text.get_rect()
W2Rect.topleft = (340, 600)

# Welcome Text 3
W3S = "click on Help in top right for help!"
W3Text = largeFont.render(W3S, True, BLACK)
W3Rect = W3Text.get_rect()
W3Rect.topleft = (320, 650)

# Look here
LHS = "Look in the terminal for instructions!"
LHText = bigFont.render(LHS, True, BLACK)
LHRect = LHText.get_rect()
LHRect.topleft = (925, 25)

# Help Message
HS = """Instructions for Playing the BoatGame: \n\n

The goal of BoatGame is to move the boat, which starts centered at meter 700, a certain \n
target distance, displayed in the control panel as 'Target' in meters to the left of the \n
boat. \n
The player does this by inputting a certain start velocity, in meters per second, and angle, \n
in degrees, for the cannon on the boat to shoot the cannonball at. They then hit the 'Fire!' \n
button, projecting the cannonball to the right and sending the boat some distance to the left.\n
If the boat is within 65 meters of the target, the player wins. Otherwise, they have the chance \n
to either 'Replay' the same level, or 'Restart' the game with new figures. \n\n

To most effectively win BoatGame, the player should rely on the underlying physics. Apart from \n
having access to the target distance in the control panel, the player can also find there \n
the mass of the boat and of the cannonball. It should be noted that, in the following calculations, \n
the mass of the boat has the mass of cannonball subtracted from it once the cannonball has been fired. \n
Additionally, each pixel on the screen is treated as one pixel for a total of 1200. \n
After, the cannonball is fired, conservation of momentum is used to find the starting velocity of the \n
boat. \n
First, the cosine of the launch angle (in radians) is multipled by the input velocity to find the \n
starting x-velocity of the cannonball. This looks as follows: \n
\t x_vel_ball = cosine(angle) * userVelocity \n
It is important to note that the y-velocity of the ball is not accounted for, as this is not a \n
buoyancy simulation. \n
After this, the motion of the boat is updated each "round" using the following steps:\n
\t 1. The x-velocity of the boat is found using conservation of momentum.\n
\t 2. The drag force on the boat is found by multiplying the drag coefficient\n
\t (4.7856e-02, or .5 * 997* .0003 * .4 * .8, \n
\t or 1/2 * density of water * drag coefficient * area dimensions) by the square of the \n
\t boat's x-velocity. \n
\t 3. The acceleration of the boat is found by dividing drag force by boat mass. \n
\t 4. The boat is moved to the left by the x-velocity. \n
\t 5. The x-velocity has the acceleration subtracted from it. \n
This loop continues until the x-velocity of the boat is less than 1 m/s, or until the boat \n
moves off the edge of the screen.\n
In pseudocode, this approximately looks like: \n
\t x_vel_boat = (rock_mass * x_vel_ball) / boat_mass \n
\t while x_vel_boat >= 1 and xBoat > 0: \n
\t \t drag = DRAG_COEFFICIENT * (boatVelocity ** 2) \n
\t \t xBoat -= x_vel_boat \n
\t \t dist_from_goal -= boatVelocity \n
\t \t acceleration = drag / actualMass # mass of boat - mass of ball \n
\t \t x_vel_boat -= acceleration\n
In addition, the BoatGame displays the center of mass (COM) of the system, and, \n
if the user pays close attention, simulates the projectile motion of the  \n
cannonball using the kinematics equations.
"""

# control panel
CPS = "Control Panel: "
control_panel = bigFont.render(CPS, True, BLACK, WHITE)
cpRect = control_panel.get_rect()
cpRect.center = (50, 600)

# Cannonball Mass
MS = "Cannonball Mass: "

# Boat Mass
BS = "Boat Mass: "

# Target Distance
TDS = "Target Distance: "

# Velocity Text
VS = "Input Velocity (m/s): "
vText = smallFont.render(VS, True, BLACK, WHITE)
vRect = vText.get_rect()
vRect.center = (60, 680)

# Angle Text
AS = "Input Launch Angle (Degrees): "
aText = smallFont.render(AS, True, BLACK, WHITE)
aRect = aText.get_rect()
aRect.center = (56, 700)

# COM TEXT
COMS = "COM"
comText = smallFont.render(COMS, True, BLACK)
comRect = comText.get_rect()
comRect.topleft = (xCOM, yCOM+10)

# goal TEXT
GS = "GOAL"
goalText = smallFont.render(GS, True, GOLD)
goalRect = goalText.get_rect()
goalRect.topleft = (goal, 510)

# Lost Text
LS = "You Lost!"
lostText = largeFont.render(LS, True, RED)
lostRect = lostText.get_rect()
lostRect.center = (590, 630)

# Won Text
WS = "You Won!"
wonText = largeFont.render(WS, True, RED)
wonRect = wonText.get_rect()
wonRect.center = (580, 620)

####################### END TEXT SETUP #######################

####################### INPUT SETUP #######################

# Start Button
SS = "Start!"
startText = largeFont.render(SS, True, BLACK)
startRect = startText.get_rect()
startRect.topleft = (600, 700)

# Velocity Input
velocityRect = pg.Rect(113, 673, 20, 15)
vColor = color_inactive
vActive = False
userVelocity = '0'

# Angle Input
angleRect = pg.Rect(137, 693, 20, 15)
aColor = color_inactive
aActive = False
userAngle = '0'

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
    screen.blit(help, helpRect)
    screen.blit(boat, (xBoat, yBoat))
    screen.blit(sailor, (xBoat + 60, 460))
    pg.draw.rect(screen, WHITE , pg.Rect(0,580,200,150))
    screen.blit(control_panel, cpRect)

    massText = smallFont.render(MS + str(ballMass) + " kg", True, BLACK, WHITE)
    massRect = massText.get_rect()
    massRect.center = (70, 620)
    screen.blit(massText, massRect)

    boatText = smallFont.render(BS + str(boatMass) + " kg", True, BLACK, WHITE)
    bRect = boatText.get_rect()
    bRect.center = (55, 640)
    screen.blit(boatText, bRect)

    targetText = smallFont.render(TDS + str(round(dist_from_goal, 2)) + " m", True, BLACK, WHITE)
    tRect = targetText.get_rect()
    tRect.center = (72, 660)
    screen.blit(targetText, tRect)

    screen.blit(comText,  (xCOM, yCOM+10))
    screen.blit(goalText,  (goal, 500+10))
    screen.blit(vText, vRect)
    screen.blit(aText, aRect)
    screen.blit(buttonText, buttonRect)
    pg.draw.rect(screen, BLACK , pg.Rect(0,580,200,150),  2)


    if fired and xBall>xBoat+130:
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
    screen.blit(lostText, lostRect)
    screen.blit(repText, repRect)
    screen.blit(resText, resRect)
    screen.blit(lose, (400,0))

# rendered if player won
def wonRender():
    screen.blit(wonText, wonRect)
    screen.blit(resText, res2Rect)
    screen.blit(win, (400,0))

# Update screen
def frame():
    # update
    pg.display.update()
    clock.tick(60)

# display iamge as rotated
def blitRotateCenter(surf, image, topleft, degrees):

    rotated_image = pg.transform.rotate(image, degrees)
    new_rect = rotated_image.get_rect(center = image.get_rect(topleft = topleft).center)

    surf.blit(rotated_image, new_rect)

####################### END RENDERING SETUP #######################

####################### DRIVER LOOP #######################

# game driver loop (rounds loop within)

i = 0
counter = 0
clicked = False
for counter in range(len(W1S) + 1):

    if clicked: break

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
        if event.type == pg.MOUSEBUTTONDOWN: clicked = not clicked

    tmp = largeFont.render(W1S[:counter] + "|", True, BLACK)
    render()
    screen.blit(tmp, (475 - i, 550))
    i += 5
    frame()
    sleep(.1)

i = 0
counter = 0
clicked = False
for counter in range(len(W2S) + 1):

    if clicked: break

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
        if event.type == pg.MOUSEBUTTONDOWN: clicked = not clicked

    tmp = largeFont.render(W2S[:counter] + "|", True, BLACK)
    render()
    screen.blit(W1Text, W1Rect)
    screen.blit(tmp, (500 - i, 600))
    i += 5
    frame()
    sleep(.1)

i = 0
counter = 0
clicked = False
for counter in  range(len(W3S) + 1):

    if clicked: break

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
        if event.type == pg.MOUSEBUTTONDOWN: clicked = not clicked

    tmp = largeFont.render(W3S[:counter] + "|", True, BLACK)
    render()
    screen.blit(W1Text, W1Rect)
    screen.blit(W2Text, W2Rect)
    screen.blit(tmp, (500 - i, 650))
    i += 5
    frame()
    sleep(.1)

started = False
while not started:

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
        if event.type == pg.MOUSEBUTTONDOWN:
            if startRect.collidepoint(event.pos):
                started = True
            if helpRect.collidepoint(event.pos):
                print(HS)
                for i in range(100):
                    for event in pg.event.get():
                        if event.type == pg.QUIT:
                            pg.quit()
                            exit()
                    render()
                    screen.blit(W1Text, W1Rect)
                    screen.blit(W2Text, W2Rect)
                    screen.blit(W3Text, W3Rect)
                    screen.blit(startText, startRect)
                    screen.blit(LHText, LHRect)
                    frame()

    render()
    screen.blit(W1Text, W1Rect)
    screen.blit(W2Text, W2Rect)
    screen.blit(W3Text, W3Rect)
    screen.blit(startText, startRect)
    frame()


while True:



    if not fired:

        for event in pg.event.get(): # grab events
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            # handler for clicking
            if event.type == pg.MOUSEBUTTONDOWN:
                # help
                if helpRect.collidepoint(event.pos):
                    print(HS)
                    for i in range(100):
                        for event in pg.event.get():
                            if event.type == pg.QUIT:
                                pg.quit()
                                exit()
                    render()
                    screen.blit(W1Text, W1Rect)
                    screen.blit(W2Text, W2Rect)
                    screen.blit(W3Text, W3Rect)
                    screen.blit(startText, startRect)
                    screen.blit(LHText, LHRect)
                    frame()
                # handler for clicking on input
                if buttonRect.collidepoint(event.pos):
                    #debugging
                    #print(userAngle)
                    # handle clicking on enter
                    fired = not fired
                    try:
                        if userAngle.strip() == '':
                            angle = 0
                        else:
                            angle = float(userAngle.strip())
                    except ValueError:
                        continue
                    try:
                        if userVelocity.strip() == '':
                            ballVelocity = 0
                        else:
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

            #default values
            if  not vActive and userVelocity == '':
                userVelocity = '0'
            if not aActive and userAngle == '':
                userAngle = '0'
            if vActive and userVelocity == '0':
                userVelocity = userVelocity[:-1]
            if aActive and userAngle == '0':
                userAngle = userAngle[:-1]

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

        if abs(dist_from_goal) < 65:
            while fired:

                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        pg.quit()
                        exit()
                    if event.type == pg.MOUSEBUTTONDOWN:

                        if helpRect.collidepoint(event.pos):
                            print(HS)
                            for i in range(100):
                                for event in pg.event.get():
                                    if event.type == pg.QUIT:
                                        pg.quit()
                                        exit()
                            render()
                            screen.blit(W1Text, W1Rect)
                            screen.blit(W2Text, W2Rect)
                            screen.blit(W3Text, W3Rect)
                            screen.blit(startText, startRect)
                            screen.blit(LHText, LHRect)
                            frame()

                        if res2Rect.collidepoint(event.pos):

                            xBoat = 700
                            goal = makeGoal()
                            dist_from_goal = xBoat +75 - goal

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
                        if helpRect.collidepoint(event.pos):
                            print(HS)
                            for i in range(100):
                                for event in pg.event.get():
                                    if event.type == pg.QUIT:
                                        pg.quit()
                                        exit()
                            render()
                            screen.blit(W1Text, W1Rect)
                            screen.blit(W2Text, W2Rect)
                            screen.blit(W3Text, W3Rect)
                            screen.blit(startText, startRect)
                            screen.blit(LHText, LHRect)
                            frame()
                        if repRect.collidepoint(event.pos):

                            xBoat = 700

                            dist_from_goal = xBoat + 75 - goal

                            xBall = 800
                            yBall = 460
                            xVelocity = 0
                            yVelocity = 0

                            xCOM = getXCOM()
                            yCOM = getYCOM()

                            fired = False

                        if resRect.collidepoint(event.pos):

                            xBoat = 700
                            goal = round(uniform(20, 600), 2)
                            dist_from_goal = xBoat + 75 - goal

                            xBall = 800
                            yBall = 460
                            xVelocity = 0
                            yVelocity = 0

                            ballMass = round(uniform(.45, 23), 2)
                            boatMass = round(uniform(20, 30), 2)
                            actualMass = boatMass - ballMass

                            xCOM = getXCOM()
                            yCOM = getYCOM()

                            fired = False

                render()
                lostRender()
                frame()

####################### END DRIVER LOOP #######################
