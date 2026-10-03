from flask import Blueprint, request, jsonify
from services.booking_service import book_ticket, get_all_tickets
import logging

logger = logging.getLogger(__name__)

booking_bp = Blueprint('booking', __name__)

@booking_bp.route('/book', methods=['POST'])
def book():
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No input provided"}), 400
        
    user_name = data.get('user_name')
    user_email = data.get('user_email')
    trip_name = data.get('trip_name')
    
    # Validation
    if not user_name or not user_email or not trip_name:
        return jsonify({"error": "Missing required fields (user_name, user_email, trip_name)"}), 400
        
    try:
        ticket = book_ticket(user_name, user_email, trip_name)
        return jsonify({
            "message": "Ticket booked successfully",
            "ticket": ticket
        }), 201
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        logger.error(f"Booking failed: {str(e)}")
        return jsonify({"error": "An internal error occurred"}), 500

@booking_bp.route('/tickets', methods=['GET'])
def fetch_tickets():
    try:
        tickets = get_all_tickets()
        return jsonify(tickets), 200
    except Exception as e:
        logger.error(f"Fetch tickets failed: {str(e)}")
        return jsonify({"error": "An internal error occurred"}), 500
