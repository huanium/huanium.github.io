'''
    	# rotational transformation
    	# to center-of-mass frame:
	
    	theta = 0
    	#theta = math.atan((vy1 - vy2)/(vx1-vx2))
    	theta = math.atan((vy1 - vy2)/(vx1-vx2))
    	print(theta)
    	c_theta = math.cos(theta)
    	s_theta = math.sin(theta)
	
    	# calculate beta (deflection angle in COM frame)
    	# transform into COM:
    	X1 = x1*math.cos(theta) - y1*math.sin(theta)
    	Y1 = x1*math.sin(theta) + y1*math.cos(theta)

    	X2 = x2*math.cos(theta) - y2*math.sin(theta)
    	Y2 = x2*math.sin(theta) + y2*math.cos(theta)
    
    	X1 = 0
    	Y1 = 0
    
    	X2 = -math.sqrt((x1-x2)**2 + (y1-y2)**2)
    	y2 = 0

    	#beta = math.atan(abs((Y1-Y2)/(X1-X2)))
    	beta = theta

    	alpha = math.pi/2 - beta

    	# calculate relative velocity
    	V1 = math.sqrt(vx1**2 + vy1**2)
    	V2 = math.sqrt(vx2**2 + vy2**2)

    	# in COM:
    	VX = math.sqrt((vx1-vx2)**2 + (vy1 - vy2)**2)
    	VY = 0

    	# calculate A(1) and B(2) in COM frame:
    	# A (object 1)
    	vxa = VX*(math.cos(math.pi/2 - beta))**2
    	vya = VX*(math.sin(math.pi - 2*beta))*0.5

    	# B (object 2)
    	vxb = VX*(math.cos(beta))**2
    	vyb = -VX*(math.sin(2*beta))*0.5

    	# transforming A B back to original coordinates:

    	# A:
    	va_x = vxa*c_theta - vya*s_theta
    	va_y = vxa*s_theta + vya*c_theta

    	# B:
    	vb_x = vxb*c_theta - vyb*s_theta
    	vb_y = vxb*s_theta + vyb*c_theta

    	return [[va_x, va_y], [vb_x, vb_y]]
    '''
