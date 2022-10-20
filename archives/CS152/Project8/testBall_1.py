# Bruce A. Maxwell
# Fall 2015
# CS 151S Project 8
#
# Physics simulation project
# Test file for the Ball class
#

# test the get/set methods
# test the setPosition method
#
import graphics as gr
import physics_objects as pho
import bucket
import time
import random

def main():

    # create a GraphWin
    win = gr.GraphWin( "Ball test", 750, 500, False)

    # create a default Ball object and draw it into the window
    scale = 10
    ball = pho.Ball(win)
    thickness = 5
    p = ball.getPosition()
    #floor1 = pho.Floor(win, 5, 10, 10, 5)
    #floor = pho.Floor(win, 5,50, 30,10)

    

    b = bucket.Bucket(win, 10, 5)
    #print('Position:', p[0], p[1])

    v = ball.getVelocity()
    #print ('Velocity:', v[0], v[1])

    ball.setVelocity( [10, 10] )

    v = ball.getVelocity()
    #print ('New Velocity:', v[0], v[1])

    ## add other get/set test cases here ##

    

    p = ball.getPosition()
    #print ('Position:', p[0], p[1])

    # move the ball to the center of the screen
    ball.setPosition( [25, 25] )

    p = ball.getPosition()
    #print ('New Position:', p[0], p[1])

    #print(ball.getCenter())

    #print(ball.getRadius())

    #print(floor.pos)
    #print(floor.thickness)

    #print(floor1.pos)
    #print(floor1.thickness)
    #ball.draw()
    #floor1.draw()
    #floor.draw()
    b.draw()
    #b.floor.draw()
    #win.update()

    #print(b.thickness)
    #print(b.numBall)

    #print(win.getHeight())
    #print(win.getWidth())

    # add some motion here.  Uncomment the code below to make it run
    dt = 0.1
    while win.checkMouse() == None:
         ball.update(dt)
         time.sleep(dt)
         ball.setVelocity( [random.randint(-10, 10), random.randint(-10, 10)] )
         win.update()

    win.getMouse()
    win.close()


if __name__ == "__main__":
    main()
    
    
