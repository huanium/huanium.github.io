# Huan Bui
# CS152 Project 9
# November 14, 2017
#
# physics_objects.py
#
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
        self.scale = 10
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

    def setPosition(self, p):
        self.position[0] = p[0]
        self.position[1] = p[1]
        '''

        for item in self.vis:
            c = item.getCenter()
            dx = self.scale*self.position[0] - c.getX()
            dy = self.win.getHeight() - self.scale*self.position[1] - c.getY()
            item.move(dx,dy)

        '''
            

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
            #print("hello")
            item.draw(self.win)
            item.setFill(gr.color_rgb(random.randint(0,255),random.randint(0,255),random.randint(0,255)))

            #print('drew')
            #self.win.update()
            # item.setFill(self.color)

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
        '''
        self.velocity[0] *= 0.998
        self.velocity[1] *= 0.99
        '''
    
class Ball(Thing):
    def __init__(self, win, x0=5, y0=5, mass = 1, radius=1):
        Thing.__init__(self, win, "ball")
        #print(x0, y0)
        self.position = [x0, y0]
        self.win = win
        self.mass = mass
        self.radius = radius
        self.elasticity = 0.95
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

    def draw(self):
        for item in self.vis:
            item.draw(self.win)
            #item.setFill("yellow")

    def attract(self, otherBall):
        p1 = self.getPosition()
        p2 = otherBall.getPosition()

        G = 6.67e-3

        # distance
        d = math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)
        a_ball = [ G*otherBall.getMass()*(p2[0]-p1[0])/d**2 , G*otherBall.getMass()*(p2[1]-p1[1])/d**2 ]
        a_otherBall = [ G*self.mass*(p1[0]-p2[0])/d**2 , G*self.mass*(p1[1]-p2[1])/d**2 ]

        self.setAcceleration(a_ball)
        otherBall.setAcceleration(a_otherBall)

class Floor(Thing):
    def __init__(self, win, x0, y0, length, thickness):
        Thing.__init__(self, win, "floor")
        self.position = [x0, y0]
        self.width = length
        self.height = thickness
        self.vis = [ gr.Rectangle(gr.Point(x0*self.scale, self.win.getHeight()-(y0 + thickness/2.0)*self.scale),
                                  gr.Point((x0+length)*self.scale, self.win.getHeight()-(y0 - thickness/2)*self.scale)) ]

    def getHeight(self):
        return self.height

    def getWidth(self):
        return self.width


class Wall(Thing):
    def __init__(self, win, x0, y0, length, thickness):
        Thing.__init__(self, win, "wall")
        self.position = [x0, y0]
        self.width = thickness
        self.height = length
        self.vis = [ gr.Rectangle(gr.Point((x0-thickness/2)*self.scale, self.scale*y0),
                                  gr.Point((x0+thickness/2)*self.scale, (y0 + length)*self.scale)) ]

    def getHeight(self):
        return self.height

    def getWidth(self):
        return self.width

class Block(Thing):
    def __init__(self, win, x0, y0, length, height):
        Thing.__init__(self, win, "block")
        self.position = [x0, y0]
        self.width = length
        self.height = height
        self.drawn = False

    def getWidth(self):
        return self.width
    def getHeight(self):
        return self.height
    def render(self):
        length = self.width
        height = self.height
        win = self.win
        self.vis = [ gr.Rectangle(gr.Point((self.position[0]-length/2)*self.scale, win.getHeight() - (self.position[1] - height/2)*self.scale),
                    gr.Point((self.position[0]+length/2)*self.scale, win.getHeight() - (self.position[1] + height/2)*self.scale)) ]

    def draw(self):
        for item in self.vis:
            item.undraw()

        self.render()

        for item in self.vis:    
            item.setFill(gr.color_rgb(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
            item.draw(self.win)

    '''
    def draw(self):
		for item in self.vis:
                        item.undraw()
			
		self.render()
		
		for item in self.vis:
                        item.setFill(gr.color_rgb(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
                        item.draw(self.win)

		self.drawn = True
    '''
class L(Thing):
    def __init__(self, win, x0, y0, length, height):
        Thing.__init__(self, win, "letter")
        self.position = [x0, y0]
        self.width = length
        self.height = height
        self.l1 = Block(win, x0, y0, length, height)
        self.l2 = Block(win, x0, y0 - height, length, height)
        self.l3 = Block(win, x0, y0 - 2*height, length, height)
        self.l4 = Block(win, x0 + length, y0, length, height)
        self.l5 = Block(win, x0 + 2*length, y0, length, height)

        self.vis = [self.l1, self.l2, self.l3, self.l4, self.l5]
    
    def getWidth(self):
        return self.width
    def getHeight(self):
        return self.height
    def getVis(self):
        #print(self.vis)
        return self.vis
    def draw(self):
        for block in self.vis:
            block.draw()

class U(Thing):
    def __init__(self, win, x0, y0, length, height):
        Thing.__init__(self, win, "letter")
        self.position = [x0, y0]
        self.width = length
        self.height = height
        self.l1 = Block(win, x0, y0, length, height)
        self.l2 = Block(win, x0, y0 - height, length, height)
        self.l3 = Block(win, x0, y0 - 2*height, length, height)
        self.l4 = Block(win, x0 + length, y0, length, height)
        self.l5 = Block(win, x0 + 2*length, y0, length, height)
        self.l6 = Block(win, x0 + 3*length, y0, length, height)
        self.l7 = Block(win, x0 + 3*length, y0 - height, length, height)

        self.vis = [self.l1, self.l2, self.l3, self.l4, self.l5, self.l6, self.l7]

    def getVis(self):
    #print(self.vis)
        return self.vis
    def draw(self):
        for block in self.vis:
            block.draw()

class RotatingBlock(Thing):
	def __init__(self, win, x0, y0, width, height, Ax = 25, Ay = 25):
		Thing.__init__(self, win, "rotating block")
		self.position = [x0, y0]
		self.width = width
		self.height = height
		self.points = [[-width/2,-height/2],[width/2,-height/2],[width/2,height/2],[-width/2,height/2]]
		self.angle = 0.0
		self.rvel = 0.0
		self.anchor = [x0, y0]
		self.drawn = False
		
		
	def draw(self):
		for item in self.vis:
                        item.undraw()
			
		self.render()
		
		for item in self.vis:
                        item.setFill(gr.color_rgb(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
                        item.draw(self.win)

		self.drawn = True	
	
	
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
                
