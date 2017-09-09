import sys
import regex as re

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