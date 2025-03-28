from flask import Flask, render_template, request, redirect, url_for, make_response, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default-secret-key-please-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///site.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    
    def __repr__(self):
        return f'<User {self.username}>'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def login_required_global(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Vă rugăm să vă autentificați pentru a accesa această pagină.', 'warning')
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
@login_required_global
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Validare input
        if not username or not email or not password:
            flash('Vă rugăm să completați toate câmpurile.', 'danger')
            return redirect(url_for('register'))
        
        # Verifică lungimea parolei
        if len(password) < 8:
            flash('Parola trebuie să aibă cel puțin 8 caractere.', 'danger')
            return redirect(url_for('register'))
        
        # Verifică existența utilizatorului
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash('Utilizator sau email deja existent!', 'danger')
            return redirect(url_for('register'))
        
        # Creează utilizator nou
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, email=email, password=hashed_password)
        
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Cont creat cu succes! Vă puteți autentifica acum.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash('A apărut o eroare la crearea contului.', 'danger')
            app.logger.error(f'Eroare înregistrare: {str(e)}')
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            next_page = request.args.get('next')
            flash('Autentificare reușită!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Autentificare eșuată. Verifică username și parolă.', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Ați fost deconectat cu succes.', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

@app.route('/servicii')
def servicii():
    return render_template('servicii.html')

@app.route('/galerie')
def galerie():
    return render_template('galerie.html')

@app.route('/contacte')
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
    # Creează baza de date dacă nu există
    with app.app_context():
        db.create_all()
    
    # Configurare pentru mediul de producție
    app.run(
        host='0.0.0.0', 
        port=int(os.environ.get('PORT', 10000)),
        debug=os.environ.get('FLASK_DEBUG', 'False') == 'True'
    )
