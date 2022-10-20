# Huan Bui
# CS152 Project 11
# December 8, 2017
#
# physics_objects.py
# Gravity Project Edition
#

import graphics as gr
import random
import math
import collision

class Thing:
    def __init__(self, win, the_type):
        self.win = win
        self.type = the_type
        self.mass = 1
        self.radius = 1
        self.position = [10, 10]
        self.velocity = [0,0]
        self.acceleration = [0, 0]
        self.force = [0,0]
        self.elasticity = 1.0
        self.scale = 1e-9
        self.vis = []

    def getType(self):
        return self.type

    def getMass(self):
        return self.mass

    def getRadius(self):
        return self.radius

    def getPosition(self):
        return tuple(self.position)

    def getVelocity(self):
        #print(self.velocity)
        return tuple(self.velocity)

    def getAcceleration(self):
        return tuple(self.acceleration)

    def getForce(self):
        return tuple(self.force)

    def getElasticity(self):
        return self.elasticity

    def getScale(self):
        return self.scale

    def setType(self, the_type):
        self.type = the_type

    def setMass(self, m):
        self.mass = m

    def setRadius(self, r):
        self.radius = r

    def setVelocity(self, v):
        #print('v')
        self.velocity[0] = v[0]
        self.velocity[1] = v[1]

    def setAcceleration(self, a):
        self.acceleration[0] = a[0]
        self.acceleration[1] = a[1]

    def setForce(self, f):
        self.force[0] = f[0]
        self.force[1] = f[1]

    def setElasticity(self, e):
        self.elasticity = e

    def setScale(self, s):
        self.scale = s

    def undraw(self):
        for item in self.vis:
            item.undraw()

    def draw(self):
        #print(self.vis)
        self.win.setBackground('black')
        for item in self.vis:
            item.draw(self.win)
            item.setFill(gr.color_rgb(random.randint(0,255),random.randint(0,255),random.randint(0,255)))


    def update(self, dt):
        #print('u')
        self.position[0] += self.velocity[0]*dt
        self.position[1] += self.velocity[1]*dt

        dx = self.velocity[0]*dt*self.scale
        dy = -self.velocity[1]*dt*self.scale

        for item in self.vis:
            item.move(dx,dy)

        self.velocity[0] += self.acceleration[0]*dt
        self.velocity[1] += self.acceleration[1]*dt

        self.velocity[0] += dt*self.force[0]/self.mass
        self.velocity[1] += dt*self.force[1]/self.mass
    
