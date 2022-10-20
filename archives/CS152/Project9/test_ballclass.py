#Bruce Maxwell
# Fall 2015
# CS 151S Project 9
#
# ball class test

import graphics as gr
import physics_objects as pho
import collision as coll
import time

# create two balls heading towards one another

def main():
    win = gr.GraphWin( 'balls colliding', 500, 500, False )
    ball1 = pho.Ball(win,2,20)
    ball2 = pho.Ball(win,12,20)
    # set up velocity and acceleration so they collide
    ball1.setVelocity( [20, 0] )
    ball2.setVelocity( [-20, 0] )
    ball1.setAcceleration( [0, -10] )
    ball2.setAcceleration( [0, -10] )
    ball1.draw()
    ball2.draw()
    # loop for some time and check for collisions
    dt = 0.01
    for frame in range(12000):
        if not coll.collision_ball_ball( ball1, ball2, dt ):
            ball1.update(dt)
        if not coll.collision_ball_ball( ball2, ball1, dt ):
            ball2.update(dt)
        if frame % 10 == 0:
            win.update()
            time.sleep(0.5*dt)
        if win.checkMouse() != None:
            break
    win.getMouse()
    win.close()

if __name__ == "__main__":
    main() 
