# Huan Bui
# November 7, 2017
# CS152 Project 8: Physics!
#
# File name:
# physics_objects.py
#
#
#
#
#
#


import graphics as gr
import random

class Ball:
	
	def __init__(self, win, color, position = [0,0]):
                self.color = color
                self.mass = 1
                self.radius = 0.15
                self.pos = position[:]
                self.vel = [0,0]
                self.acc = [0,0]
                self.force = [0,0]
                self.win = win
                self.scale = 10
                self.vis = [ gr.Circle( gr.Point(self.pos[0]*self.scale, win.getHeight()-self.pos[1]*self.scale), self.radius * self.scale ) ]
		
		
	def draw(self):
		'''
			takes in self
			for every part of the object
			draw in self.win
		'''
		for item in self.vis:
			item.draw(self.win)
			#item.setFill("blue")
			item.setFill(self.color)
			#item.setFill(random.choice(["red","blue","green"]))
			
	def getPosition(self):
		return tuple(self.pos)
	
	def setPosition(self, p):
		self.pos[0] = p[0]
		self.pos[1] = p[1]
		
		for item in self.vis:
			c = item.getCenter()
			dx = self.scale*self.pos[0] - c.getX()
			dy = self.win.getHeight() - self.scale*self.pos[1] - c.getY()
			item.move(dx,dy)

	def getCenter(self):
                return (self.pos[0]*self.scale, self.win.getHeight()-self.pos[1]*self.scale)
	
	def getRadius(self):
		return self.radius

	def setRadius(self, r):
		self.radius = r
	
	def getVelocity(self):
		return tuple(self.vel)
	
	def setVelocity(self, v):
		self.vel[0] = v[0]
		self.vel[1] = v[1]
	
	def getAcceleration(self):
		return tuple(self.acc)
	
	def setAcceleration(self, a):
		self.acc[0] = a[0]
		self.acc[1] = a[1]
	
	def getForce(self):
		return tuple(self.force)
	
	def setForce(self, f):
		self.force[0] = f[0]
		self.force[1] = f[1]
	
	def getMass(self):
		return self.mass
	
	def setMass(self, m):
		self.mass = m
		
		
	def update(self, dt):
                # takes in dt, modifies velocities
		self.pos[0] += self.vel[0]*dt
		self.pos[1] += self.vel[1]*dt
		
		dx = self.vel[0]*dt*self.scale
		dy = -self.vel[1]*dt*self.scale
		
		for item in self.vis:
			item.move(dx,dy)
			
		self.vel[0] += self.acc[0]*dt
		self.vel[1] += self.acc[1]*dt
		
		self.vel[0] += dt*self.force[0]/self.mass
		self.vel[1] += dt*self.force[1]/self.mass
		
		#self.vel[0] *= 0.998
		#self.vel[0] *= 0.998

	def collision(self, newBall):
                # takes in newBall
                # returns True if there's a collision
                # False otherwise
		posNew = newBall.getPosition()
		posCur = self.getPosition()
		rad = self.getRadius()
		
		material = 2*rad
		
		if abs((posCur[0]-posNew[0])**2 + (posCur[1] - posNew[1])**2) <= material**2:
			return True
			
		return False
		
		
class Floor:

	def __init__(self, win, x0, y0, length, thickness):
		self.pos = [x0, y0]
		self.length = length
		self.thickness = thickness
		self.win = win
		self.scale = 10
		self.vis = [ gr.Rectangle(gr.Point(x0*self.scale, self.win.getHeight()-(y0 + thickness/2.0)*self.scale), gr.Point((x0+length)*self.scale, self.win.getHeight()-(y0 - thickness/2)*self.scale)) ]
		
	def draw(self):
		'''
			takes in self
			for every part of the object
			draw in self.win
		'''
		for item in self.vis:
			item.draw(self.win)
			item.setFill("black")
			
	def collision(self, ball):
		# assume: the balls will not be moving fast enough to 
		# zip thru the floor in a single time step
		
		'''returns true if there is a collision
		false otherwise
		'''
		
		posBall = ball.getPosition()
		rad = ball.getRadius()
		
		material = self.thickness/2 + rad
		
		if abs(posBall[1] - self.pos[1]) <= material:
			return True
			
		return False

class Wall:
	def __init__(self, win, x0, y0, height, thickness):
                self.pos = [x0, y0]
                self.height = height
                self.thickness = thickness
                self.win = win
                self.scale = 10
                self.vis = [ gr.Rectangle(gr.Point((x0-thickness/2)*self.scale, self.scale*y0), gr.Point((x0+thickness/2)*self.scale, (y0 + height)*self.scale)) ]

	def draw(self):
		'''
			takes in self
			for every part of the object
			draw in self.win
		'''
		for item in self.vis:
			item.draw(self.win)
			item.setFill("black")

	def collision(self, ball):
		# assume: the balls will not be moving fast enough to 
		# zip thru the floor in a single time step
		
		'''returns true if there is a collision
		false otherwise
		'''
		
		posBall = ball.getPosition()
		rad = ball.getRadius()
		
		material = self.thickness/2 + rad

		if posBall[1] < self.win.getHeight()/self.scale - self.height:
                        return False
                
		if abs(posBall[0] - self.pos[0]) <= material:
			return True
			
		return False
		
	
	
	
	
	
	
	
	
	
	
		
	
	
	
	
		
