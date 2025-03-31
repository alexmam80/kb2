from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy  # Adăugați această linie
from werkzeug.utils import secure_filename
import os

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



app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contact.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
app.secret_key = 'cheie-secreta-foarte-puternica'

# Creează directorul pentru upload dacă nu există
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)


class ContactForm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nume = db.Column(db.String(50), nullable=False)
    prenume = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    telefon = db.Column(db.String(20), nullable=False)
    comentarii = db.Column(db.Text, nullable=False)
    nume_fisier = db.Column(db.String(100))
    data_trimiterii = db.Column(db.DateTime, default=db.func.current_timestamp())


# Creează tabelele (rulează o singură dată)
with app.app_context():
    db.create_all()


@app.route('/submit-form', methods=['POST'])
def submit_form():
    try:
        # Procesează datele din formular
        nume = request.form['nume']
        prenume = request.form['prenume']
        email = request.form['email']
        telefon = request.form['telefon']
        comentarii = request.form['comentarii']

        # Verifică CAPTCHA
        if request.form['captcha'] != '7':
            return jsonify({'error': 'CAPTCHA incorect'}), 400

        # Procesează fișierul încărcat (dacă există)
        fisier = request.files.get('atasare')
        nume_fisier = None
        if fisier and fisier.filename != '':
            nume_fisier = secure_filename(fisier.filename)
            fisier.save(os.path.join(app.config['UPLOAD_FOLDER'], nume_fisier))

        # Salvează în baza de date
        new_contact = ContactForm(
            nume=nume,
            prenume=prenume,
            email=email,
            telefon=telefon,
            comentarii=comentarii,
            nume_fisier=nume_fisier
        )
        db.session.add(new_contact)
        db.session.commit()

        return jsonify({'message': 'Formular trimis cu succes!'})

    except Exception as e:
        app.logger.error(f"Eroare la procesarea formularului: {str(e)}")
        return jsonify({'error': str(e)}), 500







if __name__ == '__main__':
    app.run(debug=True)
