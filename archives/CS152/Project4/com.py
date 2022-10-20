# Huan Bui
# Sept 27, 2017
# CS152 Lab 4

import sys

print(sys.argv)

if len(sys.argv) < 3:
	print("usage : python3 com.py <number> <number>")
	exit()

print(sys.argv[1] + sys.argv[2])

print(int(sys.argv[1]) + int(sys.argv[2]))
