from flask import Flask, request, make_response, render_template_string
from datetime import datetime, timedelta

class CookieConsent:
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.context_processor(self.inject_cookie_status)
        app.before_request(self.check_consent)

    def inject_cookie_status(self):
        """Adaugă starea cookie-urilor în toate template-urile"""
        return {'cookies_accepted': request.cookies.get('cookie_consent') == 'true'}

    def check_consent(self):
        """Verifică consimțământul pentru cookie-uri"""
        if request.endpoint != 'static':
            consent = request.cookies.get('cookie_consent')
            if consent is None and not request.path.startswith('/set-cookie-consent'):
                return self.show_cookie_banner()

    def show_cookie_banner(self):
        """Arată bannerul de cookie-uri"""
        banner_html = """
        <div id="cookie-banner" style="position:fixed;bottom:0;left:0;right:0;background:#333;color:#fff;padding:15px;z-index:1000;">
            <div style="max-width:1200px;margin:0 auto;display:flex;justify-content:space-between;align-items:center;">
                <p>Acest site folosește cookie-uri pentru a îmbunătăți experiența ta. Continuând, ești de acord cu utilizarea lor.</p>
                <div>
                    <button onclick="location.href='/set-cookie-consent?accept=true'" style="background:#4CAF50;color:white;border:none;padding:8px 15px;margin-right:10px;">Accept</button>
                    <button onclick="location.href='/set-cookie-consent?accept=false'" style="background:#f44336;color:white;border:none;padding:8px 15px;">Refuză</button>
                </div>
            </div>
        </div>
        """
        return render_template_string(banner_html)

def setup_cookie_routes(app):
    @app.route('/set-cookie-consent')
    def set_cookie_consent():
        accept = request.args.get('accept', 'false').lower() == 'true'
        response = make_response(redirect_back())
        
        if accept:
            expiry = datetime.now() + timedelta(days=365)
            response.set_cookie(
                'cookie_consent', 
                'true',
                expires=expiry,
                httponly=True,
                samesite='Lax'
            )
            # Setează cookie-uri esențiale aici
            response.set_cookie(
                'session_cookie', 
                'essential',
                expires=expiry,
                httponly=True,
                samesite='Lax'
            )
        else:
            # Șterge cookie-urile non-esențiale existente
            response.delete_cookie('_ga')
            response.delete_cookie('_gid')
        
        return response

    def redirect_back():
        return request.referrer or url_for('index')
