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

#### Run the Flask App

Once the models are trained, you can serve them on a Flask app. Run `export FLASK_APP=model_app.py; flask run` to launch the app.
