import sys
import pickle
import regex as re

def index(text, dict):
    regex = re.compile(r'\p{L}+')
    for match in regex.finditer(text.lower()):
        if dict.get(match.group()) == None:
            dict[match.group()] = [match.start()]
        else:
            dict[match.group()] += [match.start()]

def main(args):
    dict = {}
    f = open(args).read()
    index(f, dict)
    pickle.dump(dict, open(args[:-3] + "idx", "wb"))

if __name__ == '__main__':
    main("Selma/bannlyst.txt")