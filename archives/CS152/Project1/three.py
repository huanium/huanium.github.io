# Huan Bui
# Sept 7, 2017
# CS152_Project1

import sys #sys lets us communicate with info from terminal

print('version 6')
a = sys.stdin.readline()  #intake values
b = sys.stdin.readline()
c = sys.stdin.readline()
a = float(a)              #casts float() to a since input is of string type
b = float(b)
c = float(c)


def sum3(x,y,z):
    sum = x + y + z
    return sum

def avg(x,y,z):
    avg = (x + y + z)/3
    return avg

print('sum ', sum3(a,b,c))
print('avg ', avg(a,b,c))

#cat threenumbers.txt | py three.py
# the vertical slash == PIPE
#which sends the output of one program to the input of the next
#to change output, change the .txt file to need to change code

#change argument after -f to change depth





