import sys
import pickle
import regex as re

def main(args):
    dict = {}
    regex = re.compile("[a-zA-ZåäöÅÄÖ]+")
    f = open(args).read()
    for match in regex.finditer(f.lower()):
        print(match)

    pickle.dump(dict, open(args[:-3] + "idx", "wb"))

if __name__ == '__main__':
    main("Selma/bannlyst.txt")