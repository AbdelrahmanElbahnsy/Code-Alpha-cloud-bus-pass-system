import os
import firebase_admin
from firebase_admin import credentials, firestore
import logging

logger = logging.getLogger(__name__)

def init_firebase():
    """Initializes Firebase Admin SDK and returns the Firestore client."""
    try:
        # Prevent re-initialization errors
        if not firebase_admin._apps:
            # Use environment variable, fallback to local firebase.json
            cred_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS', 'firebase.json')
            
            if not os.path.exists(cred_path):
                raise FileNotFoundError(
                    f"Firebase credentials not found. Please ensure {cred_path} exists "
                    "or set the GOOGLE_APPLICATION_CREDENTIALS environment variable."
                )
            
            # Ensure proper initialization using credentials.Certificate
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
            logger.info(f"Firebase initialized successfully using {cred_path}")
            
        # Return Firestore client
        return firestore.client()
        
    except Exception as e:
        logger.error(f"Failed to initialize Firebase: {e}")
        raise

def get_db():
    """Helper function to get the Firestore client."""
    return init_firebase()
