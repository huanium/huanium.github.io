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
    radius = 1
    floor = pho.Floor(win, 0, thickness/2, width, thickness)
    ceiling = pho.Floor(win, 0, win.getHeight()/scale - thickness/2, width, thickness)
    wallL = pho.Wall(win, thickness/2, 0, length, thickness)
    wallR = pho.Wall(win, win.getWidth()/scale - thickness/2, 0, length, thickness)
    
    obs_list = [ceiling, wallL, wallR, floor]

    for item in obs_list:
        item.setElasticity(1.0)
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
    
    ball.setElasticity( 1.03 )
    ball.setPosition( (x0, y0) )
    ball.setForce( (fx, fy) )
    
    for i in range(5):
        ball.update(0.01)
    
    ball.setForce( (0.0, 0.0) )
    ball.setAcceleration( (0.0, 0.0) )

# main code
def main():
    scale = 10
    thickness = 5
    radius = 1
    win = gr.GraphWin("pinball", 700, 500, False )
    obstacles = buildGame(win, win.getWidth(), win.getHeight())
    ball1 = pho.Ball(win, 70,70,1,1)
    ball1.setVelocity([random.randint(0,5),0])
    ball1.draw()

    paddle1 = pho.Block(win, 10, 25, 2,10)
    paddle1.draw()

    paddle2 = pho.Block(win, 60, 25, 2, 10)
    paddle2.draw()

    paddleList = [paddle1, paddle2]
    '''
    rotating_block1 = pho.RotatingBlock(win,38,35,5,1)
    rotating_block1.draw()
    
    rotating_block2 = pho.RotatingBlock(win,12,35,5,1)
    rotating_block2.draw()

    rotating_block3 = pho.RotatingBlock(win,25,50,10,1)
    rotating_block3.draw()

    rotating_block4 = pho.RotatingBlock(win,25,50,10,1)
    rotating_block4.draw()
    
    rotating_block5 = pho.RotatingBlock(win,25,35,5,5)
    rotating_block5.draw()

    flying_square = pho.RotatingBlock(win,25,60,5,1)
    flying_square.setAnchor([25,50])
    flying_square.draw()
    '''
    start = gr.Text(gr.Point(250,25), "Click to play!")
    start.setFace("helvetica")
    start.setSize(36)
    start.setStyle("bold")
    start.setTextColor("yellow")
    start.draw(win)
    
    win.getMouse()
    
    launch(ball1, 25, 10, 0.001, 0.001, 10)
    
    #obstacles.append(rotating_block1)
    #obstacles.append(rotating_block2)
    #obstacles.append(rotating_block3)
    #obstacles.append(rotating_block4)
    #obstacles.append(rotating_block5)
    #obstacles.append(flying_square)
    obstacles.append(paddle1)
    obstacles.append(paddle2)

    
    dt = 0.005
    frame = 0
    points = 0

    message = gr.Text(gr.Point(250,350), "You Lose!")
    message.setFace("helvetica")
    message.setSize(36)
    message.setStyle("bold")
    message.setTextColor("yellow")
    
    while win.checkMouse() == None:

        # creating objects here

        start.undraw()
        #rotating_block1.rotate(-2)
        #rotating_block2.rotate(2)
        #rotating_block5.rotate(3)
        #rotating_block3.rotate(2)
        #rotating_block4.rotate(-2)
        #flying_square.rotate(1)
        collided = False
        for item in obstacles:
            if collision.collision(ball1, item, dt) == True:
                collided = True
        if collided == False:
            ball1.update(dt)
        if frame%10 == 0:
            win.update()
            frame+=1

        # Win/Lose determinator
        


        p = ball1.getPosition()
        if p[0] <= thickness + radius + 0.5:
            print("Left Loses!")
            print(points)
            message = gr.Text(gr.Point(250,350), "Right wins!")
            message.setFace("helvetica")
            message.setSize(36)
            message.setStyle("bold")
            message.setTextColor("yellow")
            message.draw(win)
            break

        elif p[0] >= 63:
            print("Right Loses!")
            print(points)
            message = gr.Text(gr.Point(250,350), "Left Wins!")
            message.setFace("helvetica")
            message.setSize(36)
            message.setStyle("bold")
            message.setTextColor("yellow")
            message.draw(win)
            break
    

        # paddle control
        
        pp1 = paddle1.getPosition()
        pp2 = paddle2.getPosition()
        
        key = win.checkKey()
        if key == "w":
            paddle1.setPosition([pp1[0], pp1[1] + 5])
            paddle1.draw()
            paddle1.update(0.01)

            
        elif key == "s":
            paddle1.setPosition([pp1[0], pp1[1] - 5])
            paddle1.draw()
            paddle1.update(0.01)

        elif key == "Down":
            paddle2.setPosition([pp2[0], pp2[1] - 5])
            paddle2.draw()
            paddle2.update(0.01)

        elif key == "d":
            paddle1.setPosition([pp1[0] + 5, pp1[1]])
            paddle1.draw()
            paddle1.update(0.01)

            
        elif key == "a":
            paddle1.setPosition([pp1[0] - 5, pp1[1]])
            paddle1.draw()
            paddle1.update(0.01)

        elif key == "Left":
            paddle2.setPosition([pp2[0] - 5, pp2[1]])
            paddle2.draw()
            paddle2.update(0.01)

        elif key == "Right":
            paddle2.setPosition([pp2[0] + 5, pp2[1]])
            paddle2.draw()
            paddle2.update(0.01)

        elif key == "Up":
            paddle2.setPosition([pp2[0], pp2[1] + 5])
            paddle2.draw()
            paddle2.update(0.01)

        

    win.getMouse()
    win.close()

if __name__ == "__main__":
    main()
