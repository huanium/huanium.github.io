# Huan Bui
# CS152 Project 10
# November 28, 2017
#
#
# input.py
#
#

import graphics as gr


def main():
	win = gr.GraphWin('clicks', 500, 500, False)
	while True:
		mouse = win.checkMouse()
		key = win.checkKey()
		if mouse != None:
			print(mouse)
			
		if key != "":
			print(key)
					
if __name__ == "__main__":
	main()