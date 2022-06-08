import pygame as pg
from sys import exit

from pyparsing import White

####################### INITIAL SETUP #######################

pg.init()

# setting up the screen
WIDTH = 1200
HEIGHT = 800
CAPTION = "Super Duper Ultra Incredible Absolutely Amazing BoatGame!"
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption(CAPTION)

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

####################### DRIVER LOOP #######################

# game driver loop (rounds loop within)
while True:

    for event in pg.event.get(): # grab events 
        if event.type == pg.QUIT: 
            pg.quit()
            exit()

    # this should be within a round
    screen.blit(sky, (0, 0))
    screen.blit(water, (0, 500))
    screen.blit(boat, (700, 440))
    screen.blit(cannon, (780, 435))
    screen.blit(sailor, (760, 460))
    pg.display.update()
    clock.tick(60)

####################### END DRIVER LOOP #######################