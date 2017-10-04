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


def encode_classes(y_symbols):
    """
    Encode the classes as numbers
    :param y_symbols:
    :return: the y vector and the lookup dictionaries
    """
    # We extract the chunk names
    classes = sorted(list(set(y_symbols)))
    # We assign each name a number
    dict_classes = dict(enumerate(classes))
    # We build an inverted dictionary
    inv_dict_classes = {v: k for k, v in dict_classes.items()}
    # We convert y_symbols into a numerical vector
    y = [inv_dict_classes[i] for i in y_symbols]
    return y, dict_classes, inv_dict_classes


if __name__ == '__main__':
    train_file = 'swedish_talbanken05_train.conll'
    test_file = 'swedish_talbanken05_test.conll'
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
    y, dict_classes, inv_dict_classes = encode_classes(y_symbols)
    pickle.dump(dict_classes, open('mapping3', 'wb'))
    '''print("Training the model...")
    classifier = linear_model.LogisticRegression(penalty='l2', dual=True, solver='liblinear')
    model = classifier.fit(X, y)
    print(model)
    joblib.dump(model, 'set1.pkl')

    classifier = joblib.load('set1.pkl')
    test_sentences = conll.read_sentences(test_file)
    test_formatted_corpus = conll.split_rows(test_sentences, column_names_2006)
    # Here we carry out a chunk tag prediction and we report the per tag error
    # This is done for the whole corpus without regard for the sentence structure
    print("Predicting the chunks in the test set...")
    X_dict_test = list()
    y_symbols_test = list()
    sent_cnt = 0
    for sentence in test_formatted_corpus:
        sent_cnt += 1
        if sent_cnt % 1000 == 0:
            print(sent_cnt, 'sentences on', len(test_formatted_corpus), flush=True)
        stack = []
        queue = list(sentence)
        graph = {}
        graph['heads'] = {}
        graph['heads']['0'] = '0'
        graph['deprels'] = {}
        graph['deprels']['0'] = 'ROOT'
        transitions = []
        while queue:
            X_dict_test.append(features.extract(stack, queue, graph, feature_name, sentence))
            stack, queue, graph, trans = reference(stack, queue, graph)
            transitions.append(trans)
            y_symbols_test.append(trans)
        stack, graph = transition.empty_stack(stack, graph)
        #print('Equal graphs:', transition.equal_graphs(sentence, graph))

        # Poorman's projectivization to have well-formed graphs.
        for word in sentence:
            word['head'] = graph['heads'][word['id']]
    # Vectorize the test set and one-hot encoding
    X_test = vec.transform(X_dict_test)  # Possible to add: .toarray()
    y_test = [inv_dict_classes[i] if i in y_symbols else 0 for i in y_symbols_test]
    y_test_predicted = classifier.predict(X_test)
    print("Classification report for classifier %s:\n%s\n"
          % (classifier, metrics.classification_report(y_test, y_test_predicted)))
    #clf = joblib.load('filename.pkl')'''