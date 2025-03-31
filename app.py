# pip install flask
from flask import Flask, render_template, request, make_response
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

@app.route('/')
def index():
    if request.cookies.get('cookie_consent') == 'true':
        # Setează cookie-uri de analiză doar dacă există consimțământ
        response = make_response(render_template('index.html'))
        response.set_cookie('analytics_cookie', 'enabled', max_age=30*24*60*60)  # Expiră în 30 de zile
        return response
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
