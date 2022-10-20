# Huan Bui
# CS152 Project 9
# November 14, 2017
#
# wordmap.py
#
#
#

def main():
    words = ['a', 'b', 'c', 'd', 'f', 'e']
    mapping = dict()
    for word in words:
        s = input("input here: ")
        response = str(s)
        mapping[word] = response

    for key in mapping:
        print(key, mapping[key])



main()
