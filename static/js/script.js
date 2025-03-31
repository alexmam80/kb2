// Selectăm butonul și meniul
const menuToggle = document.querySelector('.menu-toggle');
const menu = document.querySelector('.menu');

// Adăugăm evenimentul de click
menuToggle.addEventListener('click', () => {
    menu.classList.toggle('active'); // Adaugă sau elimină clasa 'active'
});

// Închidem meniul când se face click în afara lui (opțional)
document.addEventListener('click', (e) => {
    if (!menu.contains(e.target) && !menuToggle.contains(e.target)) {
        menu.classList.remove('active');
    }
});



//Contact Form
function submitForm() {
    const form = document.getElementById('contactForm');
    const formData = new FormData(form);
    const responseMessage = document.getElementById('responseMessage');

    fetch('/submit-form', {
        method: 'POST',
        body: formData,
        headers: {
            'Accept': 'application/json'  // Cere explicit răspuns JSON
        }
    })
    .then(response => {
        if (!response.ok) {
            return response.text().then(text => {
                throw new Error(text || 'Eroare la server');
            });
        }
        return response.json();
    })
    .then(data => {
        responseMessage.innerHTML = `<div class="success">${data.message || 'Formular trimis cu succes!'}</div>`;
        form.reset();
    })
    .catch(error => {
        console.error('Eroare:', error);
        responseMessage.innerHTML = `<div class="error">${error.message || 'Eroare la trimiterea formularului'}</div>`;
    });
}
