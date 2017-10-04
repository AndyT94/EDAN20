"""
Gold standard parser
"""
__author__ = "Pierre Nugues"

import transition
import conll
import features
from sklearn.feature_extraction import DictVectorizer
from sklearn import linear_model
from sklearn import metrics
from sklearn.externals import joblib
import pickle


def reference(stack, queue, graph):
    """
    Gold standard parsing
    Produces a sequence of transitions from a manually-annotated corpus:
    sh, re, ra.deprel, la.deprel
    :param stack: The stack
    :param queue: The input list
    :param graph: The set of relations already parsed
    :return: the transition and the grammatical function (deprel) in the
    form of transition.deprel
    """
    # Right arc
    if stack and stack[0]['id'] == queue[0]['head']:
        # print('ra', queue[0]['deprel'], stack[0]['cpostag'], queue[0]['cpostag'])
        deprel = '.' + queue[0]['deprel']
        stack, queue, graph = transition.right_arc(stack, queue, graph)
        return stack, queue, graph, 'ra' + deprel
    # Left arc
    if stack and queue[0]['id'] == stack[0]['head']:
        # print('la', stack[0]['deprel'], stack[0]['cpostag'], queue[0]['cpostag'])
        deprel = '.' + stack[0]['deprel']
        stack, queue, graph = transition.left_arc(stack, queue, graph)
        return stack, queue, graph, 'la' + deprel
    # Reduce
    if stack and transition.can_reduce(stack, graph):
        for word in stack:
            if (word['id'] == queue[0]['head'] or
                        word['head'] == queue[0]['id']):
                # print('re', stack[0]['cpostag'], queue[0]['cpostag'])
                stack, queue, graph = transition.reduce(stack, queue, graph)
                return stack, queue, graph, 're'
    # Shift
    # print('sh', [], queue[0]['cpostag'])
    stack, queue, graph = transition.shift(stack, queue, graph)
    return stack, queue, graph, 'sh'


def parse_ml(stack, queue, graph, trans):
    if stack and trans[:2] == 'ra':
        stack, queue, graph = transition.right_arc(stack, queue, graph, trans[3:])
        return stack, queue, graph, 'ra'
    elif trans[:2] == 'la' and transition.can_leftarc(stack, graph):
        stack, queue, graph = transition.left_arc(stack, queue, graph, trans[3:])
        return stack, queue, graph, 'la'
    elif trans[:2] == 're' and transition.can_reduce(stack, graph):
        stack, queue, graph = transition.reduce(stack, queue, graph)
        return stack, queue, graph, 're'
    else:
        stack, queue, graph = transition.shift(stack, queue, graph)
        return stack, queue, graph, 'sh'

if __name__ == '__main__':
    train_file = 'swedish_talbanken05_train.conll'
    test_file = 'swedish_talbanken05_test_blind.conll'
    column_names_2006 = ['id', 'form', 'lemma', 'cpostag', 'postag', 'feats', 'head', 'deprel', 'phead', 'pdeprel']
    column_names_2006_test = ['id', 'form', 'lemma', 'cpostag', 'postag', 'feats']
    #feature_name = ['stack0_POS', 'stack0_word', 'queue0_POS', 'queue0_word', 'can-re', 'can-la']
    #feature_name = ['stack0_POS', 'stack0_word', 'queue0_POS', 'queue0_word', 'can-re', 'can-la', 'stack1_POS', 'stack1_word', 'queue1_POS', 'queue1_word']
    feature_name = ['stack0_POS', 'stack0_word', 'queue0_POS', 'queue0_word', 'can-re', 'can-la', 'stack1_POS', 'stack1_word', 'queue1_POS', 'queue1_word', 'stack_next_POS', 'stack_next_word', 'queue_next_POS', 'queue_next_word']

    sentences = conll.read_sentences(train_file)
    formatted_corpus = conll.split_rows(sentences, column_names_2006)

    sent_cnt = 0
    X_dict = list()
    y_symbols = list()
    for sentence in formatted_corpus:
        sent_cnt += 1
        if sent_cnt % 1000 == 0:
            print(sent_cnt, 'sentences on', len(formatted_corpus), flush=True)
        stack = []
        queue = list(sentence)
        graph = {}
        graph['heads'] = {}
        graph['heads']['0'] = '0'
        graph['deprels'] = {}
        graph['deprels']['0'] = 'ROOT'
        transitions = []
        while queue:
            X_dict.append(features.extract(stack, queue, graph, feature_name, sentence))
            stack, queue, graph, trans = reference(stack, queue, graph)
            transitions.append(trans)
            y_symbols.append(trans)
        stack, graph = transition.empty_stack(stack, graph)
        #print('Equal graphs:', transition.equal_graphs(sentence, graph))

        # Poorman's projectivization to have well-formed graphs.
        for word in sentence:
            word['head'] = graph['heads'][word['id']]
        # print(transitions)
        # print(graph)

    vec = DictVectorizer(sparse=True)
    X = vec.fit_transform(X_dict)

    sentences = conll.read_sentences(test_file)
    formatted_corpus = conll.split_rows(sentences, column_names_2006_test)

    sent_cnt = 0
    classifier = joblib.load('set3.pkl')
    f_out = open('out3', 'w', newline='\n')
    dict_classes = pickle.load(open('mapping3', 'rb'))
    for sentence in formatted_corpus:
        sent_cnt += 1
        if sent_cnt % 1000 == 0:
            print(sent_cnt, 'sentences on', len(formatted_corpus), flush=True)
        stack = []
        queue = list(sentence)
        graph = {}
        graph['heads'] = {}
        graph['heads']['0'] = '0'
        graph['deprels'] = {}
        graph['deprels']['0'] = 'ROOT'
        transitions = []
        while queue:
            X_features = features.extract(stack, queue, graph, feature_name, sentence)
            X = vec.transform(X_features)
            trans_nr = classifier.predict(X)
            trans = dict_classes[trans_nr[0]]
            stack, queue, graph, trans = parse_ml(stack, queue, graph, trans)
        stack, graph = transition.empty_stack(stack, graph)
        #print('Equal graphs:', transition.equal_graphs(sentence, graph))

        # Poorman's projectivization to have well-formed graphs.
        for word in sentence:
            word['head'] = graph['heads'][word['id']]
            word['deprel'] = graph['deprels'][word['id']]
            if int(word['id']) != 0:
                f_out.write(word['id'] + '\t' + word['form'] + '\t' + word['lemma'] + '\t' + word['cpostag'] + '\t' + word['postag'] + '\t' + word['feats'] + '\t' + word['head'] + '\t' + word['deprel'] + '\t_\t_')
                f_out.write('\n')
        f_out.write('\n')
        # print(transitions)