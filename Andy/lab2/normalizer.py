import sys
import regex as re
from count import count_unigrams
from tokenizer import tokenize, tokenize2
from count_bigrams import count_bigrams
import math


def normalize(text):
    res = ''
    pattern = re.compile(r'\p{Lu}[^\.]*')
    for sentence in pattern.finditer(text):
        norm = '<s> '
        sentence = re.sub(r'\p{P}', '', sentence.group())
        sentence = re.sub('\n', '', sentence)
        norm += sentence.lower()
        norm += ' </s>\n'
        res += norm
    return res


def print_unigram(unigrams, sentence, nbr_words):
    print('Unigram model')
    print('=========================================================')
    print('wi\tC(wi)\t#words\tP(wi)')
    print('=========================================================')
    split = sentence.split()
    uni_prob = 1
    for i in range (1, len(split)):
        word = split[i]
        prob = unigrams[word] / nbr_words
        print(word, '\t', unigrams[word], '\t', nbr_words, '\t', prob)
        uni_prob *= prob
    print('=========================================================')
    print('Prob. unigrams:\t', uni_prob)
    ent = -math.log(uni_prob) / (len(split) - 1)
    print('Entropy rate: ', ent)
    perp = math.pow(2, ent)
    print('Perplexity: ', perp)


def print_bigram(unigrams, bigrams, sentence, nbr_words):
    print('Bigram model')
    print('=========================================================')
    print('wi\twi+1\tCi,i+1\tC(i)\tP(wi+1|wi)')
    split = sentence.split()
    bi_prob = 1
    for i in range (1, len(split)):
        if bigrams.get((split[i-1], split[i])) is None:
            prob = unigrams[split[i-1]] / nbr_words
            print(split[i-1], '\t', split[i], '\t', 0, '\t', unigrams[split[i-1]], '\t', '0.0 *backoff: ', prob)
            bi_prob *= prob
        else:
            cii = bigrams.get((split[i-1], split[i]))
            prob = cii / unigrams[split[i-1]]
            print(split[i-1], '\t', split[i], '\t', cii, '\t', unigrams[split[i-1]], '\t', prob)
            bi_prob *= prob
    print('=========================================================')
    print('Prob. bigrams:\t', bi_prob)
    ent = -math.log(bi_prob) / (len(split) - 1)
    print('Entropy rate: ', ent)
    perp = math.pow(2, ent)
    print('Perplexity: ', perp)

if __name__ == '__main__':
    text = sys.stdin.read()
    normalizedtext = normalize(text)
    f = open('normalize.txt', 'w')
    print(normalizedtext, file=f)
    f.close()

    tokens = tokenize2(normalizedtext)
    unigrams = count_unigrams(tokens)
    print('unigrams count: ', len(unigrams))
    bigrams = count_bigrams(tokens)
    print('bigrams count: ', len(bigrams))
    nbr_words = len(tokens)

    a = "Det var en gång en katt som hette nils."
    a_norm = normalize(a)
    print_unigram(unigrams, a_norm, nbr_words)
    print()
    print_bigram(unigrams, bigrams, a_norm, nbr_words)

