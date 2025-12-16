"""
Flask application factory
"""
from flask import Flask
from flask_cors import CORS

def create_app():
    """Create and configure Flask application"""
    app = Flask(__name__)
    
    # Enable CORS
    CORS(app)
    
    # Basic configuration
    app.config['JSON_SORT_KEYS'] = False
    
    # Register blueprints
    from app.routes import api_bp
    app.register_blueprint(api_bp)
    
    # Register storage routes
    from app.storage.minio_proxy import storage_bp
    app.register_blueprint(storage_bp)
    
    # Health check endpoint
    @app.route('/health')
    def health():
        return {'status': 'ok', 'service': 'StarTrack Backend'}
    
    return app
