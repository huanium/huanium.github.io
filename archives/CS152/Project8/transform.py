# Huan Bui
# CS152 Project 8
# November 7 2017
#
# file name:
# transform.py
#
#
import math

def transform(vx1, vy1, vx2, vy2, x1, x2, y1, y2):
    '''Takes in velocities and positions of glancing particles
       returns a set of new velocities 
    '''

    d = math.sqrt((x1-x2)**2 + (y1 - y2)**2)
    nx = (1/d)*(x1 - x2)
    ny = (1/d)*(y1 - y2)
    
    E = (vx1*nx + vy1*ny) - (vx2*nx + vy2*ny)
    
    vx1_new = vx1 - E*nx
    vy1_new = vy1 - E*ny
    vx2_new = vx2 + E*nx
    vy2_new = vy2 + E*ny
    
    return [[vx1_new, vy1_new], [vx2_new, vy2_new]]


    

