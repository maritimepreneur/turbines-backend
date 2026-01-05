from flask import Flask
from dotenv import load_dotenv
import os
from routes.home_routes import home_bp
from routes.user_routes import user_bp

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Register blueprints
app.register_blueprint(home_bp)
app.register_blueprint(user_bp)

if __name__ == '__main__':
    port = int(os.getenv('PORT'))
    host = os.getenv('HOST')
    debug = os.getenv('DEBUG', 'True').lower() == 'true'
    
    app.run(host=host, port=port, debug=debug)