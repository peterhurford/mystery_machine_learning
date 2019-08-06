import numpy as np

from flask import Flask, jsonify, request
from flask_cors import CORS
from joblib import load
from collections import defaultdict

from utils import CHARACTERS, remove_parentheticals, clean_punct, print_step


def predict_character(text):
    t_text = remove_parentheticals(text)
    t_text = clean_punct(t_text)
    tfidf_text = tfidf.transform([t_text])
    preds = defaultdict(lambda: 0)
    for character in CHARACTERS:
        preds[character] = models[character].predict_proba(tfidf_text)[:, 1][0]
    sumx = sum(preds.values())
    for character in CHARACTERS:
        preds[character] /= sumx
    return {'text': text,
            'prediction': preds.keys()[np.argmax(preds.values())],
			'probability': np.max(preds.values()),
            'probabilities': preds}


print_step('Load TFIDF')
tfidf = load('cache/tfidf.joblib')
models = defaultdict(lambda: '')
for character in CHARACTERS:
    print_step('Loading {} model...'.format(character))
    models[character] = load('cache/{}_model.joblib'.format(character))


app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return 'Main page!'

@app.route('/ping')
def ping():
    return 'Pong'

@app.route('/predict/<string>', methods=['GET'])
def get_predict(string):
	return jsonify(predict_character(string))

@app.route('/predict', methods=['POST'])
def post_predict():
    string = request.json['text']
    return jsonify(predict_character(string))
