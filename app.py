import os
import logging
from flask import Flask, render_template
from dotenv import load_dotenv

# Load env variables
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Firebase BEFORE routes that might use it
from config.firebase_config import init_firebase
init_firebase()

from routes.booking_routes import booking_bp

app = Flask(__name__)

# Register blueprints
app.register_blueprint(booking_bp, url_prefix='/api')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=os.environ.get('FLASK_DEBUG', 'False') == 'True')
