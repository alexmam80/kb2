from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

# Configure upload folder for contact form
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/servicii')
def servicii():
    return render_template('servicii.html')

@app.route('/galerie')
def galerie():
    return render_template('galerie.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Process form data
        nume = request.form.get('nume')
        prenume = request.form.get('prenume')
        email = request.form.get('email')
        telefon = request.form.get('telefon')
        comentarii = request.form.get('comentarii')
        captcha = request.form.get('captcha')
        
        # Validate captcha
        if captcha != '7':
            return render_template('contacte.html', error="Captcha incorect")
        
        # Handle file upload
        if 'atasare' in request.files:
            file = request.files['atasare']
            if file.filename != '':
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        
        # Here you would typically save to database or send email
        print(f"Form submission: {nume} {prenume}, {email}, {telefon}, {comentarii}")
        
        return redirect(url_for('contact', success="Formular trimis cu succes!"))
    
    success = request.args.get('success')
    return render_template('contacte.html', success=success)

if __name__ == '__main__':
    app.run(debug=True)
