import sys
import regex as re
from count import count_unigrams
from tokenizer import tokenize
from count_bigrams import count_bigrams
import math


def normalize(text):
    res = []
    pattern = re.compile(r'\p{Lu}[^\.]*')
    for sentence in pattern.finditer(text):
        norm = ''
        norm += '<s> '
        sentence = re.sub(r'\p{P}', '', sentence.group())
        sentence = re.sub('\n', '', sentence)
        norm += sentence.lower()
        norm += ' </s>\n'
        res += [norm]
    return res


def print_unigram(unigrams, sentence, nbr_sentences, nbr_words):
    print('Unigram model')
    print('=========================================================')
    print('wi\tC(wi)\t#words\tP(wi)')
    print('=========================================================')
    split = sentence.split()
    uni_prob = 1
    for i in range (1, len(split) - 1):
        word = split[i]
        prob = unigrams[word] / nbr_words
        print(word, '\t', unigrams[word], '\t', nbr_words, '\t', prob)
        uni_prob *= prob
    prob = nbr_sentences / nbr_words
    print('</s>', '\t', nbr_sentences, '\t', nbr_words, '\t', prob)
    uni_prob *= prob
    print('=========================================================')
    print('Prob. unigrams:\t', uni_prob)
    ent = -math.log(uni_prob) / (len(split) - 1)
    print('Entropy rate: ', ent)
    perp = math.pow(2, ent)
    print('Perplexity: ', perp)


if __name__ == '__main__':
    text = sys.stdin.read()
    normalizedtext = normalize(text)
    f = open('normalize.txt', 'w')
    print(normalizedtext, file=f)

    words = tokenize(text.lower())
    unigrams = count_unigrams(words)
    print('unigrams count: ', len(unigrams))
    bigrams = count_bigrams(words)
    print('bigrams count: ', len(bigrams))

    nbr_words = len(words)

    a = "<s> det var en gång en katt som hette nils </s>"
    print_unigram(unigrams, a, len(normalizedtext), len(words))

