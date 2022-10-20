# Bruce A. Maxwell
# Fall 2015
# CS 151S Project 10
#
# Second Test function for the RotatingBlock class

import graphics as gr
import rot
import physics_objects as pho
import math
import time

def test():
    win = gr.GraphWin('rotator', 500, 500, False)

    block = pho.RotatingBlock(win,  25, 30, 20, 10 )
    block.draw()
    block.setAnchor( (25, 20) )
    block.setRotVelocity(45)

    dt = 0.02
    for i in range(400):
        block.update(dt)
        win.update()
        time.sleep(0.01)
            
        if win.checkMouse() != None:
            break

    win.getMouse()
    win.close()

if __name__ == "__main__":
    test()
    
