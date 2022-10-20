# Huan Bui
# Sept 17, 2017
# CS152 Project 2
#
# sunny.py
# Reads the stream of PAR data and classifies each value as either a cloudy day or a sunny day
#
# Examples Unix command for running the file
# grep '[567]/[[:digit:]]\+/16' MLRC_19.csv | grep 12:00 | cut -d ',' -f 8 | py sunny.py (Win)
# grep '[567]/[[:digit:]]\+/16' MLRC_19.csv | grep 12:00 | cut -d ',' -f 8 | python3 sunny.py (Mac)

import sys

def main(stdin):
    '''
        takes parameter stdin (from data), prints number of sunny days (int),
        average PAR of sunny days (floats), number of cloudy days (int), and average PAR of cloudy days (float)
    '''
    
    # assign to nSun the value 0
    nSun = 0
    # assign to sumSun the value 0
    sumSun = 0.0
    # assign to nCloud the value 0
    nCloud = 0
    # assign to sumCloud the value 0
    sumCloud = 0.0

    # assign to buf the result of calling readline using the stdin parameter
    buf = stdin.readline()
    
    while buf.strip() != '':
        # assign to par the result of casting buf to a float
        par = float(buf)
        # if the par value is greater than 800
            # increment nSun by 1
            # increment sumSun by the value of par
        if par > 800:
            nSun = nSun + 1
            sumSun = sumSun + par
        # else
            # increment nCloud by 1
            # increment sumCloud by the value of par
        else:
            nCloud = nCloud + 1
            sumCloud = sumCloud + 1
        # assign to buf the result of calling readline using the stdin parameter
        buf = stdin.readline()

    # print out the number of sunny days and the average par of sunny days
    print("Number of sunny days:", nSun)
    print("Average PAR of sunny days:", sumSun/nSun)
    # print out the number of cloudy days and the average par of cloudy days
    print("Number of cloudy days:", nCloud)
    print("Average PAR of cloudy days:", sumCloud/nCloud)

if __name__ == "__main__":
    main(sys.stdin)
