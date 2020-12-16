from flask import Flask, request
import pandas as pd
import numpy as np
import pickle
import flasgger
from flasgger import Swagger


app = Flask(__name__)# from which point we want to start our flask app
Swagger(app)
pickle_in = open("classifier.pkl","rb") # opening in read byte mode
classifier = pickle.load(pickle_in)

@app.route('/')
def welcome():
    return "Welcome All"

@app.route('/predict',methods=["Get"])
def predict_note_authentication():
    
    """Let's Authenticate the Bank Note
    This is using docstrings for specifications.
    ---
    parameters:
      - name: variance
        in: query
        type: number
        required: true
      - name: skewness
        in: query
        type: number
        required: true
      - name: curtosis
        in: query
        type: number
        required: true
      - name: entropy
        in: query
        type: number
        required: true
    responses:
        200:
            description: The output values
    
    """


    
    variance = request.args.get("variance")
    skewness = request.args.get("skewness")
    curtosis = request.args.get("curtosis")
    entropy  = request.args.get("entropy")

    prediction = classifier.predict([[variance,skewness,curtosis,entropy]])

    if prediction[0] == 0:
        result = "FAKE"
    else:
        result = "REAL"
    return "The bank note is {}".format(result)

@app.route("/predict_file",methods=["POST"])
def predict_note_file():

    """Let's Authenticate the Bank Note
    This is using docstrings for specifications.
    ---
    parameters:
      - name: file
        in: formData
        type: file
        required: true
    responses:
        200:
            description: The output values 
    """
    
    df_test = pd.read_csv(request.files.get("file"))
    prediction = classifier.predict(df_test)

    return "The predicted values for the csv file are {}".format(str(list(prediction)))


if __name__ == "__main__":
    app.run()
