# Huan Bui
# CS152 Project 11 - Project Gravity
# Dcember 8, 2017
#
# gravity.py
#
#
#

import graphics as gr
import physics_objects as pho
import rot
import collision
import math

def buildUI():
    pass
	
def buildDefault(win):

    sun = pho.Ball(win, 400e9, 350e9, 1.989e30, 10e9)
    sun.setColor('yellow')

    earth = pho.Ball(win, 552e9, 350e9, 5.972e24, 3.8e9)
    earth.setColor('blue')
    
    venus = pho.Ball(win, 508.2e9, 350e9, 4.867e24, 3.78e9)
    venus.setColor('orange')
    
    mercury = pho.Ball(win, 470e9, 350e9, 0.3285e24, 3.387e9)
    mercury.setColor(gr.color_rgb(209, 203, 198))
    
    mars = pho.Ball(win, 299.23e9 + 400e9, 350e9, 0.639e24, 3.53e9)
    mars.setColor(gr.color_rgb(226, 113, 27))
    
    jupiter = pho.Ball(win, 816.62e9 + 400e9, 350e9, 1898.19e24, 4.854e9)
    jupiter.setColor(gr.color_rgb(234, 179, 91))
    
    saturn = pho.Ball(win, 1514.50e9 + 400e9, 350e9, 568.34e24, 4.780e9)
    saturn.setColor(gr.color_rgb(224, 195, 148))
    
    uranus = pho.Ball(win, 3003.62e9 + 400e9, 350e9, 86.813e24, 4.4075e9)
    uranus.setColor(gr.color_rgb(120, 219, 237))
    
    neptune = pho.Ball(win, 4545.67e9 + 400e9, 350e9, 102.413e24, 4.3938e9)
    neptune.setColor(gr.color_rgb(27, 50, 226))

    earth.setVelocity([0, 29.29e3])
    sun.setVelocity([0, 0])
    venus.setVelocity([0, 35e3])
    mercury.setVelocity([0, 46e3])
    mars.setVelocity([0, 21.97e3])
    jupiter.setVelocity([0, 12.44e3])
    saturn.setVelocity([0, 9.09e3])
    uranus.setVelocity([0, 6.49e3])
    neptune.setVelocity([0, 5.37e3])
    
    bodies = [sun, earth, venus, mercury, mars, jupiter, saturn, uranus, neptune]
    
    #bodies = [sun, earth]
    
    for body in bodies:
    	body.draw()
    
    return bodies
    
def buildMass(win, m = [400, 350], type=None):

    mass = pho.Ball(win, m[0]*10e8, m[1]*10e8, 2e30, 10e9)
    mass.setColor('yellow')
    mass.draw()
    '''
    if m != [400, 350]:
    	mass.setVelocity([0, 0])
    	mass.setMass(0.001e30)
    '''
    if type == 'Velocity':
    	mass.undraw()
    	mass = None
    	mass = pho.Ball(win, m[0]*10e8, m[1]*10e8, 2e30, 5e9)
    	mass.setColor('red')
    	mass.setPointer('Velocity')
    	mass.draw()
    return mass
    
def massiveBody(bodies):
	maxWeight = 0
	maxWeightIDX = -1
	minWeight = 10e50
	#minWeightIDX = -1
	for i in range(len(bodies)):
		if bodies[i].getMass() > maxWeight:
			maxWeight = bodies[i].getMass()
			maxWeightIDX = i
			
		if bodies[i].getMass() < minWeight:
			minWeight = bodies[i].getMass()
			#minWeightIDX = i
			
	if maxWeight/minWeight > 10e4:
		return [True, maxWeightIDX]
	return [False, -1]

def planetAction(bodies, dt):
	l = massiveBody(bodies)
	if l[0] == False: # if there's no extremely massive body
		for i in range(len(bodies)):
			for k in range(len(bodies)):
				if k != i:
					s = bodies[i].attract(bodies[k])
					#bodies[i].update(dt)
					bodies[k].update(dt)
			
					if s == 'Supernova':
						return s
					
	else: # if there's a very massive body... this ignores the movement of the massive body
		for i in range(1, len(bodies)):
			if l[1] != i:
				s = bodies[l[1]].attract(bodies[i])
				
				if s == "Supernova":
					return s
					
		for i in range(len(bodies)):
			bodies[i].update(dt)

#     for i in range(1,len(bodies)):
#         s = bodies[0].attract(bodies[i])
#         
#         if s == 'Supernova':
#             return s
#                     
#     for i in range(len(bodies)):
#         bodies[i].update(dt)
        

def getMouseLocation(m, win):
	if m == None:
		return
	return [m.getX(), win.getHeight() - m.getY()]
	
