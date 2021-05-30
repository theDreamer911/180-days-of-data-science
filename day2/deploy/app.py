from flask import Flask, render_template, request
import joblib
import numpy as np

app = Flask(__name__, template_folder='web')


@app.route('/')
def student():
    return render_template("home.html")


def ValuePredictor(to_predict_list):
    to_predict = np.array(to_predict_list).reshape(-1, 1)
    loaded_model = joblib.load('model.sav')
    result = loaded_model.predict(to_predict)
    return result[0]


@app.route('/', methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        to_predict_list = request.form.to_dict()
        to_predict_list = list(to_predict_list.values())
        to_predict_list = list(map(float, to_predict_list))
        result = round(float(ValuePredictor(to_predict_list)), 2)
        return render_template("home.html", result=result)


if __name__ == '__main__':
    app.run(debug=True)
