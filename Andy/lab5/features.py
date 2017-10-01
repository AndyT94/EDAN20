import transition

def extract(stack, queue, graph, feature_names, sentence):
    features = list()

    #Set 1
    features.extend(['nil', 'nil', 'nil', 'nil'])
    if stack:
        features[0] = stack[0]['postag']
        features[1] = stack[0]['form']
    if queue:
        features[2] = queue[0]['postag']
        features[3] = queue[0]['form']
    features.append(transition.can_reduce(stack, graph))
    features.append(transition.can_leftarc(stack, graph))

    #Set 2
    features.extend(['nil', 'nil', 'nil', 'nil'])
    if len(stack) > 1:
        features[6] = stack[1]['postag']
        features[7] = stack[1]['form']
    if len(queue) > 1:
        features[8] = queue[1]['postag']
        features[9] = queue[1]['form']

    #Set 3
    features.extend(['nil', 'nil', 'nil', 'nil'])
    if stack and len(sentence) > int(stack[0]['id']) + 1:
        features[10] = sentence[int(stack[0]['id']) + 1]['postag']
        features[11] = sentence[int(stack[0]['id']) + 1]['form']
    if queue and len(sentence) > int(queue[0]['id']) + 1:
        features[12] = sentence[int(queue[0]['id']) + 1]['postag']
        features[13] = sentence[int(queue[0]['id']) + 1]['form']

    features = dict(zip(feature_names, features))
    return features