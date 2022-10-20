# Huan Bui
# Sept 20, 2017
# CS152 Project 3
#
# storedata.py
#
# Unix command to run program:
# cat 2015-08-01-dosat.csv | py storedata.py


import sys
import stats

def main(stdin):
    '''
        takes in parameter stdin from data, store every line of data (float)
        into list called mylist, returns mylist.
    '''
    
    #assign mylist the empty list []
    mylist = []

    #assign to buf the result of calling readline on stdin
    buf = stdin.readline()

    #while buf.strip is not equal to the empty string
        #append to mylist the result of casting buf to a float
        #assign to buf the result of calling readline on stdin

    while buf.strip() != '':
        mylist.append(float(buf))
        buf = stdin.readline()

    print(mylist)
    #return mylist

    mean = stats.mean(mylist)
    stdev = stats.stdev(mylist)

    print()
    print('Mean: ', mean)
    print('Stdev: ', stdev)

if __name__ == "__main__":
    main(sys.stdin)
