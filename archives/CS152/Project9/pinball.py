# Huan Bui
# CS152
# Project 9
#
# pinball.py
#

import graphics as gr
import time
import random
import physics_objects as pho
import math
import collision

# build the obstacle course
#def buildGame(win, x0, y0, width, height):
def buildGame(win, width, length):
    thickness = 5
    scale = 10
    floor = pho.Floor(win, 0, thickness/2, width, thickness)
    ceiling = pho.Floor(win, 0, win.getHeight()/scale - thickness/2, width, thickness)
    wallL = pho.Wall(win, thickness/2, 0, length, thickness)
    wallR = pho.Wall(win, win.getWidth()/scale - thickness/2, 0, length, thickness)
    block = pho.Block(win, 35,25,5,5)
    l0 = pho.L(win, 10, 30, 5,5)
    l1 = pho.L(win, 20, 15, 3,3)
    l2 = pho.L(win, 10, 60, 7,7)
    u1 = pho.U(win, 30, 50, 4, 4)
    obs_list = [floor, ceiling, wallL, wallR, block, l0, l1, l2, u1]

    for item in obs_list:
        item.setElasticity(1.1)
        item.draw()
    return obs_list

# launch the ball into the scene
def launch( ball, x0, y0, dx, dy, forceMag ):
    
    scale = 10
    d = math.sqrt(dx*dx + dy*dy)
    dx /= d
    dy /= d
    
    fx = dx * forceMag
    fy = dy * forceMag
    
    ball.setElasticity( 0.9 )
    ball.setPosition( (x0, y0) )
    ball.setForce( (fx, fy) )
    
    for i in range(5):
        ball.update(0.02)
    
    ball.setForce( (0., 0.) )
    ball.setAcceleration( (0., -0.) )

# main code
def main():
    scale = 10
    win = gr.GraphWin("pinball", 500, 700, False )
    obstacles = buildGame(win, win.getWidth(), win.getHeight())
    ball1 = pho.Ball(win, 25,25,1,1)
    ball2 = pho.Ball(win, 30,30,1,1)
    ball1.setVelocity([random.randint(-10,10),random.randint(-10,10)])
    ball2.setVelocity([random.randint(-10,10),random.randint(-10,10)])
    ball1.draw()
    ball2.draw()

    win.getMouse()
    launch(ball1, 25, 25, 0.001, 0.001, 10)
    launch(ball2, 30, 30, 0.01, 0.01, 20)
    
    listBall = [ball1, ball2]

    dt = 0.01
    frame = 0
    while win.checkMouse() == None:
        collided = False
        for i in range(len(listBall)):
            for item in obstacles:
                if collision.collision(listBall[i], item, dt) == True or collision.collision(listBall[i], listBall[1-i], dt) == True:
                    collided = True
            if collided == False:
                listBall[i].update(dt)
            if frame%10 == 0:
                win.update()
                frame+=1
        p1 = ball1.getPosition()
        if p1[0] < 0 or p1[0]*scale > win.getWidth() or p1[1] < 0 or p1[1]*scale > win.getHeight():
            launch(ball1, 25, 25, 5, 5, 10000)
        p2 = ball2.getPosition()
        if p2[0] < 0 or p2[0]*scale > win.getWidth() or p2[1] < 0 or p2[1]*scale > win.getHeight():
            launch(ball2, 25, 25, 5, 5, 10000)
    win.getMouse()
    win.close()

# wait for a mouse click, then close the window

if __name__ == "__main__":
    main()
