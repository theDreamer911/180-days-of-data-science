from flask import Flask, request, render_template, jsonify
import model

app = Flask(__name__, template_folder="templates")


@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/classifier', methods=['POST', 'GET'])
def classify_type():
    try:
        sepal_len = request.args.get('slen')
        sepal_wid = request.args.get('swid')
        petal_len = request.args.get('plen')
        petal_wid = request.args.get('pwid')

        variety = model.classifier(sepal_len, sepal_wid, petal_len, petal_wid)

        return render_template('output.html', variety=variety)
    except:
        return 'Error'


if(__name__ == '__main__'):
    app.run(debug=True)
