import sys
import pickle
import regex as re
import os


def get_files(dir, suffix):
    """
    __author__ = EDAN20
    Returns all the files in a folder ending with suffix
    :param dir:
    :param suffix:
    :return: the list of file names
    """
    files = []
    for file in os.listdir(dir):
        if file.endswith(suffix):
            files.append(file)
    return files


def index(text, dict, filename):
    regex = re.compile(r'\p{L}+')
    for match in regex.finditer(text.lower()):
        if dict.get(match.group()) is None:
            dict[match.group()] = [match.start()]
        else:
            dict[match.group()] += [match.start()]


def main(args):
    dict = {}
    for file in get_files(args, '.txt'):
        f = open(args + '/' + file).read()
        index(f, dict, file)
    for k in dict.keys():
        print(k, dict.get(k))
        # pickle.dump(dict, 'masterindex.idx', 'wb')


if __name__ == '__main__':
    main(sys.argv[1])
