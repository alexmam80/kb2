from flask import Flask, render_template, request, redirect, url_for, make_response, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import psycopg2
import os



@app.route('/index')
@login_required
def dashboard():
    return render_template('index.html')

@app.route('/servicii')
@login_required
def servicii():
    return render_template('servicii.html')

@app.route('/galerie')
@login_required
def galerie():
    return render_template('galerie.html')

@app.route('/contacte')
@login_required
def contacte():
    return render_template('contacte.html')








@app.route('/set-cookie-consent', methods=['POST'])
def set_cookie_consent():
    # Creează un răspuns care redirecționează către pagina principală
    response = make_response(redirect(url_for('index')))
    
    # Setează cookie-ul de consimțământ pentru 30 de zile
    response.set_cookie('cookie_consent', 'true', max_age=30*24*60*60)
    
    # Adaugă un mesaj flash pentru confirmare
    flash('Ați acceptat utilizarea cookie-urilor.', 'success')
    
    return response
    
@app.route('/politica-cookie-uri')
def cookie_policy():
    return render_template('cookie_policy.html')

@app.before_request
def check_cookie_consent():
    # Liste de rute exceptate de la verificarea cookie-urilor
    exempt_routes = [
        'cookie_policy',  # Pagina politicii de cookie-uri
        'set_cookie_consent',  # Ruta pentru setarea consimțământului 
        'static',  # Resurse statice 
        'login',  # Pagina de autentificare
        'register'  # Pagina de înregistrare
    ]
    
    # Verifică dacă ruta curentă necesită consimțământ pentru cookie-uri
    if request.endpoint not in exempt_routes:
        # Verifică dacă cookie-ul de consimțământ există
        if not request.cookies.get('cookie_consent'):
            # Redirecționează către pagina politicii de cookie-uri
            return redirect(url_for('cookie_policy'))





if __name__ == '__main__':
    create_users_table()  # Asigură-te că tabela există
    app.run(debug=True)








    
    # Configurare pentru mediul de producție
    port = int(os.environ.get('PORT', 10000))
    debug = os.environ.get('FLASK_DEBUG', 'False') == 'True'
    
    print(f"Aplicația va rula pe portul {port} cu debug={debug}")
    print(f"Utilizăm URL-ul bazei de date: {DATABASE_URL}")
    
    app.run(
        host='0.0.0.0', 
        port=port,
        debug=debug
    )
