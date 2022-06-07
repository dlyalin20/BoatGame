import pygame as pg
from sys import exit

pg.init()

WIDTH = 1200
HEIGHT = 800
CAPTION = "Super Duper Ultra Incredible Absolutely Amazing BoatGame!"
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption(CAPTION)

clock = pg.time.Clock() # we love fps

sky = pg.image.load("sky.jpeg")
skySize = (1200, 500)
sky = pg.transform.scale(sky, skySize)

boat = pg.image.load("man.png")


waterSize = (1200, 300)
waterColor = pg.Color(48, 213, 200)
water = pg.Surface(waterSize)
pg.draw.rect(water, waterColor, water.get_rect())

while True: # game driver loop (rounds should loop within)

    for event in pg.event.get(): # grab events 
        if event.type == pg.QUIT: 
            pg.quit()
            exit()

    # this should be within a round
    screen.blit(sky, (0, 0))
    screen.blit(boat, (900, 500))
    screen.blit(water, (0, 500))
    pg.display.update()
    clock.tick(60)