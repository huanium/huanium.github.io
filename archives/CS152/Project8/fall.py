# Huan Bui
# CS152 Project 8
# November 7, 2017
#
#
#
#
#
#
#
#
#
#

import graphics as gr
import physics_objects as pho
import time
import random

def main():
	win = gr.GraphWin("Ball", 700, 500, False)
	ball = pho.Ball(win, [10,35])
	ball.setVelocity([-10,10])
	floor = pho.Floor(win, 0, 5, 70, 5)
	wall = pho.Wall(win, 5, 0, 50, 5)
	
	
	ball.setAcceleration([0,-10])
	ball.draw()
	floor.draw()
	wall.draw()
	#time.sleep(1)
        
        
	bounces = 0
	
	while win.checkMouse() == None and bounces <= 3000:
		bounces += 1
		time.sleep(0.022)
		ball.update(dt = 0.1)
		p = ball.getPosition()
		v = ball.getVelocity()
		print(bounces)
		print("x-pos:", p[0])
		print("y-pos:", p[1])
		print("x-vel:", v[0])
		print("y-vel:", v[1])
		print(floor.collision(ball))
		print(wall.collision(ball))
		print()
		
		if p[1] < 0:
			ball.setVelocity([0,0])
			ball.setPosition([random.randint(0,50), random.randint(40,50)])
			win.update()
			time.sleep(0.075)

		if p[0] < 0:
                        ball.setVelocity([0,0])
                        ball.setPosition([random.randint(0,50), random.randint(40,50)])
                        win.update()
                        time.sleep(0.075)
                        
		if floor.collision(ball) == True:
                        v = ball.getVelocity()
                        ball.setVelocity([v[0], -v[1]*0.75])
                        while floor.collision(ball) == True:
                                ball.update(dt = 0.001)

		if wall.collision(ball) == True:
                        v = ball.getVelocity()
                        ball.setVelocity([-v[0]*0.95, v[1]])
                        while wall.collision(ball) == True:
                                ball.update(dt = 0.001)
			
			
	
	win.close()
	
if __name__ == "__main__":
    main()
    
