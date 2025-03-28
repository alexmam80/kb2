# pip install flask
from flask import Flask, render_template, request, redirect, url_for, make_response
from cookies import CookieConsent, setup_cookie_routes
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Important pentru securitate!

# Inițializează sistemul de cookie-uri
cookie_consent = CookieConsent(app)
setup_cookie_routes(app)

@app.route('/')
def index():
    if request.cookies.get('cookie_consent') == 'true':
        # Setează cookie-uri de analiză doar dacă există consimțământ
        response = make_response(render_template('index.html'))
        response.set_cookie('analytics_cookie', 'enabled', max_age=30*24*60*60)  # Expiră în 30 de zile
        return response
    return render_template('index.html')

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

# Adaugă această rută pentru politica de cookie-uri
@app.route('/politica-cookie-uri')
def cookie_policy():
    return render_template('cookie_policy.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
