class Visitor:
    pass

class Guest(Visitor):
    pass

class Customer(Visitor):
    def __init__(self, customer_id: str, name: str, email: str):
        self.__customer_id = customer_id
        self.__name = name
        self.__email = email
        self.__booking_list = []  # List of Booking
        self.__ticket_list = []  # List of Ticket
        
    def cancel_ticket(self, booking_id):
        pass
        

class Member(Customer):
    def __init__(self, customer_id: str, name: str, email: str, points: int):
        super().__init__(customer_id, name, email)
        self.__points = points
        self.__payment_details = []  # List of PaymentMethod

class Regular(Customer):
    pass

class Movie:
    def __init__(self, movie_id: str, title: str, trailer: str, description: str, duration: int, genre: list):
        self.__movie_id = movie_id
        self.__title = title
        self.__trailer = trailer
        self.__description = description
        self.__duration = duration
        self.__genre = genre
        self.__showtime_list = []  # List of Showtime

class Showtime:
    def __init__(self, showtime_id: str, movie: Movie, theater, date, time, price: float):
        self.__showtime_id = showtime_id
        self.__movie = movie
        self.__theater = theater
        self.__date = date
        self.__time = time
        self.__price = price
        self.__booked_seats = []  # List of SeatBooked

class Theater:
    def __init__(self, theater_id: str, name: str):
        self.__theater_id = theater_id
        self.__name = name
        self.__seat_list = []  # List of Seat

class Seat:
    def __init__(self, seat_id: str, row: str, number: int, type: str, price: float):
        self.__seat_id = seat_id
        self.__row = row
        self.__number = number
        self.__type = type
        self.__price = price

class SeatBooked(Seat):
    def __init__(self, seat_id: str, row: str, number: int, type: str, price: float, status: str, booking_id: str):
        super().__init__(seat_id, row, number, type, price)
        self.__status = status
        self.__booking_id = booking_id

class Booking:
    def __init__(self, booking_id: str, showtime: Showtime, total_price: float, status: str, created_at):
        self.__booking_id = booking_id
        self.__showtime = showtime
        self.__selected_seats = []  # List of SeatBooked
        self.__food_list = []  # List of FoodOrder
        self.__total_price = total_price
        self.__status = status
        self.__created_at = created_at

class Food:
    def __init__(self, food_id: str, name: str, description: str, price: float, quantity: int):
        self.__food_id = food_id
        self.__name = name
        self.__description = description
        self.__price = price
        self.__quantity = quantity

class FoodOrder:
    def __init__(self, food: Food, quantity: int, subtotal: float):
        self.__food = food
        self.__quantity = quantity
        self.__subtotal = subtotal

class Ticket:
    def __init__(self, ticket_id: str, booking: Booking, seat: SeatBooked, status: str):
        self.__ticket_id = ticket_id
        self.__booking = booking
        self.__seat = seat
        self.__status = status

class QrTicket:
    def __init__(self, qr_code_id: str, content: str):
        self.__qr_code_id = qr_code_id
        self.__content = content

class Payment:
    def __init__(self, payment_id: str, booking: Booking, amount: float, method: str, status: str):
        self.__payment_id = payment_id
        self.__booking = booking
        self.__amount = amount
        self.__method = method
        self.__status = status

class QrPayment:
    def __init__(self, qr_code_id: str, expiry_time):
        self.__qr_code_id = qr_code_id
        self.__expiry_time = expiry_time

class DebitCard:
    def __init__(self, card_id: str, card_number: str, card_holder: str, expiry_date, cvv: str):
        self.__card_id = card_id
        self.__card_number = card_number
        self.__card_holder = card_holder
        self.__expiry_date = expiry_date
        self.__cvv = cvv

class CreditCard:
    def __init__(self, card_id: str, card_number: str, card_holder: str, expiry_date, cvv: str):
        self.__card_id = card_id
        self.__card_number = card_number
        self.__card_holder = card_holder
        self.__expiry_date = expiry_date
        self.__cvv = cvv

class BookingController:
    def __init__(self):
        self.__movie_list = []  # List of Movie
        self.__theater_list = []  # List of Theater
        self.__booking_list = []  # List of Booking
        self.__customer_list = []  # List of Customer
        self.__food_list = []  # List of Food
        
    def check_booking_id(self, booking_id):
        for booking in self.__booking_list:
            if booking.booking_id == booking_id:
                return booking
        return None
    
    def process_refund(self, booking):
        if booking and booking.status == "Confirmed":
            booking.status = "Refunded"
            return True
        return False
    
    def update_booking_status(self, booking_id, status):
        booking = self.check_booking_id(booking_id)
        if booking:
            booking.status = status
            return True
        return False
    
    def update_ticket_status(self, ticket_id, status):
        for customer in self.__customer_list:
            for ticket in customer.ticket_list:
                if ticket.ticket_id == ticket_id:
                    ticket.status = status
                    return True
        return False
    
    def search_movie(self, movie_name):
        result = [movie for movie in self.__movie_list if movie_name.lower() in movie.title.lower()]
        return result
    
    def check_Movie(self, movie_id):
        for movie in self.__movie_list:
            if movie.movie_id == movie_id:
                return movie
        return None
        
bookingcontroller = BookingController()
        
def create_instance(self):
        # Creating sample data
        movie = Movie("M001", "Sample Movie", "trailer_link", "Sample Description", 120, ["Action", "Drama"])
        theater = Theater("T001", "Main Theater")
        seat = Seat("S001", "A", 1, "Regular", 10.0)
        customer = Customer("C001", "John Doe", "johndoe@example.com")
        showtime = Showtime("ST001", movie, theater, "2025-02-19", "18:00", 15.0)
        booking = Booking("B001", showtime, 30.0, "Confirmed", "2025-02-19T17:00:00")
        food = Food("F001", "Popcorn", "Large Popcorn", 5.0, 50)
        food_order = FoodOrder(food, 2, 10.0)
        payment = Payment("P001", booking, 30.0, "CreditCard", "Paid")
        ticket = Ticket("T001", booking, seat, "Valid")
        
        
        
