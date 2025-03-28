# pip install flask
from flask import Flask, render_template
from flask import request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/servicii')
def servicii():
    return render_template('servicii.html')

@app.route('/galerie')
def galerie():
    return render_template('galerie.html')

@app.route('/contacte')
def contacte():
    return render_template('contacte.html')



if __name__ == '__main__':
    app.run(debug=True)