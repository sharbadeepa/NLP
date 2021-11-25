import re
import unicodedata
import string
import random
import nltk
from nltk.util import ngrams
import streamlit as st

from nltk.probability import ConditionalFreqDist
from nltk.tokenize import word_tokenize
import numpy as np

st.write("""
 # Next Tamil Word Prediction
""")

predict = {}
def predict_dict(current : str, next_word : str):
    if current not in predict:
        predict.update({current: {next_word: 1} })
        return
    options = predict[current]
    print(options)
    if next_word not in options:
        options.update({next_word : 1})
    else:

        options.update({next_word : options[next_word] + 1})


with open('sample2.txt', 'r') as f:
    lines=f.readlines()
    text = "".join(lines)
    text = text.translate(str.maketrans(' ', ' ', string.punctuation))
    pattern = r'[(\\n]+'
    regex = re.sub(pattern," ", text)
    print("==============================",regex)

    word_tokens = regex.split(" ")
    for i in range(len(word_tokens) - 1):
        predict_dict(word_tokens[i], word_tokens[i+1])

    bigram = list(ngrams(word_tokens, 2))
    freq_tri = nltk.FreqDist(bigram)
    freq_tri.plot(30, cumulative=False)
    cfdist = ConditionalFreqDist()
    
    prob_sum, sum_vals = 0, sum(freq_tri.values())
#     print(sum_vals) - total no words
    for k, v in freq_tri.items():
#         print(v)-the words repeated how many times
        pmf = v / sum_vals
        prob_sum += pmf
        freq_tri[k] = prob_sum
        print(k,v)

for word, transition in predict.items():
    transition = dict((key, value / sum(transition.values())) 
                      for key, value in transition.items())
    predict[word] = transition
#     print(predict[word])
    
line = input('> ')
st.write(line)

word = line.strip().split(' ')[-1]
st.write(word)
if word not in predict:
    print('Word not found')
else:
    options = predict[word]
    
    predicted = np.random.choice(list(options.keys()), p=list(options.values()))
    print(line + ' ' + predicted)
    st.write(predicted)
    for i,j in options.items():
        print("=========",i)
        st.write(line + ' ' + i)


