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

