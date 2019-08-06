## Mystery Machine Learning

Learning which Scooby-Doo character said what based on machine learning and transcripts from [https://transcripts.fandom.com](https://transcripts.fandom.com).

## Run the App

#### Installation

Make your [appropriate Python virtualenv](https://pypi.org/project/virtualenv/) and then install the dependencies (`pip install -r requirements.txt`).

#### Collect the data

[Optional] Run `python compile_transcripts.py` to compile the dataset. Source transcripts are in the `transcirpts` directory.

#### Train the Models

Create an empty cache directory to store models (`mkdir cache`).

Then run `python make_sklearn_models.py` to train the models. They will create models as `.joblib` files that live in the `cache` directory.

#### Start the front end

Compile the React front-end to run with Flask!

```
cd client/that-demo
npm run build
cd ../.. # Go back to root to start the Flask app
```

#### Run the Flask App

Once the models are trained, you can serve them on a Flask app. Run `export FLASK_APP=model_app.py; flask run` to launch the app.

You can play directly with the front end or you can make API calls (see below).

#### Make requests to the API

You can now POST the `predict` API with a `text` parameter and get back predictions.

Output will come back with a `prediction` key that says the character who is most likely to have said `text` and a `probability` key for the likelihood that the predicted character said `text`. You will also get back a `probabilities` key with all the individual probabilities for how likely each character is to have said `text`. Lastly, you will get back the `text` you passed as well.

```
curl -i -X POST http://127.0.0.1:5000/predict -d '{"text":"Jinkies!"}' -H "Content-Type: application/json
{"prediction":"Velma Dinkley",
 "probability":0.6843294567220954,
 "probabilities":{"Daphne Blake":0.06822105721051124,
                  "Fred Jones":0.08190035215124208,
                  "Scooby-Doo":0.0726696931194721,
                  "Shaggy Rogers":0.09287944079667905,
                  "Velma Dinkley":0.6843294567220954},
 "text":"Jinkies!"}

curl -i -X POST http://127.0.0.1:5000/predict -d '{"text":"Zoinks!"}' -H "Content-Type: application/json

{"prediction":"Shaggy Rogers",
 "probability":0.7192686835595966,
 "probabilities":{"Daphne Blake":0.06184231582779559,
                  "Fred Jones":0.07819071867107619,
                  "Scooby-Doo":0.07055911654043422,
                  "Shaggy Rogers":0.7192686835595966,
                  "Velma Dinkley":0.0701391654010975},
 "text":"Zoinks!"}
```
