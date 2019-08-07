echo building all the things...
cd client/that-demo;
npm run build;
cd ../..
export FLASK_APP=model_app.py; 
flask run;