def buttonClicked(button, m, scale):
	tlbr = tlbrButton(button, scale)
	tl = tlbr[0]
	br = tlbr[1]
	
	if m == None:
		return 
		
	elif tl[0] <= m[0] <= br[0] and tl[1] <= m[1] <= br[1]:
		return True
	return False
	
def tlbrButton(button, scale):

	pos = button.getPosition()
	width = button.getWidth()
	height = button.getHeight()
	
	tlbr = [[(pos[0] - width/2)*scale, (pos[1] - height/2)*scale],
		[(pos[0] + width/2)*scale, (pos[1] + height/2)*scale]]
			
	return tlbr

def textButton(win, x,y, text):
    message = gr.Text(gr.Point(x,win.getHeight()-y), text)
    message.setFace("courier")
    message.setSize(15)
    message.setStyle('bold')
    message.setTextColor('blue')

    return message
	
def buildButtons(win, scale):

    # help button

    button3 = pho.RotatingBlock(win, 850e9, 670e9, 30e9, 30e9)
    button3_text = textButton(win, 850, 670, "+")
    
    button4 = pho.RotatingBlock(win, 850e9, 630e9, 30e9, 30e9)
    button4_text = textButton(win, 850, 630, "-")
    
    button5 = pho.RotatingBlock(win, 850e9, 590e9, 50e9, 30e9)
    button5_text = textButton(win, 850, 590, ">>")

    button6 = pho.RotatingBlock(win, 850e9, 550e9, 50e9, 30e9)
    button6_text = textButton(win, 850, 550, "<<")

    button9 = pho.RotatingBlock(win, 850e9, 510e9, 80e9, 30e9)
    button9_text = textButton(win, 850, 510, "Clear")

    button10 = pho.RotatingBlock(win, 850e9, 470e9, 80e9, 30e9)
    button10_text = textButton(win, 850, 470, "Reset")

    button1 = pho.RotatingBlock(win, 850e9, 145e9, 80e9, 30e9)
    button1_text = textButton(win, 850, 145, "Start!")
    
    button2 = pho.RotatingBlock(win, 850e9, 105e9, 80e9, 30e9)
    button2_text = textButton(win, 850, 105, "Pause")
    
    button7 = pho.RotatingBlock(win, 850e9, 65e9, 80e9, 30e9)
    button7_text = textButton(win, 850, 65, "Help?")

    button8 = pho.RotatingBlock(win, 850e9, 25e9, 80e9, 30e9)
    button8_text = textButton(win, 850, 25, "Exit")
    
    button11 = pho.RotatingBlock(win, 850e9, 415e9, 80e9, 60e9)
    button11_text = textButton(win, 850, 415, "Free\nPlay")

    # buttonList and # button_textList
    buttonList = [button1, button2, button3, button4, button5, button6,
                  button7, button8, button9, button10, button11]
    button_textList = [button1_text, button2_text, button3_text, button4_text,
                       button5_text, button6_text, button7_text, button8_text,
                       button9_text, button10_text, button11_text]
    
    # draw button and Texts in window
    for i in range(len(buttonList)):
        buttonList[i].draw()
        button_textList[i].draw(win)

    return buttonList
	
def witchButton(m, buttonList, scale):
	for i in range(len(buttonList)):
		if buttonClicked(buttonList[i], m, scale):
			return i+1

def displayHelp():
    winHelp = gr.GraphWin("Help", 400, 400, False)
    winHelp.setBackground('gray')
    winHelp.setCoords(0,0,400,400)

    textHelp = 'by Huan Bui\nWelcome to Gravity Simulator!\nInstructions:\nPause/Start - Pause/Unpause\nClear to clear scene\nExit - Quit\n+/- to Zoom In/Out\n>>/<< to Speed Up/Slow Down\nReset to Restart Simulation\nFree Play to Freely play with Gravity!'
                
    message = gr.Text(gr.Point(200,200), textHelp)
    message.setFace("courier")
    message.setSize(12)
    message.setStyle('italic')
    message.setTextColor('yellow')
    message.draw(winHelp)

