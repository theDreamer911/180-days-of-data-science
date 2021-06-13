from flask import Flask, render_template
from flask.globals import request
import pandas as pd
import numpy as np
import pickle
import re

app = Flask(__name__)
df = pd.read_csv('./cleaned_car.csv')
model = pickle.load(open('linear_regression_model.pkl', 'rb'))


@app.route('/')
def index():
    perusahaan = sorted(df['company'].unique())
    model_mobil = sorted(df['name'].unique())
    tahun = sorted(df['year'].unique(), reverse=True)
    bahan_bakar = df['fuel_type'].unique()
    perusahaan.insert(0, "Masukkan Perusahaan")

    return render_template('index.html', perusahaan=perusahaan, model_mobil=model_mobil, tahun=tahun, bahan_bakar=bahan_bakar)


@app.route('/predict', methods=['POST'])
def predict():
    perusahaan = request.form.get('perusahaan')
    model_mobil = request.form.get('model_mobil')
    tahun = int(request.form.get('tahun'))
    bahan_bakar = request.form.get('bahan_bakar')
    jarak_tempuh = int(request.form.get('jarak_tempuh'))

    predictions = model.predict(pd.DataFrame([[model_mobil, perusahaan, tahun, jarak_tempuh, bahan_bakar]], columns=[
        'name', 'company', 'year', 'kms_driven', 'fuel_type']))

    money = np.round(predictions[0], 2)
    payment = str(round(money))
    pay = re.sub(r'(?<!^)(?=(\d{3})+$)', r'.', payment)

    return pay


if __name__ == '__main__':
    app.run(debug=True)
