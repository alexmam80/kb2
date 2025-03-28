# pip install flask
from flask import Flask, render_template, request, redirect, url_for, make_response, flash
from cookies import CookieConsent, setup_cookie_routes
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # SQLite database
db = SQLAlchemy(app)


# Configurare Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Crează baza de date (rulează o singură dată)
with app.app_context():
    db.create_all()

# === RUTE PRINCIPALE ===
@app.route('/')
def index():
    if request.cookies.get('cookie_consent') == 'true':
        response = make_response(render_template('index.html'))
        response.set_cookie('analytics_cookie', 'enabled', max_age=30*24*60*60)
        return response
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Verifică dacă utilizatorul există deja
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash('Username sau email deja folosit!', 'danger')
            return redirect(url_for('register'))
        
        # Creează utilizator nou
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Cont creat cu succes! Te poți autentifica.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Autentificare reușită!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Autentificare eșuată. Verifică username și parolă.', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Ai fost deconectat cu succes.', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)





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
