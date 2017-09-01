import sys
import pickle
import regex as re
import os
import math


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


def getNbrWords(files, dict):
    docWords = {}
    for file in files:
        nbrWords = 0
        for word in dict:
            i = dict.get(word)
            if i.get(file) is not None:
                nbrWords += len(i.get(file))
        docWords[file] = nbrWords
    return docWords

def calctfidf(files, dict):
    docWords = getNbrWords(files, dict)
    tfidf = {}
    for file in files:
        tfidf[file] = {}

    for word in dict.keys():
        for file in files:
            if dict.get(word).get(file) is None:
                tfidf[file][word] = 0.0
            else:
                tf = len(dict.get(word).get(file)) / docWords.get(file)
                idf = math.log10(len(files) / len(dict.get(word)))
                tfidf[file][word] = tf * idf
    return tfidf


def main(args):
    dict = {}
    files = get_files('Selma', '.txt')
    for file in files:
        f = open('Selma' + '/' + file).read()
        index(f, dict, file)

    tfidf = calctfidf(files, dict)

    pickle.dump(dict, open('masterindex.idx', 'wb'))


if __name__ == '__main__':
    main(sys.argv[1])
