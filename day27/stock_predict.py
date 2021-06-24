# PREDICTION FROM DATA IN 2015

# Load the modules

from sklearn.preprocessing import MinMaxScaler
from keras.models import load_model

import matplotlib.pyplot as plt
import pandas_datareader as web
import datetime as dt
import pandas as pd
import numpy as np

# Load the model
model = load_model('stock_model.h5')

# Load the train data
company = 'BBRI.JK'  # You can change this Company

start = dt.datetime(2015, 1, 1)
end = dt.datetime(2021, 5, 1)

data = web.DataReader(company, 'yahoo', start, end)

# Preparing the data
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(data['Close'].values.reshape(-1, 1))

prediction_days = 60

X_train = []
y_train = []

for x in range(prediction_days, len(scaled_data)):
    X_train.append(scaled_data[x - prediction_days: x, 0])
    y_train.append(scaled_data[x, 0])

X_train, y_train = np.array(X_train), np.array(y_train)
X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))

# Preparing test data
test_start = dt.datetime(2021, 5, 1)
test_end = dt.datetime.now()

test_data = web.DataReader(company, 'yahoo', test_start, test_end)
actual_prices = test_data['Close'].values

total_dataset = pd.concat((data['Close'], test_data['Close']), axis=0)

model_inputs = total_dataset[len(
    total_dataset) - len(test_data) - prediction_days:].values
model_inputs = model_inputs.reshape(-1, 1)
model_inputs = scaler.transform(model_inputs)

X_test = []

for x in range(prediction_days, len(model_inputs)):
    X_test.append(model_inputs[x-prediction_days:x, 0])

X_test = np.array(X_test)
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

predicted_prices = model.predict(X_test)
predicted_prices = scaler.inverse_transform(predicted_prices)

# Save the visualization predictions
plt.plot(actual_prices, color='black', label=f"Actual {company} Price")
plt.plot(predicted_prices, color='green', label=f"Predicted {company} Price")
plt.title(f"{company} Stock Price")
plt.xlabel('Time')
plt.ylabel(f"{company} Stock Price")
plt.legend()
plt.savefig(f'{company}_stock.png')

# Predict tomorrow market
real_data = [
    model_inputs[len(model_inputs) + 1 - prediction_days:len(model_inputs+1), 0]]
real_data = np.array(real_data)
real_data = np.reshape(real_data, (real_data.shape[0], real_data.shape[1], 1))

prediction = model.predict(real_data)
prediction = scaler.inverse_transform(prediction)
print(f"Prediction: {prediction}")
