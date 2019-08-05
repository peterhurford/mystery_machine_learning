import numpy as np
import pandas as pd
import lightgbm as lgb

from collections import defaultdict
from datetime import datetime
from pprint import pprint

from sklearn.metrics import roc_auc_score, confusion_matrix
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import KFold, train_test_split
from sklearn.linear_model import LogisticRegression

from utils import CHARACTERS, remove_parentheticals, clean_punct


HOLDOUT = False


def print_step(step):
    print('[{}]'.format(datetime.now()) + ' ' + step)


lines = pd.read_csv('scooby_doo_lines.csv')

if HOLDOUT:
    train_lines, test_lines, train_character, test_character = train_test_split(lines['line'],
                                                                                lines['character'],
                                                                                test_size=0.1,
                                                                                random_state=42)
else:
    train_lines = lines['line']
    test_lines = None
    train_character = lines['character']
    test_character = None


print_step('TFIDF')
tfidf = TfidfVectorizer(ngram_range=(1, 2),
                        max_features=10000,
                        min_df=2,
                        max_df=0.8,
                        binary=True)
tfidf_train = tfidf.fit_transform(train_lines)
print(tfidf_train.shape)
if HOLDOUT:
    tfidf_test = tfidf.transform(test_lines)
    print(tfidf_test.shape)

all_test_preds = defaultdict(lambda: '')
all_train_preds = defaultdict(lambda: '')
models = defaultdict(lambda: '')

for character in CHARACTERS:
    kf = KFold(n_splits=5, shuffle=True, random_state=42)
    fold_splits = kf.split(tfidf_train)
    cv_scores = []
    character_train_preds = np.zeros(tfidf_train.shape[0])
    character_test_preds = 0
    i = 1
    print_step('{} model...'.format(character))
    for dev_index, val_index in fold_splits:
        dev_X, val_X = tfidf_train[dev_index], tfidf_train[val_index]
        dev_y, val_y = ((train_character == character).values[dev_index].astype(int),
                        (train_character == character).values[val_index].astype(int))
        model = LogisticRegression()
        model.fit(dev_X, dev_y)
        val_preds = model.predict_proba(val_X)[:, 1]
        character_train_preds[val_index] = val_preds
        cv_scores.append(roc_auc_score(val_y, val_preds))
        if HOLDOUT:
            test_preds = model.predict_proba(tfidf_test)[:, 1]
            character_test_preds = character_test_preds + test_preds
        i += 1
    print_step('...{} AUC: {}'.format(character, np.mean(cv_scores)))
    all_train_preds[character] = character_train_preds
    models[character] = model
    if HOLDOUT:
        character_test_preds /= 5
        all_test_preds[character] = character_test_preds


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
    pprint(sorted(list(result.items()), key=lambda x: x[1], reverse=True))

import pdb
pdb.set_trace()


all_train_preds = pd.DataFrame(all_train_preds)
all_train_preds['character'] = train_character.values
all_train_preds['line'] = train_lines.values
all_train_preds['sum'] = np.sum(all_train_preds.drop(['character', 'line'], axis=1), axis=1)
for character in CHARACTERS:
    all_train_preds[character] = all_train_preds[character] / all_train_preds['sum']
all_train_preds.drop('sum', axis=1, inplace=True)
all_train_preds['probability'] = np.max(all_train_preds.drop(['character', 'line'], axis=1), axis=1)
all_train_preds['prediction'] = [all_train_preds.columns[p] for p in np.argmax(all_train_preds.drop(['character', 'line'], axis=1).values, axis=1)]
conf_mat = confusion_matrix(all_train_preds['character'],
                            all_train_preds['prediction'],
                            labels=CHARACTERS)
print(pd.DataFrame(conf_mat, columns=CHARACTERS, index=CHARACTERS))
print('-')

if HOLDOUT:
    all_test_preds = pd.DataFrame(all_test_preds)
    all_test_preds['character'] = test_character.values
    all_test_preds['line'] = test_lines.values
    all_test_preds['sum'] = np.sum(all_test_preds.drop(['character', 'line'], axis=1), axis=1)
    for character in CHARACTERS:
        all_test_preds[character] = all_test_preds[character] / all_test_preds['sum']
    all_test_preds.drop('sum', axis=1, inplace=True)
    all_test_preds['probability'] = np.max(all_test_preds.drop(['character', 'line'], axis=1), axis=1)
    all_test_preds['prediction'] = [all_test_preds.columns[p] for p in np.argmax(all_test_preds.drop(['character', 'line'], axis=1).values, axis=1)]
    conf_mat = confusion_matrix(all_test_preds['character'],
                                all_test_preds['prediction'],
                                labels=CHARACTERS)
    print(pd.DataFrame(conf_mat, columns=CHARACTERS, index=CHARACTERS))
import pdb
pdb.set_trace()


atrp2 = all_train_preds.copy()
atrp2['line_length'] = atrp2['line'].apply(lambda l: len(l.split(' ')))
atrp2.drop(['probability', 'prediction', 'line'], axis=1, inplace=True)

if HOLDOUT:
    atep2 = all_test_preds.copy()
    atep2['line_length'] = atep2['line'].apply(lambda l: len(l.split(' ')))
    atep2.drop(['probability', 'prediction', 'line'], axis=1, inplace=True)


for character in CHARACTERS:
    kf = KFold(n_splits=5, shuffle=True, random_state=42)
    fold_splits = kf.split(atrp2)
    cv_scores = []
    character_train_preds = np.zeros(atrp2.shape[0])
    character_test_preds = 0
    i = 1
    print_step('{} model...'.format(character))
    for dev_index, val_index in fold_splits:
        dev_X, val_X = (atrp2.drop('character', axis=1).values[dev_index],
                       atrp2.drop('character', axis=1).values[val_index])
        dev_y, val_y = ((atrp2['character'] == character).values[dev_index].astype(int),
                        (atrp2['character'] == character).values[val_index].astype(int))
        d_train = lgb.Dataset(dev_X, label=dev_y)
        d_valid = lgb.Dataset(val_X, label=val_y)
        watchlist = [d_train, d_valid]
        params = {'learning_rate': 0.01,
                  'application': 'binary',
                  'max_depth': 9,
                  'num_leaves': 15,
                  'verbosity': -1,
                  'metric': 'rmse',
                  'data_random_seed': 4,
                  'bagging_fraction': 0.8,
                  'feature_fraction': 0.9,
                  'nthread': 4,
                  'lambda_l1': 1,
                  'lambda_l2': 1}
        print('Train Fold {}'.format(i))
        model = lgb.train(params,
                          train_set=d_train,
                          num_boost_round=200,
                          valid_sets=watchlist,
                          verbose_eval=50)
        val_preds = model.predict(val_X)
        character_train_preds[val_index] = val_preds
        cv_scores.append(roc_auc_score(val_y, val_preds))
        if HOLDOUT:
            test_preds = model.predict(atep2.drop('character', axis=1))
            character_test_preds = character_test_preds + test_preds
        i += 1
    print_step('...{} AUC: {}'.format(character, np.mean(cv_scores)))
    all_train_preds[character] = character_train_preds
    models[character] = model
    if HOLDOUT:
        character_test_preds /= 5
        all_test_preds[character] = character_test_preds

import pdb
pdb.set_trace()