def main():
    win = gr.GraphWin("2-D Gravity Simulator by Huan Bui", 900, 700, False)
    win.setBackground('black')
    scale = 1e-9
    
    textHelp = 'Welcome to 2-D Gravity Simulator!\n\nExplore our Home - the Solar System\n\n Or Play with The Law of Gravitation in Free Play!\n\nClick Anywhere to Begin Your Journey...'
                
    message = gr.Text(gr.Point(450,350), textHelp)
    message.setFace("courier")
    message.setSize(20)
    message.setStyle('italic')
    message.setTextColor('yellow')
    message.draw(win)
    
    win.getMouse()
    message.undraw()
    message = None
    
    # build buttons
    buttonList = buildButtons(win, scale)
    
    # build the default celestial bodies!
    bodies = buildDefault(win)    
   
    #dt = 3600 only use this for Mac
    dt = 500
    
    # checks for initiation
    entry_buttonNum = 0
    
    # freePlay mode is not activated yet
    freePlay = False
    
    while entry_buttonNum != 1:
        mouse = win.getMouse()
        m = getMouseLocation(mouse, win)
        entry_buttonNum = witchButton(m, buttonList, scale)
        if entry_buttonNum == 7:
            displayHelp()
        if entry_buttonNum == 8:
            exit()
            
    # run mode        
    while True:
        # check for entries
        mouse = win.checkMouse()
        m = getMouseLocation(mouse, win)
        s = win.checkKey()
        
        #print(bodies)
        
        buttonNum = witchButton(m, buttonList, 1e-9)
        
        #### BUTTON CONTROL ####
   
        if entry_buttonNum == 1 or buttonNum == 1: # start running
            
            s = planetAction(bodies, dt)
            
            if s == 'Supernova':
            	textHelp = 'SUPERNOVA!'
                
            	message = gr.Text(gr.Point(450,350), textHelp)
            	message.setFace("courier")
            	message.setSize(30)
            	message.setStyle('italic')
            	message.setTextColor('yellow')
            	message.draw(win)
            	
            	for body in bodies:
            		body.undraw()
            		
            	bodies = []
            	
            	win.getMouse()
            	message.undraw()
            	message = None
            	

        if buttonNum == 2: #pause
            mouse = win.getMouse()
            m = getMouseLocation(mouse, win)
            buttonNum = witchButton(m, buttonList, scale)
        
        if buttonNum == 3:
            scale /= 2
            for body in bodies:
                body.zoomIn(scale)
                         
        if buttonNum == 4:
            scale *= 2
            for body in bodies:
                body.zoomOut(scale)
        
        if buttonNum == 5: # >>
            dt += 1000

        if buttonNum == 6: # <<
            dt -= 1000

        if buttonNum == 7: # help
            displayHelp()

        if buttonNum == 8: # exit
            exit()
    
        if buttonNum == 9: #clear
            freePlay = False
            for i in range(len(bodies)):
                bodies[i].undraw()
            bodies = bodies[0:1]
            
            # get rid of free play 
            buttonList[11].undraw()
            buttonList = buttonList[0:11]
            
        if buttonNum == 10: # reset
            freePlay = False
            win.close()
            main()
            
            
        # free play mode   
        if buttonNum == 11:
            
            freePlay = True
            
            for i in range(len(bodies)): #clear space first
                bodies[i].undraw()
            bodies = []
            
            # button 12 "done"
            button12 = pho.RotatingBlock(win, 850e9, 360e9, 80e9, 30e9)
            button12_text = textButton(win, 850, 360, "Done!")
            button12.draw()
            button12_text.draw(win)
            buttonList.append(button12)
            
            # generate instructions!
            textHelp = 'Click around to add masses!\nClick "Done!" when you finish adding masses!'
            message = gr.Text(gr.Point(450,350), textHelp)
            message.setFace("courier")
            message.setSize(20)
            message.setStyle('italic')
            message.setTextColor('yellow')
            message.draw(win)
            
            # How many times the message appears...
            count = 0
            
            while True: # adding mass process
                m = getMouseLocation(win.checkMouse(), win)
                buttonNum = witchButton(m, buttonList, 1e-9)

                if buttonNum == 12:
                    message.undraw()
                    for body in bodies:
                    	if body.getPointer() == "Velocity":
                    		body.undraw()
                    		bodies.remove(body) # getting rid of all the Velo pointers
                    
                    break
                elif m != None:
                    message.undraw()
                    bodies.append(buildMass(win,m))
                    
                    textHelp = 'Click anywhere to set velocity'
                    message = gr.Text(gr.Point(450,350), textHelp)
                    message.setFace("courier")
                    message.setSize(20)
                    message.setStyle('italic')
                    message.setTextColor('yellow')
                    
                    if count <= 0:
                    	message.draw(win)
                    
                    v = getMouseLocation(win.getMouse(), win)
                    p = bodies[-1].getPosition()
                    
                    # this scaling is optimized for Windows
                    newV_x = (v[0]/scale - p[0])*10e-7
                    newV_y = (v[1]/scale - p[1])*10e-7
                    
                    bodies[-1].setVelocity([newV_x,newV_y])
                    
                    bodies.append(buildMass(win, v, 'Velocity'))
                    
                    message.undraw()
                    count += 1
                    
                
        win.update()    

if __name__ == "__main__":
    main()
