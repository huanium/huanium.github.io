# Huan Bui
# Sept 17, 2017
# CS152 Project 2
#
# energy.py
# Reads through the data, extracts the values from each line
# and remembers the last three wind, gust, and PAR values
# if the line is on a 15 min internal,
# then print out the average of the last three wind, gust, and PAR values
#
# Example Unix command for running the file
# grep '5/[[:digit:]]\+/16' MLRC_19.csv | cut -d ',' -f 2,4,5,8 | py energy.py (Win)
# grep '5/[[:digit:]]\+/16' MLRC_19.csv | cut -d ',' -f 2,4,5,8 | python3 energy.py (Mac)


import sys

def main(stdin):
    '''
        takes parameter stdin (from data), prints avg of last three wind (float),
        gust (float), and PAR values (float) 15 min intervals
    '''
    
    wind0 = 0.0 # assign to wind0 the value 0.0
    wind1 = 0.0 # assign to wind1 the value 0.0
    wind2 = 0.0 # assign to wind2 the value 0.0

    gust0 = 0.0 # assign to gust0 the value 0.0
    gust1 = 0.0 # assign to gust1 the value 0.0
    gust2 = 0.0 # assign to gust2 the value 0.0

    par0 = 0.0 # assign to par0 the value 0.0
    par1 = 0.0 # assign to par1 the value 0.0
    par2 = 0.0 # assign to par2 the value 0.0
    
  
    datetime = '' # assign to datetime the empty string ''
    
    buf = stdin.readline() # assign to buf the result of calling readline using the stdin parameter

    while buf.strip() != '':
    
        wind2 = wind1 # assign to wind2 the value in wind1
        wind1 = wind0 # assign to wind1 the value in wind0
        
        gust2 = gust1 # assign to gust2 the value in gust1
        gust1 = gust0 # assign to gust1 the value in gust0
        
        par2 = par1 # assign to par2 the value in par1
        par1 = par0 # assign to par1 the value in par0
        

        words = buf.split(',') # assign to words the result of calling split on the buf variable with a comma as argument

        datetime = words[0] # assign to datetime the value in words[0]
        
        wind0 = float(words[1]) # assign to wind0 the result of casting words[1] to a float        
        gust0 = float(words[2]) # assign to gust0 the result of casting words[2] to a float
        par0 = float(words[3]) # assign to par0 the result of casting words[3] to a float

        # if any of the strings ":00:", ":15:", ":30:", or ":45:" are in the datetime string
            # assign to avgwind the average of wind0, wind1, and wind2
            # assign to avggust the average of gust0, gust1, and gust2
            # assign to avgpar the average of par0, par1, and par2
            
        if (":00:" in datetime or ":15:" in datetime or ":30:" in datetime or ":45:" in datetime):
            avgwind = (wind0 + wind1 + wind2)/3
            avggust = (gust0 + gust1 + gust2)/3
            avgpar = (par0 + par1 + par2)/3
            
        # print the datetime, average wind, average gust, and average PAR separated by commas
            print(datetime, ',', avgwind, ',', avggust, ',', avgpar)
            
        # assign to buf the result of calling readline using the stdin parameter
        buf = stdin.readline()

if __name__ == "__main__":
    main(sys.stdin)
