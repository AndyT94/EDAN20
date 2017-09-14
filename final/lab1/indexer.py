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


def cosSim(tfidf):
    sim = {}
    for file in tfidf.keys():
        for f in tfidf.keys():
            if f != file:
                sumAB = 0
                sumAA = 0
                sumBB = 0
                for word in tfidf.get(file):
                    sumAB += tfidf.get(file).get(word) * tfidf.get(f).get(word)
                    sumAA += tfidf.get(file).get(word) * tfidf.get(file).get(word)
                    sumBB += tfidf.get(f).get(word) * tfidf.get(f).get(word)
                sim[file + ' <-> ' + f] = sumAB / (math.sqrt(sumAA) * math.sqrt(sumBB))
    return sim


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


if __name__ == '__main__':
    dict = {}
    files = get_files(sys.argv[1], '.txt')
    for file in files:
        f = open(sys.argv[1] + '/' + file).read()
        index(f, dict, file)

    tfidf = calctfidf(files, dict)
    sim = cosSim(tfidf)

    maxval = max(sim.values())
    maxdocs = ''
    for k in sim.keys():
        if sim[k] == maxval:
            maxdocs += k + ' '
    print(maxdocs, maxval)
    #print(sim)
    pickle.dump(dict, open('masterindex.idx', 'wb'))
