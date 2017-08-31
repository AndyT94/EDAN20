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
            dict[match.group()] = {}
            dict[match.group()][filename] = [match.start()]
        elif dict[match.group()].get(filename) is None:
            dict[match.group()][filename] = [match.start()]
        else:
            dict[match.group()][filename] += [match.start()]


def main(args):
    dict = {}
    for file in get_files(args, '.txt'):
        f = open(args + '/' + file).read()
        index(f, dict, file)
    pickle.dump(dict, open('masterindex.idx', 'wb'))


if __name__ == '__main__':
    main(sys.argv[1])
