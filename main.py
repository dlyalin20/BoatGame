from matplotlib import use
import pygame as pg
from sys import exit

####################### INITIAL SETUP #######################

pg.init()

# setting up the screen
WIDTH = 1200
HEIGHT = 800
CAPTION = "Super Duper Ultra Incredible Absolutely Amazing BoatGame!"
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption(CAPTION)

# colors
WHITE = (255, 255, 255)
WATER_BLUE = (58, 213, 199)
BLACK = (0, 0, 0)

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

####################### TEXT SETUP #######################

bigFont = pg.font.Font(None, 20)
smallFont = pg.font.Font(None, 16)

# control panel
CPS = "Control Panel: "
control_panel = bigFont.render(CPS, True, BLACK, WATER_BLUE)
cpRect = control_panel.get_rect()
cpRect.center = (50, 600)

# Cannonball Mass
MS = "Cannonball Mass: "
massText = smallFont.render(MS, True, BLACK, WATER_BLUE)
massRect = massText.get_rect()
massRect.center = (50, 620)

# Boat Mass
BS = "Boat Mass: "
boatText = smallFont.render(BS, True, BLACK, WATER_BLUE)
bRect = boatText.get_rect()
bRect.center = (35, 640)

# Target Distance
TDS = "Target Distance: "
targetText = smallFont.render(TDS, True, BLACK, WATER_BLUE)
tRect = targetText.get_rect()
tRect.center = (50, 660)

# Velocity Input
velocityRect = pg.Rect(100, 100, 140, 32)
color_inactive = pg.Color('lightskyblue3')
color_active = pg.Color('dodgerblue2')
color = color_inactive
active = False
userVelocity = ''
done = False

####################### END TEXT SETUP #######################

####################### DRIVER LOOP #######################

# game driver loop (rounds loop within)
while True:

    for event in pg.event.get(): # grab events 
        if event.type == pg.QUIT: 
            pg.quit()
            exit()
        # handler for clicking
        if event.type == pg.MOUSEBUTTONDOWN:
            # handler for clicking on velocity input
            if velocityRect.collidepoint(event.pos):
                active = not active
            else:
                active = False
            color = color_active if active else color_inactive
        # handler for saving user input to screen
        if event.type == pg.KEYDOWN:
            # handler for velocity input rendering
            if active:
                if event.key == pg.K_RETURN:
                    print(userVelocity)
                    userVelocity = ''
                elif event.key == pg.K_BACKSPACE:
                    userVelocity = userVelocity[:-1]
                else:
                    userVelocity += event.unicode

    screen.blit(sky, (0, 0))
    screen.blit(water, (0, 500))
    screen.blit(boat, (700, 440))
    screen.blit(cannon, (780, 435))
    screen.blit(sailor, (760, 460))
    screen.blit(control_panel, cpRect)
    screen.blit(massText, massRect)
    screen.blit(boatText, bRect)
    screen.blit(targetText, tRect)

    # velocity input rendering --> modify location & color & size
    velocitySurface = smallFont.render(userVelocity, True, color)
    velocityRect.w = max(200, velocitySurface.get_width() + 10)
    screen.blit(velocitySurface, (velocityRect.x + 5, velocityRect.y + 5))
    pg.draw.rect(screen, color, velocityRect, 2)

    # update
    pg.display.update()
    clock.tick(60)

####################### END DRIVER LOOP #######################