"""
CoNLL-X and CoNLL-U file readers and writers
"""
__author__ = "Pierre Nugues"

import os


def get_files(dir, suffix):
    """
    Returns all the files in a folder ending with suffix
    Recursive version
    :param dir:
    :param suffix:
    :return: the list of file names
    """
    files = []
    for file in os.listdir(dir):
        path = dir + '/' + file
        if os.path.isdir(path):
            files += get_files(path, suffix)
        elif os.path.isfile(path) and file.endswith(suffix):
            files.append(path)
    return files


def read_sentences(file):
    """
    Creates a list of sentences from the corpus
    Each sentence is a string
    :param file:
    :return:
    """
    f = open(file).read().strip()
    sentences = f.split('\n\n')
    return sentences


def split_rows(sentences, column_names):
    """
    Creates a list of sentence where each sentence is a list of lines
    Each line is a dictionary of columns
    :param sentences:
    :param column_names:
    :return:
    """
    new_sentences = []
    root_values = ['0', 'ROOT', 'ROOT', 'ROOT', 'ROOT', 'ROOT', '0', 'ROOT', '0', 'ROOT']
    start = [dict(zip(column_names, root_values))]
    for sentence in sentences:
        rows = sentence.split('\n')
        sentence = [dict(zip(column_names, row.split())) for row in rows if row[0] != '#']
        sentence = start + sentence
        new_sentences.append(sentence)
    return new_sentences


def save(file, formatted_corpus, column_names):
    f_out = open(file, 'w')
    for sentence in formatted_corpus:
        for row in sentence[1:]:
            # print(row, flush=True)
            for col in column_names[:-1]:
                if col in row:
                    f_out.write(row[col] + '\t')
                else:
                    f_out.write('_\t')
            col = column_names[-1]
            if col in row:
                f_out.write(row[col] + '\n')
            else:
                f_out.write('_\n')
        f_out.write('\n')
    f_out.close()


def count_subject_verb(corpus, SS):
    freq = {}
    for sentence in corpus:
        for word in sentence:
            if word['deprel'] == SS:
                if (word['form'].lower(), sentence[int(word['head'])]['form'].lower()) in freq:
                    freq[(word['form'].lower(), sentence[int(word['head'])]['form'].lower())] += 1
                else:
                    freq[(word['form'].lower(), sentence[int(word['head'])]['form'].lower())] = 1
    print('Total number of pairs: ', sum(freq.values()))
    sort_freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    return sort_freq


def count_subject_verb_object(corpus, SS, OO):
    freq = {}
    for sentence in corpus:
        for word in sentence:
            if word['deprel'] == OO:
                verb_index = int(word['head'])
                for w in sentence:
                    if w['deprel'] == SS and verb_index == int(w['head']):
                        if (w['form'].lower(), sentence[verb_index]['form'].lower(), word['form'].lower()) in freq:
                            freq[(w['form'].lower(), sentence[verb_index]['form'].lower(), word['form'].lower())] += 1
                        else:
                            freq[(w['form'].lower(), sentence[verb_index]['form'].lower(), word['form'].lower())] = 1
    print('Total number of triplets: ', sum(freq.values()))
    sort_freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    return sort_freq




if __name__ == '__main__':
    column_names_2006 = ['id', 'form', 'lemma', 'cpostag', 'postag', 'feats', 'head', 'deprel', 'phead', 'pdeprel']

    train_file = 'swedish_talbanken05_train.conll'
    # train_file = 'test_x'
    test_file = 'swedish_talbanken05_test.conll'

    sentences = read_sentences(train_file)
    formatted_corpus = split_rows(sentences, column_names_2006)
    # print(formatted_corpus)
    # print(train_file, len(formatted_corpus))
    # print(formatted_corpus[0])

    pairs = count_subject_verb(formatted_corpus, 'SS')
    for i in range(5):
        print(pairs[i])

    triplets = count_subject_verb_object(formatted_corpus, 'SS', 'OO')
    for i in range(5):
        print(triplets[i])

    column_names_u = ['id', 'form', 'lemma', 'upostag', 'xpostag', 'feats', 'head', 'deprel', 'deps', 'misc']

    files = get_files('ud-treebanks-conll2017', 'train.conllu')
    for train_file in files:
        print('\n', train_file)
        sentences = read_sentences(train_file)
        formatted_corpus = split_rows(sentences, column_names_u)
        # print(train_file, len(formatted_corpus))
        # print(formatted_corpus[0])

        pairs = count_subject_verb(formatted_corpus, 'nsubj')
        if len(pairs) > 5:
            for i in range(5):
                print(pairs[i])

        triplets = count_subject_verb_object(formatted_corpus, 'nsubj', 'obj')
        if len(triplets) > 5:
            for i in range(5):
                print(triplets[i])
