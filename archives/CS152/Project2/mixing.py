# Huan Bui
# Sept 17, 2017
# CS152 Project 2
#
# mixing.py
# computes the percent difference in temperature between 1m and 7m in May 2016
#
# Example Unix command for running the file
# grep '5/[[:digit:]]\+/2016' 3100_iSIC2016.csv | cut -d ',' -f 1,9,18 | py mixing.py (Win)
# grep '5/[[:digit:]]\+/2016' 3100_iSIC2016.csv | cut -d ',' -f 1,9,18 | python3 mixing.py (Mac)
# Redirect output to file mixing.csv
# grep '5/[[:digit:]]\+/2016' 3100_iSIC2016.csv | cut -d ',' -f 1,9,18 | py mixing.py > mixing.csv (Win)
# grep '5/[[:digit:]]\+/2016' 3100_iSIC2016.csv | cut -d ',' -f 1,9,18 | python3 mixing.py > mixing.csv (Mac)

import sys

def main(stdin):
    '''
        takes parameter stdin (from data), prints datetime (string) and
        percent difference in temperatre between 1m and 7m (May 2016)
    '''
    
    # assign to buf the result of calling readline using the stdin parameter
    buf = stdin.readline()

    while buf.strip() != '':
        # assign to words the result of calling buf.split(',')
        words = buf.split(',')
        # assign to temp1m the result of casting words[1] to a float
        temp1m = float(words[1])
        # assign to temp7m the result of casting words[2] to a float
        temp7m = float(words[2])
        # assign to change the expression (temp1m - temp7m)/temp7m
        C = ((temp1m - temp7m)/temp7m)*100
        # print out words[0] and change, separated by a comma
        print(words[0], ',', C)

        # assign to buf the result of calling readline using the stdin parameter
        buf = stdin.readline()

if __name__ == "__main__":
    main(sys.stdin)
