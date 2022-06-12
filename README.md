# Running BoatGame

To run the BoatGame, first please make sure that you have Python 2 or 
3 installed. Then, simply pull the github link, enter the "dist" directory
and run `./main`. The game takes ~10 seconds to load in because Python was not designed to be converted to executables. If you wish for it to run faster, you can run the Python script directly from base directory using `python3 main.py`. 

If you encounter any errors, you most likely simply have to change the runtime permissions on the executable, meaning you should run the command `chmod u+x main`. If other errors are experienced, please contact the developers at [dlyalin20@stuy.edu](dlyalin20@stuy.edu).

# Instructions for Playing the BoatGame

The goal of BoatGame is to move the boat, which starts centered at meter 700, a certain
target distance, displayed in the control panel as 'Target' in meters to the left of the 
boat.

The plater does this by inputting a certain start velocity, in meters per second, and angle, 
in degrees, for the cannon on the boat to shoot the cannonball at. They then hit the 'Fire!'
button, projecting the cannonball to the right and sending the boat some distance to the left.
If the boat is within 65 meters of the target, the player wins. Otherwise, they have the chance
to either 'Replay' the same level, or 'Restart' the game with new figures.

To most effectively win BoatGame, the player should rely on the underlying physics. Apart from
having access to the target distance in the control panel, the player can also find there
the mass of the boat and of the cannonball (the cannon is treated as massless). It
should be noted that, in the following calculations,the mass of the boat has the mass of cannonball
subtracted from it once the cannonball has been fired. Additionally, each pixel on the screen is treated as 
one pixel for a total of 1200 in a row.

After, the cannonball is fired, conservation of momentum is used to find the starting velocity of the
boat.

First, the cosine of the launch angle (in radians) is multipled by the input velocity to find the
starting x-velocity of the cannonball. This looks as follows:

`x_vel_ball = cosine(angle) * userVelocity`

It is important to note that the y-velocity of the ball is not accounted for, as this is not a
buoyancy simulation.

After this, the motion of the boat is updated each "round" using the following steps:
1. The x-velocity of the boat is found using conservation of momentum.
2. The drag force on the boat is found by multiplying the drag coefficient (4.7856e-02, or .5 * 997* .0003 * .4 * .8, or 1/2 * density of water * drag coefficient * area dimensions) by the square of the
boat's x-velocity.
3. The acceleration of the boat is found by dividing drag force by boat mass.
4. The boat is moved to the left by the x-velocity.
5. The x-velocity has the acceleration subtracted from it.

This loop continues until the x-velocity of the boat is less than 1 m/s, or until the boat moves off the edge of the screen.

In pseudocode, this approximately looks like:
```
x_vel_boat = (rock_mass * x_vel_ball) / boat_mass
while x_vel_boat >= 1 and xBoat > 0:
    drag = DRAG_COEFFICIENT * (boatVelocity ** 2)
    xBoat -= x_vel_boat
    dist_from_goal -= boatVelocity
    acceleration = drag / actualMass # mass of boat - mass of ball
    x_vel_boat -= acceleration
```
In addition, the BoatGame displays the center of mass (COM) of the system, and, if the user pays close attention, simulates the projectile motion of the cannonball using the kinematics equations.
