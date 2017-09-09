import sys
import regex as re

__author__ = "Pierre Nugues"


def count_unigrams(words):
    frequency = {}
    for word in words:
        if word in frequency:
            frequency[word] += 1
        else:
            frequency[word] = 1
    return frequency


__author__ = "Pierre Nugues"


def count_bigrams(words):
    bigrams = [tuple(words[inx:inx + 2])
               for inx in range(len(words) - 1)]
    frequencies = {}
    for bigram in bigrams:
        if bigram in frequencies:
            frequencies[bigram] += 1
        else:
            frequencies[bigram] = 1
    return frequencies


def normalize(text):
    norm = ''
    pattern = re.compile(r'\p{Lu}[^\.]*')
    for sentence in pattern.finditer(text):
        norm += '<s> '
        sentence = re.sub(r'\p{P}', '', sentence.group())
        sentence = re.sub('\n', '', sentence)
        norm += sentence.lower()
        norm += ' </s>\n'
    return norm


if __name__ == '__main__':
    text = sys.stdin.read()
    normalizedtext = normalize(text)
    print(normalizedtext)