class Ball(Thing):
    def __init__(self, win, x0=5, y0=5, mass = 1, radius=1):
        Thing.__init__(self, win, "ball")
        #print(x0, y0)
        self.position = [x0, y0]
        self.win = win
        self.color = 'white'
        self.mass = mass
        self.radius = radius
        self.elasticity = 0.95
        self.oldScale = 1e-9
        self.pointer = 'NOTVelocity'
        self.vis = [ gr.Circle( gr.Point(self.position[0]*self.scale, win.getHeight()-self.position[1]*self.scale), self.radius * self.scale ) ]

    def setPosition(self,p):
        #print('p')
        self.position[0] = p[0]
        self.position[1] = p[1]

        for item in self.vis:
            c = item.getCenter()
            dx = self.scale*self.position[0] - c.getX()
            dy = self.win.getHeight() - self.scale*self.position[1] - c.getY()
            item.move(dx,dy)
            
    def getPointer(self):
    	return self.pointer
    	
    def setPointer(self, s):
    	self.pointer = s
            
    def setMass(self,m):
    	self.mass = m

    def setColor(self, color):
        self.color = color

    def draw(self):
        for item in self.vis:
            item.draw(self.win)
            item.setFill(self.color)

    def zoomOut(self, s):
        widthWin = 1e9*(self.win.getWidth() - 100)
        heightWin = 1e9*(self.win.getHeight())
        oldScale = self.oldScale
        v = self.getVelocity()
        
        x_center = widthWin/2
        y_center = heightWin/2
        
        #self.scale = s
        self.setPosition([(self.position[0]+x_center)/(s/oldScale), (self.position[1]+y_center)/(s/oldScale)])
        self.mass /= (s/oldScale)**3
        self.setVelocity([v[0]/(s/oldScale), v[1]/(s/oldScale)])
        
        self.oldScale = s 

        
    def zoomIn(self, s):
        widthWin = 1e9*(self.win.getWidth() - 100)
        heightWin = 1e9*(self.win.getHeight())
        oldScale = self.oldScale
        v = self.getVelocity()

        
        x_center = widthWin/2
        y_center = heightWin/2
        
        #self.scale = s
        self.setPosition([self.position[0]/(s/oldScale)-x_center, self.position[1]/(s/oldScale)-y_center])
        self.mass /= (s/oldScale)**3
        self.setVelocity([v[0]/(s/oldScale), v[1]/(s/oldScale)])
        
        self.oldScale = s
         

    def attract(self, otherBall):
        p1 = self.getPosition()
        p2 = otherBall.getPosition()

        G = 6.67e-11

        # distance
        d = math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)
        
        if d < 10000000000:
        	return 'Supernova'
                
        a_ball = [ G*otherBall.getMass()*(p2[0]-p1[0])/d**3 , G*otherBall.getMass()*(p2[1]-p1[1])/d**3 ]
        a_otherBall = [ G*self.mass*(p1[0]-p2[0])/d**3 , G*self.mass*(p1[1]-p2[1])/d**3 ]

        self.setAcceleration(a_ball)
        otherBall.setAcceleration(a_otherBall)
        
class RotatingBlock(Thing):
    def __init__(self, win, x0, y0, width, height, Ax = 25, Ay = 25):
        Thing.__init__(self, win, "rotating block")
        self.position = [x0, y0]
        self.color = gr.color_rgb(196, 200, 206)
        self.width = width
        self.height = height
        self.points = [[-width/2,-height/2],[width/2,-height/2],[width/2,height/2],[-width/2,height/2]]
        self.angle = 0.0
        self.rvel = 0.0
        self.anchor = [x0, y0]
        self.drawn = False
        self.scale = 1e-9

    def setColor(self, color):
        self.color = color

    def draw(self):
        for item in self.vis:
            item.undraw()
            
        self.render()
        
        for item in self.vis:
            item.setFill(self.color)
            item.draw(self.win)

        self.drawn = True
        
    def getHeight(self):
    	return self.height
    	
    def getWidth(self):
    	return self.width
    
    def setAngle(self, a):
        self.angle = a
        
        if self.drawn == True:
            self.draw()
    
    def getAngle(self):
        return self.angle
        
    def rotate(self, angle):
        self.angle += angle
        
        if self.drawn == True:
            self.draw()
            
    def getAnchor(self):
                return self.anchor
            
    def setAnchor(self, A):
        self.anchor[0] = A[0]
        self.anchor[1] = A[1]

    def setRotVelocity(self, rvel):
                self.rvel = rvel

    def getRotVelocity(self):
                return self.rvel
            
    def render(self):
    
        theta = self.angle*math.pi/180.0
        cth = math.cos(theta)
        sth = math.sin(theta)
        pts = []
        
        for vertex in self.points:
            x = vertex[0] + self.position[0] - self.anchor[0]
            y = vertex[1] + self.position[1] - self.anchor[1]
            
            xt = x*math.cos(theta) - y*math.sin(theta)
            yt = x*math.sin(theta) + y*math.cos(theta)
            
            x = xt + self.anchor[0]
            y = yt + self.anchor[1]
            
            pts.append(gr.Point(self.scale*x , self.win.getHeight() - self.scale*y))
            
        self.vis = [ gr.Polygon(pts[0], pts[1], pts[2], pts[3]) ]

    def update(self, dt):
                da = self.rvel * dt
                if da != 0:
                        self.rotate(da)
                        Thing.update(self, dt)
                
