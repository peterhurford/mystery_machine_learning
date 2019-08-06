import eli5

import numpy as np

from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from joblib import load
from collections import defaultdict

from utils import CHARACTERS, remove_parentheticals, clean_punct, print_step, get_first_name


def get_text(text):
    t_text = remove_parentheticals(text)
    t_text = clean_punct(t_text)
    return t_text

def predict_character(text):
    t_text = get_text(text)
    tfidf_text = tfidf.transform([t_text])
    preds = defaultdict(lambda: 0)
    for character in CHARACTERS:
        preds[character] = models[character].predict_proba(tfidf_text)[:, 1][0]
    sumx = sum(preds.values())
    for character in CHARACTERS:
        preds[character] /= sumx
    return {'text': text,
            'prediction': list(preds.keys())[np.argmax(list(preds.values()))],
            'probability': np.max(list(preds.values())),
            'probabilities': preds}

def get_character_from_name(character):
    indices = [get_first_name(c).lower() == character for c in CHARACTERS]
    if not any(indices):
        return 'Not found'
    else:
        return CHARACTERS[np.argmax(indices)]


print_step('Load TFIDF')
tfidf = load('cache/tfidf.joblib')
models = defaultdict(lambda: '')
for character in CHARACTERS:
    print_step('Loading {} model...'.format(character))
    models[character] = load('cache/{}_model.joblib'.format(character))


app = Flask(__name__, static_folder='client/that-demo/build/static', template_folder='build')
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ping')
def ping():
    return 'Pong'

@app.route('/predict/<string>', methods=['GET'])
def get_predict(string):
    return jsonify(predict_character(string))

@app.route('/predict/<character>', methods=['POST'])
def post_predict():
    string = request.json['text']
    return jsonify(predict_character(string))

@app.route('/explain/<string>', methods=['GET'])
def get_explain(string):
    prediction = predict_character(string)
    string = get_text(string)
    character = prediction['prediction']
    html = eli5.show_prediction(models[character], string, targets=[1], vec=tfidf).data
    html = ('<h2>Predicted ' + character + ' (' + str(int(round(prediction['probability'] * 100))) +
            '%)</h2>' + html)
    return html

@app.route('/explain', methods=['POST'])
def post_explain():
    string = request.json['text']
    string = get_text(string)
    prediction = predict_character(string)
    character = prediction['prediction']
    explanation = eli5.explain_prediction(models[character], string, targets=[1], vec=tfidf)
    explanation = explanation.targets[0].feature_weights
    explanation = explanation.pos + explanation.neg
    explanation = [(f.feature, f.weight) for f in explanation if f.feature != '<BIAS>']
    return jsonify({'prediction': character,
                    'probability': prediction['probability'],
                    'text': string,
                    'explanation': dict(explanation)})

@app.route('/top_features/<character>', methods=['GET'])
def weights(character):
    character = get_character_from_name(character)
    return eli5.show_weights(models[character], vec=tfidf).data
