from config.firebase_config import get_db
from models.ticket_model import TicketModel
import logging

logger = logging.getLogger(__name__)

TICKET_PRICES = {
    "Downtown Express": 2.50,
    "City Loop": 3.00,
    "Suburbs Route": 5.00,
    "Airport Shuttle": 15.00
}

def get_price_for_trip(trip_name):
    return TICKET_PRICES.get(trip_name, 0.0)

def book_ticket(user_name, user_email, trip_name):
    try:
        db = get_db()
        tickets_ref = db.collection('tickets')
        
        # Check for duplicate bookings (same email + same trip)
        query = tickets_ref.where('user_email', '==', user_email).where('trip_name', '==', trip_name).stream()
        
        for doc in query:
            raise ValueError(f"User {user_email} already has a ticket for {trip_name}")
            
        price = get_price_for_trip(trip_name)
        if price <= 0:
            raise ValueError("Invalid trip selected")
            
        ticket = TicketModel(user_name, user_email, trip_name, price)
        
        # Save to DB
        _, doc_ref = tickets_ref.add(ticket.to_dict())
        logger.info(f"Ticket {doc_ref.id} booked successfully for {user_email}")
        
        result = ticket.to_dict()
        result['id'] = doc_ref.id
        return result
        
    except ValueError as ve:
        logger.warning(f"Validation error during booking: {ve}")
        raise ve
    except Exception as e:
        logger.error(f"Error booking ticket: {e}")
        raise Exception("Failed to book ticket due to internal error")

def get_all_tickets():
    try:
        db = get_db()
        tickets_ref = db.collection('tickets')
        
        # Note: Order by requires index in Firestore
        docs = tickets_ref.order_by('created_at', direction='DESCENDING').stream()
        
        tickets = []
        for doc in docs:
            ticket_data = doc.to_dict()
            ticket_data['id'] = doc.id
            tickets.append(ticket_data)
            
        return tickets
    except Exception as e:
        logger.error(f"Error fetching tickets: {e}")
        # fallback to unordered fetch if index is missing in development
        try:
            db = get_db()
            docs = db.collection('tickets').stream()
            tickets = []
            for doc in docs:
                data = doc.to_dict()
                data['id'] = doc.id
                tickets.append(data)
            # Sort manually for now
            return sorted(tickets, key=lambda x: x.get('created_at', ''), reverse=True)
        except Exception as inner_e:
            raise Exception("Failed to fetch tickets")
