#Huan Bui
#Sept 6, 2017
#CS152 Project 1

print('version 1')
print('sum', 42+21+5)
print('avg', (42 + 21 + 5)/3)


print('version 2')
print('sum', 42.0 + 21.0 + 5.0)
print('avg', (42.0 + 21.0 + 5.0)/3.0)

print('version 3')
print('sum', 42 + 21 + 5)
print('avg', (42 + 21 + 5)/3.0)

print('version 4')
a = 42
b = 21
c = 5
print('sum', a + b + c) #print sum
print('avg', (a + b + c)/3.0) #print average

# note: input() returns a string of character
# --> need to convert string into num (casting)
print('version 5')
a = input('Enter first number: ')
b = input('Enter second number: ')
c = input('Enter third number: ')
a = int(a)
b = int(b)
c = int(c)
print('sum', a + b + c) #print sum
print('avg', (a + b + c)/3.0) #print average
