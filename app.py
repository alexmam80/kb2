from flask import Flask, render_template, request, redirect, url_for, make_response, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import psycopg2
import os

# Detalii conexiune
DB_USERNAME = 'alexmam80'
DB_PASSWORD = 'h846kPdU9iUOBNAl5Z70FryMZ2T7wYL5'
DB_HOST = 'dpg-cvjaa4ili9vc73eje560-a'
DB_NAME = 'kb2-db'

# Construiește URL-ul de conexiune
DATABASE_URL = 'postgresql://alexmam80:h846kPdU9iUOBNAl5Z70FryMZ2T7wYL5@dpg-cvjaa4ili9vc73eje560-a/kb2'

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', '23jkh4b5k2j3h4b5k2j3h4b5')
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Conectare la PostgreSQL
def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

# Creează tabela "users" (dacă nu există)
def create_users_table():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    cur.close()
    conn.close()
    
# Ruta pentru înregistrare utilizator
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    email = data['email']
    password = data['password']

    # Hashuiește parola
    password_hash = generate_password_hash(password)

    # Salvează în baza de date
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            'INSERT INTO users (username, password_hash, email) VALUES (%s, %s, %s)',
            (username, password_hash, email)
        )
        conn.commit()
        return jsonify({"message": "User created successfully!"}), 201
    except psycopg2.IntegrityError:
        return jsonify({"error": "Username or email already exists!"}), 400
    finally:
        cur.close()
        conn.close()





    
# Ruta pentru autentificare
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT password_hash FROM users WHERE username = %s', (username,))
    user = cur.fetchone()
    cur.close()
    conn.close()

    if user and check_password_hash(user[0], password):
        return jsonify({"message": "Login successful!"}), 200
    else:
        return jsonify({"error": "Invalid username or password!"}), 401

if __name__ == '__main__':
    create_users_table()  # Asigură-te că tabela există
    app.run(debug=True)
    












@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

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








@app.route('/debug-db')
def debug_db():
    try:
        # Modifică această linie pentru a utiliza funcția text() pentru expresiile SQL
        from sqlalchemy import text
        result = db.session.execute(text('SELECT 1')).fetchone()
        
        # Verifică dacă tabelul utilizatorilor există
        user_count = None
        try:
            user_count = User.query.count()
        except:
            pass
        
        return f"""
        <h1>Debug Bază de Date</h1>
        <p>Conexiunea la baza de date: <strong>Funcțională</strong></p>
        <p>Rezultat interogare de test: {result}</p>
        <p>URL Bază de Date: {DATABASE_URL}</p>
        <p>Număr utilizatori: {user_count}</p>
        """
    except Exception as e:
        return f"""
        <h1>Debug Bază de Date</h1>
        <p>Conexiunea la baza de date: <strong>Eroare</strong></p>
        <p>Eroare: {str(e)}</p>
        <p>URL Bază de Date: {DATABASE_URL}</p>
        """







    
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
