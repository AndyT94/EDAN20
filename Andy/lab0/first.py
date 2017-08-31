# A first program
a = 1
b = 2
c = a / (b + 1)
text = 'Result:'
print(text, c)

# Introductory programs
for i in [1, 2, 3, 4, 5, 6]:
    print(i)
print('Done\n')

for i in [1, 2, 3, 4, 5, 6]:
    if i % 2 == 0:
        print('Even:', i)
    else:
        print('Odd:', i)
print('Done\n')

# String
alphabet = 'abcdefghijklmnopqrstuvwxyz'
print('alphabet[0]:', alphabet[0]) # ’a’
print('alphabet[1]:', alphabet[1]) # ’b’
print('alphabet[25]:', alphabet[25]) # ’z’

print('alphabet[-1]:', alphabet[-1]) # the last character of a string: ’z’
print('alphabet[-2]:', alphabet[-2]) # the second last: ’y’
print('alphabet[-26]:', alphabet[-26]) # ’a’

print('len(alphabet):', len(alphabet)) # 26

def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    print(splits)
    deletes    = [L + R[1:]               for L, R in splits if R]
    print(deletes)
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    print(transposes)
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    print(replaces)
    inserts    = [L + c + R               for L, R in splits for c in letters]
    print(inserts)
    return set(deletes + transposes + replaces + inserts)


def edits2(word):
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))