# Huan Bui
# Sept 17, 2017
# CS152 Project 2
#
# Extension.py
# Reads through the data, extracts the values from each line
# and prints maximum gust, maximum wind, maximum par
# prints day with maximum sun
# prints day with most gust
#
# Example Unix command for running the file
# cat blend.csv | py Extension.py (Win)
# cat blend.csv | python3 Extension.py (Mac)


import sys

def main(stdin):
    '''
        takes parameter stdin (from data),
        prints maximum gust, maximum wind, maximum par (floats)
        day with maximum gust (string)
        day with maximum sun (string)
    '''

    speed = 0.0
    gust = 0.0
    percentDifference = 0.0
    maxPar = -100000.0
    maxGust = -100000.0
    maxPercentDif = -10000.0

    datetime = ''
    maxGustDay = ''
    maxParDay = ''
    
    buf = stdin.readline()

    while buf.strip() != '':
        
        words = buf.split(',')

        speed = float(words[3])
        gust = float(words[4])
        par = float(words[5])
        datetime = words[0]

        if (gust > maxGust):
            maxGust = gust
            maxGustDay = words[0]

        if (par > maxPar):
            maxPar = par
            maxParDay = words[0]
        
        if (speed != 0):
            percentDifference = 100*((gust - speed)/speed)
        '''
            print(datetime)
            print('Difference (gust - speed) = ', (gust-speed))
            print('Percent difference: ',percentDifference)
            print()
        else:
            print('Speed = 0')
        '''
        if (abs(percentDifference) > maxPercentDif):
                maxPercentDif = percentDifference
        
        buf = stdin.readline()
    print('Maximum gust is: ', maxGust)
    print('Maximum par is: ', maxPar)
    print('Maximum percent difference (magnitude): ', maxPercentDif)
    print()
    print('Day with most gust: ', maxGustDay)
    print('Day with most sun: ', maxParDay)

if __name__ == "__main__":
    main(sys.stdin)
