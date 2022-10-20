# Huan Bui 
# Sept 23, 2017
# CS152 Project 3
#
# extension_5.py
#
# Extension 5: Takes in datetime and another variable
# Then calculate the max and min for the variable in that day

# Variable of choice: Wind speed (field 33)

# Unix command to run program:
# grep '/2017' 3100_iSIC.csv | cut -d ',' -f 1,33 | py extension_5.py

import sys
import stats

def main(stdin):
        buf = stdin.readline()

        words = buf.split(',')
        datetime = words[0].split(' ')
        day = datetime[0]
        lastday = datetime[0]

        total = 0.0
        count = 0

        dataList = []
        
        while buf.strip() != '':
                words = buf.split(',') # split words into datetime and data
                datetime = words[0].split(' ')  #datetime has day and time seperate by comma
                day = datetime[0]       #set str day for print
                
                if day == lastday:  # if the current day is the same as the last day
                        #print(float(words[1]))
                        dataList.append(float(words[1])) 
                        total += float(words[1])        #increment total
                        count += 1              #increment count
                        
                else:
                        print('Date: ', lastday)        #printing out before resetting
                        print('Average Wind Speed: {0:f}'.format(total/count))
                        print('Min: ', stats.min(dataList))
                        print('Max: ', stats.max(dataList))
                        print('Stdev: {0:f}'.format(stats.stdev(dataList)))
                        print()
                        

                        #print(lastday, ',', total/count) # to store in .csv
                        
                        dataList = []           # reset dataList
                        dataList.append(float(words[1])) #append first value
                        total = float(words[1]) # reset total to first value of new day
                        count = 1               # reset count to 1 (new day counted)
        
                lastday = day           # set current day becomes last day
                buf = stdin.readline()

        #print(lastday, ',', total/count) #to store in .csv
        
        print('Date: ', lastday)        # print for end case
        print('Average Wind Speed: {0:f}'.format(total/count))      # print for end case
        print('Min: ', stats.min(dataList)) # print for end case
        print('Max: ', stats.max(dataList)) # print for end case
        print('Stdev: {0:f}'.format(stats.stdev(dataList))) # print for end case

if __name__ == "__main__":
        main(sys.stdin)
