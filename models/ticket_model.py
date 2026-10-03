import datetime

class TicketModel:
    def __init__(self, user_name, user_email, trip_name, price):
        self.user_name = user_name
        self.user_email = user_email
        self.trip_name = trip_name
        self.price = price
        self.status = "BOOKED"
        self.created_at = datetime.datetime.utcnow().isoformat()

    def to_dict(self):
        return {
            "user_name": self.user_name,
            "user_email": self.user_email,
            "trip_name": self.trip_name,
            "price": self.price,
            "status": self.status,
            "created_at": self.created_at
        }
