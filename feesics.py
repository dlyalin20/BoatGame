import sys, pygame, math
from random import seed, uniform

# pygame.init()
#
# size = width, height = 1000, 1000
# black = 0, 0, 0
#
# screen = pygame.display.set_mode(size)
#
# boat = pygame.image.load("boat.png")
# boatrect = boat.get_rect()

GRAVITY = 9.81
#1/2* density of water* drag coefficient* area dimensions
DRAG_CO = .5 * 997* .03 * .5 * .5 * .9

#counter = 1
while 1:

    seed()
    rock_mass = uniform(.45, 23)
    boat_mass = uniform(25, 32)
    goal = uniform(1, 100)

    print("Boat Mass: " + str(boat_mass))
    print("Rock Mass: " + str(rock_mass))
    print("Goal: " + str(goal))
    print("Drag Coefficient: " + str(DRAG_CO))

    angle = float(input("Input throwing angle: "))
    velocity = float(input("Input throwing velocity: "))
 # QUESTION:
    x_vel_ball = math.cos(angle) * velocity
    y_vel_ball = math.sin(angle) * velocity

    x_vel_boat = (rock_mass * x_vel_ball) / boat_mass
    # add buoyancy

    dist_from_goal = goal
    dist_from_water=1
    while x_vel_boat >= .01 and abs(dist_from_goal) > 1:

        drag =  DRAG_CO * (x_vel_boat ** 2)
        acceleration = drag / boat_mass

        dist_from_goal -= x_vel_boat

        x_vel_boat -= acceleration

    if abs(dist_from_goal) <= 1:
        print("You won! Distance from goal: " + str(dist_from_goal))
    else:
        print("You lost! Distance from goal: " + str(dist_from_goal))

    replay = input("Play again? (y/n)")

    if replay == 'n':
        break
