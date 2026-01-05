from flask import Flask
from dotenv import load_dotenv
import os
from routes.home_routes import home_bp
from routes.user_routes import user_bp
from database import db, init_db

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Database configuration
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

# Build database URL
DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
init_db(app)

# Register blueprints
app.register_blueprint(home_bp)
app.register_blueprint(user_bp)

# Test database connection
@app.route('/db-test')
def test_db():
    try:
        from sqlalchemy import text
        # Test connection
        result = db.session.execute(text('SELECT 1'))
        return {'status': 'success', 'message': 'Database connected successfully!', 'result': 'Query executed'}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}, 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    host = os.getenv('HOST', '0.0.0.0')
    debug = os.getenv('DEBUG', 'True').lower() == 'true'
    
    app.run(host=host, port=port, debug=debug)