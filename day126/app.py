# All is from [importdata](https://github.com/importdata/kpop-analysis)

import pandas as pd
import pickle
import flask

# Use pickle to load in the pre-trained model
with open(f"model.pkl", 'rb') as f:
    model = pickle.load(f)

# Initilize the flask app
app = flask.Flask(__name__, template_folder='templates')

'''
# Open pickle file in the rea mode
model = pickle.load(open('model.pkl', 'rb'))

# Root node for API URL


@app.route('/')
def home():
    return render_template('index.html')

# Create another API


@app.route('/predict', methods=['POST'])
def predict():
    # For rendering results on HTML GUI
    int_features = [int(x) for x in request.form.values()]

    # Convert above values into array
    final_features = [np.array(int_features)]

    # Perform predicttions
    prediction = model.predict(final_features)

    # Get prediction
    output = round(prediction[0], 2)
    print(output)

    return render_template('index.html', prediction_text="The predicted number of hours you listen to K-POP is {} hours".format(output))
'''


@app.route('/', methods=['GET', 'POST'])
def main():
    if flask.request.method == 'GET':
        return(flask.render_template('index.html'))

    if flask.request.method == 'POST':
        yr_litened = flask.request.form['yr_litened']
        daily_MV_hr = flask.request.form['daily_MV_hr']
        yr_merch_spent = flask.request.form['yr_merch_spent']
        age = flask.request.form['age']
        num_grp_like = flask.request.form['num_grp_like']

    # Make DataFrame for model
    input_variables = pd.DataFrame([[yr_litened, daily_MV_hr, yr_merch_spent, age, num_grp_like]], columns=[
                                   'yr_litened', 'daily_MV_hr', 'yr_merch_spent', 'age', 'num_grp_like'], dtype=float, index=['input'])

    # Get the prediction
    prediction = model.predict(input_variables)[0]
    output = float(round(prediction, 2))

    # Render form again
    return flask.render_template('index.html',
                                 original_input={'yr_litened': yr_litened,
                                                 'daily_MV_hr': daily_MV_hr,
                                                 'yr_merch_spent': yr_merch_spent,
                                                 'age': age,
                                                 'num_grp_like': num_grp_like},
                                 result=float(output))


if __name__ == '__main__':
    app.run(debug=True)
