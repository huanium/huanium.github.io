# Huan Bui
# Sept 8, 2017
# CS152_Project1

import sys

sum = 0.0
count = 0.0
nextval = sys.stdin.readline()
max = 0.0
min = 100000.0
sum_of_squares = 0.0 #initialize sum of squares

while nextval.strip() != '':
    sum = sum + float(nextval)
    sum_of_squares = sum_of_squares + pow(float(nextval),2) #increment 
    count = count + 1

    if float(nextval) > max:
        max = float(nextval)

    if float(nextval) < min:
        min = float(nextval)
    
    nextval = sys.stdin.readline()

stdev = pow((sum_of_squares - (1/count)*pow(sum,2))/(count - 1),0.5) #stdev.s

print('Count: ', count)
print('Average: ', sum/count)
print('Maximum Temp: ', max)
print('Minimum Temp: ', min)
print('Standard deviation of sample: ', stdev)
