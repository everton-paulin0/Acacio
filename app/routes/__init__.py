from .auth_routes import auth_bp
from .health import health_bp

def register_routes(app):
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(health_bp)
