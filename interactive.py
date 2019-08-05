from pprint import pprint
from joblib import load
from collections import defaultdict

from utils import CHARACTERS, remove_parentheticals, clean_punct, print_step


print_step('Load TFIDF')
tfidf = load('cache/tfidf.joblib')
models = defaultdict(lambda: '')
for character in CHARACTERS:
    print_step('Loading {} model...'.format(character))
    models[character] = load('cache/{}_model.joblib'.format(character))

def predict_character(text):
    text = remove_parentheticals(text)
    text = clean_punct(text)
    text = tfidf.transform([text])
    preds = defaultdict(lambda: 0)
    for character in CHARACTERS:
        preds[character] = models[character].predict_proba(text)[:, 1][0]
    sumx = sum(preds.values())
    for character in CHARACTERS:
        preds[character] /= sumx
    return preds

def show_me(result):
    return sorted(list(result.items()), key=lambda x: x[1], reverse=True)

import pdb
pdb.set_trace()
