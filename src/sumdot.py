from word2vec import *
import matplotlib.pyplot as plt

def dot(vec1, vec2):
    _vec1 = vec1 / np.linalg.norm(vec1)
    _vec2 = vec2 / np.linalg.norm(vec2)
    return np.dot(_vec1, _vec2)

def get_wv_matrix(texts):
    matrix = None
    for t in texts:
        if t in word2vec.wv:
            if type(matrix) == type(None):
                matrix = word2vec.wv[t]
            else:
                matrix = np.vstack((matrix, word2vec.wv[t]))
    # Avoid Nonetype output
    if type(matrix) != type(None):
        matrix = matrix.reshape(-1, 400)
    return matrix

titles = [r['Title'].split() for r in results]
descriptions = [r['Descriptions'].split() for r in results]
uniq_visitors = [r['UniqueVistors'] for r in results]

scores = np.zeros((len(titles)))
for idx in range(0, len(titles)):
    title, desc = titles[idx], descriptions[idx]
    title_wv, desc_wv = get_wv_matrix(title), get_wv_matrix(desc)
    if type(title_wv) == type(None) or type(desc_wv) == type(None):
        continue

    # Calculate similarity between title and descriptions
    print('[{}/{}] Calculating similarity between title:\n\t{}\ndescription:\n\t{}'.format(idx, len(titles), title, desc))
    s = np.zeros((len(title_wv)))
    for i, t in enumerate(title_wv):
        # Find max in dot(title[i], description[j])
        s[i] = max([dot(t, d) for d in desc_wv])
    print('\tScore: ', np.mean(s))
    # Save mean
    scores[idx] = np.mean(s)
