# Huan Bui 
# CS152 Project 8: Physics!
# November 7, 2017
#
# file name:
# bucket.py
#
# Run command:
# py bucket.py <numBall>
#
#
#
#
import sys
import graphics as gr
import physics_objects as pho
import random
import time
import transform
import math

class Bucket:
	def __init__(self, win, thickness, numBall):
            self.win = win
            self.thickness = thickness
            self.scale = 10
            self.floor = pho.Floor(win, 0, thickness/2, win.getWidth()/self.scale, thickness)
            self.ceiling = pho.Floor(win, 0, win.getHeight()/self.scale - thickness/2, win.getWidth()/self.scale, thickness)    
            self.wallL = pho.Wall(win, thickness/2, 0, win.getHeight()/self.scale, thickness)
            self.wallM = pho.Wall(win, win.getWidth()/(2*self.scale), thickness, 0.80*(win.getHeight()/self.scale), thickness)
            self.wallR = pho.Wall(win, win.getWidth()/self.scale-thickness/2, 0, win.getHeight()/self.scale, thickness)
            self.numBall = numBall
            #self.scale = 10
            # self.vis = [gr.Rectangle(gr.Point(0,0),gr.Point(thickness*self.scale,win.getHeight())),
                        #gr.Rectangle(gr.Point(win.getWidth()-thickness*self.scale,0), gr.Point(win.getWidth(), win.getHeight())),
                        #gr.Rectangle(gr.Point(0,win.getHeight()-thickness*self.scale), gr.Point(win.getWidth(), win.getheight()))]
            self.listBall1 = []
            self.listBall2 = []
            for i in range(numBall):
                #self.listBall.append(pho.Ball(win, [random.randint(thickness + 1,win.getWidth()/self.scale-thickness-1), random.randint(thickness+1, win.getHeight()/self.scale-thickness-1)]))
                self.listBall1.append(pho.Ball(win, "red", [random.randint((thickness + 2)//2,(win.getWidth()/self.scale-thickness-2)//2), random.randint(thickness+2+20, win.getHeight()/self.scale-thickness-2)]))
                self.listBall2.append(pho.Ball(win, "blue", [random.randint((thickness + 2 + win.getWidth()/self.scale)//2,(2*win.getWidth()/self.scale-thickness-2)//2), random.randint(thickness+2+20, win.getHeight()/self.scale-thickness-2)]))


            for ball in self.listBall1:
                ball.setVelocity([random.randint(-20, 20), random.randint(-10,10)])
                #ball.setAcceleration([0,-10])

            for ball in self.listBall2:
                ball.setVelocity([random.randint(-1, 1), random.randint(-1,1)])
                #ball.setAcceleration([0,-10])

            self.listBall = self.listBall1 + self.listBall2    
        
            self.vis = [self.wallM, self.ceiling, self.floor, self.wallL, self.wallR] + self.listBall


	def draw(self):
	    for item in self.vis:
                #continue
                item.draw()
                #self.win.update()

        #def collision(self, listBall):                        
                                     

def main(argv):
    if len(argv) > 1:
        #thickness = int(argv[1])
        numBall = int(argv[1])
    else:
        numBall = 20
        #thickness = 1
        
    lossFactorX = 1
    lossFactorY = 1
    win = gr.GraphWin("Ball", 400, 400, False)
    bucket = Bucket(win, 1, numBall)
    bucket.draw()

    #loop = 0
    #fp = open('velo.txt', 'w')
    while win.checkMouse() == None:
            #loop += 1
            time.sleep(0.005)
            for ball in bucket.listBall:
                ball.update(dt = 0.05)
                v = ball.getVelocity()
                p = ball.getPosition()
                if bucket.floor.collision(ball) == True:
                    #print('hi')
                    ball.setVelocity([v[0], -v[1]*lossFactorY])
                    while bucket.floor.collision(ball) == True:
                        ball.update(dt = 0.001)
                if bucket.ceiling.collision(ball) == True:
                    #print("hi")
                    ball.setVelocity([v[0], -v[1]*lossFactorY])
                    while bucket.ceiling.collision(ball) == True:
                        ball.update(dt = 0.001)
                if bucket.wallL.collision(ball) == True:
                    ball.setVelocity([-v[0]*lossFactorX, v[1]])
                    while bucket.wallL.collision(ball) == True:
                        ball.update(dt = 0.001)
                if bucket.wallM.collision(ball) == True:
                    ball.setVelocity([-v[0]*lossFactorX, v[1]])
                    while bucket.wallM.collision(ball) == True:
                        ball.update(dt = 0.001)
                if bucket.wallR.collision(ball) == True:
                    ball.setVelocity([-v[0]*lossFactorX, v[1]])
                    while bucket.wallR.collision(ball) == True:
                        ball.update(dt = 0.001)
                for newBall in bucket.listBall:
                    if ball != newBall:
                        if ball.collision(newBall) == True:
                            v2 = newBall.getVelocity()
                            p1 = ball.getPosition()
                            p2 = newBall.getPosition()
                            	
                            newVs = transform.transform(v[0], v[1], v2[0], v2[1], p1[0], p1[1], p2[0], p2[1])
                            ball.setVelocity(newVs[0])
                            newBall.setVelocity(newVs[1])
                            	
                            #ball.setVelocity(v2)
                            #newBall.setVelocity(v)
                            while ball.collision(newBall) == True:
                                ball.update(dt = 0.001)
                                newBall.update(dt = 0.001)
                #if p[0] < 0 or p[0] > win.getWidth()/bucket.scale - bucket.thickness or p[1] < 0 or p[1] > win.getHeight()/bucket.scale - bucket.thickness:
                        #bucket.listBall.append(pho.Ball(win, "blue", [random.randint((bucket.thickness + 2 + win.getWidth()/bucket.scale)//2,(2*win.getWidth()/bucket.scale-bucket.thickness-2)//2), random.randint(bucket.thickness+2+20, win.getHeight()/bucket.scale-bucket.thickness-2)]))
                        #bucket.listBall.remove(ball)
                        

                #velo = math.sqrt(v[0]**2 + v[1]**2)
                
                #print(velo)
                
                
                #fp.write(str(velo))
                #fp.write(',')
                #fp.write('\n')
                
                

    win.close()
	
	
if __name__ == "__main__":
    main(sys.argv)
    


    
