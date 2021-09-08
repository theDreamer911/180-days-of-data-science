#########################################
from nltk.stem import WordNetLemmatizer
from flask import Flask, request
import numpy as np
import joblib
import flask
import nltk
import re
#########################################

###############################
nltk.download('wordnet')
nltk.download('punkt')
###############################


#####################################################
app = Flask(__name__)
model = joblib.load('quora_model.pkl')
count_vect = joblib.load('quora_vectorizer.pkl')
#####################################################


###################################################################
def pre_processing(text):
    lemmatizer = WordNetLemmatizer()
    text = text.lower()
    text = re.sub('[0-9]+', 'num', text)
    word_list = nltk.word_tokenize(text)
    word_list = [lemmatizer.lemmatize(item) for item in word_list]
    return ' '.join(word_list)
###################################################################


################################################
@app.route('/')
def index():
    return flask.render_template('index.html')
################################################


################################################
@app.route('/predict', methods=['POST'])
def predict():
    to_predict_list = request.form.to_dict()
    review_text = pre_processing(to_predict_list['review_text'])

    pred = model.predict(count_vect.transform([review_text]))
    prob = model.predict_proba(count_vect.transform([review_text]))
    if prob[0][0] > 0.5:
        prediction = "Positive"
    else:
        prediction = "Negative"

    # Sanitazion to filter out non questions characters
    if not re.search("(?i)(what|which|wo|where|why|when|who|whose|\?)", to_predict_list['review_text']):
        prediction = "Negative"

    return flask.render_template('predict.html', prediction=prediction, prob=np.round(prob[0][0], 3) * 100)
################################################


if __name__ == '__main__':
    app.run(debug=True)
