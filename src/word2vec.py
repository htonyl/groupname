import re
import numpy as np
from collections import defaultdict
from gensim.parsing.preprocessing import STOPWORDS
from gensim import corpora, models, similarities
from get_data import *

stoplist = set('s m d t u ll ur ve'.split())
texts = [[word for word in re.split("\W+", re.sub(r"[,.]", "", doc['Title'].lower()))
    if word not in STOPWORDS.union(stoplist) and word is not ""] for doc in results]

frequency = defaultdict(int)
for text in texts:
    for token in text:
        frequency[token] += 1

# Remove all empty strings
frequency[''] = 0

# Extract only duplicate words
texts = [[token for token in text if frequency[token] > 1] for text in texts]
texts = np.array(texts)

# Extract word2vec
word2vec = models.Word2Vec(texts, size=400, window=4, min_count=5, workers=4)
