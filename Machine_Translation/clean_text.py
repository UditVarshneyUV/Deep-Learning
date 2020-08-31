import string
import re
from unicodedata import normalize
from pickle import dump
from numpy import array

# load doc into memory
def load_doc(filename):
    # open file in read mode
    file = open(filename,mode='rt',encoding='utf-8')
    # read all text
    text = file.read()
    # close the file
    file.close()
    return text

# splitting a loaded document into sentences
def to_pairs(doc):
    lines = doc.strip().split('\n')
    pairs = [line.split('\t') for line in lines]
    return pairs

# Now, we are ready to clean each sentence. The specific cleaning operations we
# will perform are as follows:
# 
# 1. Remove all non-printable characters.
# 2. Remove all punctuation characters.
# 3. Normalize all Unicode characters to ASCII.
# 4. Normalize the case to lowercase.
# 5. Remove any remaining tokens that are not alphabetic.

# clean a list of lines
def clean_pairs(lines):
    cleaned = list()
    # prepare regex for char filtering
    re_print = re.compile('[^%s]' % re.escape(string.printable))
    # prepare translation table for removing punctuation
    table = str.maketrans('', '', string.punctuation)
    for pair in lines:
        clean_pair = list()
        for line in pair:
            # normalize unicode characters
            line = normalize('NFD',line).encode('ascii','ignore')
            line = line.decode('UTF-8')
            # tokenize on white space
            line = line.split()
            # convert to lowercase
            line = [word.lower() for word in line]
            # remove punctuation from each token
            line = [word.translate(table) for word in line]
            # remove non-printable chars from each token
            line = [re_print.sub('',w) for w in line]
            # remove tokens with numbers in item
            line = [word for word in line if word.isalpha()]
            # store as string
            clean_pair.append(' '.join(line))
        cleaned.append(clean_pair)
    return array(cleaned)

# save a list of clean sentences to file
def save_clean_data(sentences,filename):
    dump(sentences,open(filename,'wb'))

# load dataset 
filename = './deu-eng\deu.txt'
doc = load_doc(filename)

# split into english-german pairs
pairs = to_pairs(doc)

# clean sentences
clean_pairs = clean_pairs(pairs)

# save clean pairs to file
save_clean_data(clean_pairs, 'english-german.pkl')

# spot check
for i in range(100):
    print('[%s] => [%s]' % (clean_pairs[i,0],clean_pairs[i,1]))
    print('Saved: %s' % filename)

