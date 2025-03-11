import uuid
import random
import time
from io import BytesIO
import base64
from datetime import datetime

# ================================ CLASSES ======================================================
class BookingController:
    def __init__(self):
        self.__movie_list = []  # List of Movie
        self.__theater_list = []  # List of Theater
        self.__booking_list = []  # List of Booking
        self.__customer_list = []  # List of Customer
        self.__food_list = []  # List of Food
    
    @property
    def movie_list(self):
        return self.__movie_list
    
    @property
    def booking_list(self):
        return self.__booking_list
    
    @property
    def customer_list(self):
        return self.__customer_list
    
    @property
    def food_list(self):
        return self.__food_list
    
    def get_all_movies(self):
        return self.__movie_list
    
    def add_booking(self, booking):
        self.__booking_list.append(booking)

    def cancel_booking(self, booking):
        self.__booking_list.remove(booking)
    
    def get_customer_bookings(self, customer):
        return [booking for booking in self.__booking_list if booking.customer == customer]
    
    def get_booking_id(self, booking_id):
        for booking in self.__booking_list:
            if booking.get_booking_id() == booking_id:
                return booking
        return None
    
    def select_movie(self, movie_id):
        return next((movie for movie in self.__movie_list if movie.movie_id == movie_id), None)
    
    def select_showtime(self, showtime_id):
        return next((showtime for movie in self.__movie_list for showtime in movie.get_showtimes() if showtime.id == showtime_id), None)
    
    def choose_seats(self, showtime, seats):
        return showtime.get_available_seats()[:seats]
    
    def confirm_booking(self, customer, showtime, seats, food_items):
        booking = Booking(
            booking_id=f"BK{uuid.uuid4().hex[:8].upper()}", 
            showtime=showtime, 
            total_price=0,  # Should calculate based on seats and food
            status="Pending",
            created_at=datetime.now()
        )
        self.add_booking(booking)
        return booking
    
    def search_movie(self, movie_name):
        result = [movie for movie in self.__movie_list if movie_name.lower() in movie.name.lower()]
        return result
        
    def check_booking_id(self, booking_id):
        booking = self.get_booking_id(booking_id)
        if booking:
            return booking
        else:
            return "Booking ID not found"
    
    def check_customer_id(self, customer_id):
        for customer in self.__customer_list:
            if customer.customer_id == customer_id:
                return customer
        return None
    
    def process_refund(self, booking):
        if booking and booking.status == "Confirmed":
            booking.status = "Refunded"
            return True
        return False
    
    def update_booking_status(self, booking_id, status):
        booking = self.check_booking_id(booking_id)
        if isinstance(booking, Booking):
            if status == "success":
                booking.status = "Confirmed"
                # Update seat status
                return True
            else:
                booking.status = "Cancelled"
                # Update seat status
                return True
        return False
    
    def update_ticket_status(self, ticket_id, status):
        for customer in self.__customer_list:
            for ticket in customer.ticket_list:
                if ticket.ticket_id == ticket_id:
                    ticket.status = status
                    return True
        return False
    
    def check_Movie(self, movie_id):
        for movie in self.__movie_list:
            if movie.movie_id == movie_id:
                return movie
        return None
    
    def create_booking(self, showtime, seats, total_price):
        booking_id = f"BK{uuid.uuid4().hex[:8].upper()}"
        booking = Booking(
            booking_id=booking_id, 
            showtime=showtime, 
            total_price=total_price,
            status="Pending",
            created_at=datetime.now()
        )
        self.__booking_list.append(booking)
        return booking
    
    def append_movie(self, movie):
        self.__movie_list.append(movie)

    def append_theater(self, theater):
        self.__theater_list.append(theater)

    def append_booking(self, booking):
        self.__booking_list.append(booking)

    def append_customer(self, customer):
        self.__customer_list.append(customer)

    def append_food(self, food):
        self.__food_list.append(food)

    def append_seat_booked(self, seat_booked):
        if not hasattr(self, '_BookingController__seat_bookings'):
            self._BookingController__seat_bookings = []
        self._BookingController__seat_bookings.append(seat_booked)
        return seat_booked

    def get_booked_seats(self, showtime_id):
        booked_seats = []
        # Check if seat_bookings attribute exists
        if hasattr(self, '_BookingController__seat_bookings'):
            for booking in self.__booking_list:
                if booking.showtime.id == showtime_id and booking.status != "Cancelled":
                    booked_seats.extend(booking.seats)
        return booked_seats
    
    #new
    def find_customer_by_email(self, email: str):
        """Find a customer by their email address"""
        return next((customer for customer in self.__customer_list 
                    if customer.email == email), None)
    
    def find_customer_by_id(self, customer_id: str):
        """Find a customer by their ID"""
        return next((customer for customer in self.__customer_list 
                    if customer.customer_id == customer_id), None)
    
    def authenticate_customer(self, email: str, password: str):
        """Authenticate a customer with email and password"""
        customer = self.find_customer_by_email(email)
        if customer and customer.compare_password(password):
            return customer
        return None
    
    def create_customer(self, name: str, email: str, password: str):
        """Create a new customer account"""
        # Generate new customer ID
        customer_id = f"C{len(self.__customer_list) + 1:03d}"
        
        # Create new customer
        new_customer = Customer(customer_id, name, email, password)
        self.__customer_list.append(new_customer)
        return new_customer
    
    def get_customer_bookings(self, customer_id: str) -> list:
        """Get all bookings for a specific customer"""
        return [booking for booking in self.__booking_list 
                if booking.customer.customer_id == customer_id]
    
    def append_customer(self, customer):
        """Add a new customer to the system"""
        try:
            print(f"[DEBUG] Adding customer: {customer.name} ({customer.email})")
            self.__customer_list.append(customer)
            print(f"[DEBUG] Customer added successfully. Total customers: {len(self.__customer_list)}")
            return True
        except Exception as e:
            print(f"[DEBUG] Error adding customer: {str(e)}")
            return False

    def find_customer_by_email(self, email):
        """Find a customer by their email address"""
        return next((customer for customer in self.__customer_list 
                    if customer.email.lower() == email.lower()), None)

    def find_customer_by_id(self, customer_id):
        """Find a customer by their ID"""
        return next((customer for customer in self.__customer_list 
                    if str(customer.customer_id) == str(customer_id)), None)

class Movie:
    next_id = 1
    def __init__(self, name, genre, year, duration, description, image_url=None, trailer_url=None):
        self.__movie_id = Movie.next_id
        self.__name = name
        self.__genre = genre
        self.__year = year
        self.__duration = duration
        self.__description = description
        self.__image_url = image_url or "https://placehold.co/300x450"
        self.__showtimes = []  # Store showtimes for the movie
        self.__trailer_url = trailer_url
        Movie.next_id += 1
        
    @property
    def trailer_url(self):
        return self.__trailer_url if hasattr(self, "_Movie__trailer_url") else '#'
    
    @property
    def movie_id(self):
        return self.__movie_id
    
    @property
    def name(self):
        return self.__name
    
    @property
    def genre(self):
        return self.__genre
    
    @property
    def year(self):
        return self.__year
    
    @property
    def duration(self):
        return self.__duration  # Fixed: was returning movie_id
    
    @property
    def description(self):
        return self.__description
    
    @property
    def image_url(self):
        return self.__image_url
    
    def add_showtime(self, showtime):
        self.__showtimes.append(showtime)
    
    def get_showtimes(self):
        return self.__showtimes

class Theater:
    def __init__(self, name, total_seats=70):
        self.__name = name
        self.__seats = [f"S{i}" for i in range(1, total_seats + 1)]
    
    @property
    def name(self):
        return self.__name
    
    def get_seat_map(self):
        return self.__seats

class Showtime:
    next_id = 1
    def __init__(self, movie, time, theater):
        self.__id = Showtime.next_id
        self.__movie = movie
        self.__time = time
        self.__theater = theater
        self.__booked_seats = set()  # Track booked seats
        Showtime.next_id += 1
    
    @property
    def id(self):
        return self.__id
    
    @property
    def movie(self):
        return self.__movie
    
    @property
    def time(self):
        return self.__time
    
    @property
    def theater(self):
        return self.__theater
    
    def get_available_seats(self):
        return [seat for seat in self.__theater.get_seat_map() if seat not in self.__booked_seats]

class Booking:
    def __init__(self, booking_id: str, customer, showtime, seats=None, status="Pending"):
        self.__booking_id = booking_id
        self.__customer = customer
        self.__showtime = showtime
        self.__seats = seats or []
        self.__food_orders = []  # Ensure a separate list for food
        self.__status = status
        self.__created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.__total_price = 0.0  # Default to 0, calculated dynamically

    def calculate_total_price(self):
        """Calculate total price including seats and food"""
        seat_total = len(self.__seats) * 10.0  # Assuming $10 per seat
        food_total = sum(food_order.calculate_subtotal() for food_order in self.__food_orders)
        self.__total_price = seat_total + food_total
        return self.__total_price


    def get_booking_id(self):
        return self.__booking_id
    
    @property
    def total_price(self):
        return self.__total_price
    
    @property
    def booking_id(self):
        return self.__booking_id
    
    @property
    def customer(self):
        return self.__customer
        
    @property
    def showtime(self):
        return self.__showtime
    
    @property
    def seats(self):
        return self.__seats
        
    @property    
    def status(self):
        return self.__status

    @property
    def timestamp(self):
        return self.__created_at
        
    @property
    def food_total(self):
        if not hasattr(self, 'food_orders') or not self.food_orders:
            return 0.0
        return sum(float(order.food.price) * order.quantity for order in self.food_orders)
        
    @status.setter
    def status(self, new_status):
        self.__status = new_status
    
    def add_seat(self, seat):
        """Add a seat and recalculate total price"""
        self.__seats.append(seat)
        self.calculate_total_price()  # Ensure price updates
            
    
    def add_food_order(self, food_order):
        """Add food and recalculate total price"""
        self.__food_orders.append(food_order)
        self.calculate_total_price()  # Ensure price updates

    
    def confirm_booking(self):
        self.__status = "Confirmed"
        return True
    
    def cancel_booking(self):
        self.__status = "Cancelled"
        return True
    
    
class Food:
    def __init__(self, food_id: str, name: str, description: str, price: float, quantity: int):
        self.__food_id = food_id
        self.__name = name
        self.__description = description
        self.__price = price
        self.__quantity = quantity
    
    @property
    def food_id(self):
        return self.__food_id
    
    @property
    def name(self):
        return self.__name
    
    @property
    def description(self):
        return self.__description
    
    @property
    def price(self):
        return self.__price
    
    @property
    def quantity(self):
        return self.__quantity
    
    @property
    def is_available(self):
        return self.__quantity > 0
    
    def update_quantity(self, amount):
        if self.__quantity - amount >= 0:
            self.__quantity -= amount
            return True
        return False

class FoodOrder:
    def __init__(self, food, quantity):
        self.__food = food
        self.__quantity = quantity
        self.__subtotal = self.calculate_subtotal()  # Ensure correct subtotal
        
    @property
    def food(self):
        return self.__food
    
    @property
    def quantity(self):
        return self.__quantity
    
    @property
    def subtotal(self):
        return self.calculate_subtotal()
        
    def update_quantity(self, new_quantity):
        if self.__food.update_quantity(new_quantity - self.__quantity):
            self.__quantity = new_quantity
            self.__subtotal = self.calculate_subtotal()
            return True
        return False
    
    def calculate_subtotal(self):
        return self.__food.price * self.__quantity
    
class Payment:
    def __init__(self, payment_id: str, booking: Booking, amount: float, method: str, status: str = "Pending"):
        self.__payment_id = payment_id
        self.__booking = booking
        self.__amount = amount
        self.__method = method
        self.__status = status
        
    @property
    def method(self):
        return self.__method
    
    @property
    def status(self):
        return self.__status
    
    @status.setter
    def status(self, new_status):
        self.__status = new_status
    
    @property
    def amount(self):
        return self.__amount
        
    def make_payment(self, payment_method, booking_controller):
        start_time = time.time()
        timeout = 60
        
        if isinstance(payment_method, Card):
            validated_card = payment_method.validate_Card()
            if validated_card:
                result = self.process_payment(payment_method, booking_controller, start_time, timeout)
            else:
                result = "unsuccess"
        
        elif isinstance(payment_method, QrPayment):
            qr_code = payment_method.generate_qr_code(self.__amount)
            if qr_code:
                result = payment_method.verify_payment()
            else:
                result = "unsuccess"
        
        return result
        
    def process_payment(self, payment_method, booking_controller, start_time, timeout):
        if time.time() - start_time > timeout:
            result = self.cancel_payment(booking_controller)
            return result
        
        if isinstance(payment_method, Card):
            if payment_method.charge_card(self.__amount) == True:
                self.__status = "Success"
                result = booking_controller.update_booking_status(self.__booking.get_booking_id(), "success")
                return result
            else:
                self.__status = "Failed"
                result = booking_controller.update_booking_status(self.__booking.get_booking_id(), "unsuccess")
                return result
            
    def cancel_payment(self, booking_controller):
        cancel_status = booking_controller.update_booking_status(self.__booking.get_booking_id(), "unsuccess")
        return cancel_status
    
    def validate_payment(self):
        # Validate if payment is valid
        return self.__status == "Success"
    
class QrPayment:
    def __init__(self, qr_code_id: str, expiry_time):
        self.__qr_code_id = qr_code_id
        self.__expiry_time = expiry_time
        
    def generate_qr_code(self, amount):
        payment_data = f"CE_ISAN_PAYMENT:{self.__qr_code_id}:{amount or 0}"
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(payment_data)
        qr.make(fit=True)
    
        img = qr.make_image(fill_color="black", back_color="white")
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        return f"data:image/png;base64,{img_str}"

    def verify_payment(self):
        return random.choice([True, False])
    
    def check_expiry_time(self):
        current_time = datetime.now().timestamp()
        return current_time < self.__expiry_time

class QrTicket:
    def __init__(self, qr_code_id: str, content: str):
        self.__qr_code_id = qr_code_id
        self.__content = content
    
    def generate(self):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(self.__content)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        return f"data:image/png;base64,{img_str}"
    
    def validate(self):
        # Validate the ticket QR code
        return True

class Card:
    def __init__(self, card_id: str, card_number: str, card_holder: str, expiry_date, cvv: str):
        self.__card_id = card_id
        self.__card_number = card_number
        self.__card_holder = card_holder
        self.__expiry_date = expiry_date
        self.__cvv = cvv
     
    def validate_Card(self):
        if len(self.__card_number.replace(" ", "")) == 16 and len(self.__cvv) == 3:
            return True
        return False
    
    def charge_card(self, amount):
        return random.choice([True, False])
    
class Seat:
    def __init__(self, seat_id, row, number, type, price):
        self.__seat_id = f"{row}{number}"
        self.__row = row
        self.__number = number
        self.__type = type
        self.__price = price
        self.__is_booked = False
        self.__status = "available"
    
    @property
    def seat_id(self):
        return self.__seat_id
    
    @property
    def row(self):
        return self.__row
    
    @property
    def number(self):
        return self.__number
    
    @property
    def type(self):
        return self.__type
    
    @property
    def price(self):
        return self.__price
    
    @property
    def is_booked(self):
        return self.__is_booked
    
    @property
    def status(self):
        return self.__status
    
    def book(self):
        """Mark the seat as booked"""
        if self.__status == "available":
            self.__status = "booked"
            self.__is_booked = True
            return True  # Booking successful
        return False  # Seat already booked

class SeatBooked:
    def __init__(self, seat_id, booking, seat_number):
        self.__seat_id = seat_id  # Unique ID for this seat booking
        self.__booking = booking  # Reference to the booking
        self.__seat_number = seat_number  # Seat identifier (e.g., "A1")
        self.__status = "reserved"  # Initial status when created
        
    @property
    def seat_id(self):
        return self.__seat_id
    
    @property
    def booking(self):
        return self.__booking
    
    @property
    def seat_number(self):
        return self.__seat_number
    
    @property
    def status(self):
        return self.__status
    
    @status.setter
    def status(self, new_status):
        self.__status = new_status
    
    def update_status(self, booking_status):
        """Update seat status based on booking status"""
        if booking_status == "success" or booking_status == "Confirmed":
            self.__status = "booked"
            return "payment success"
        elif booking_status == "unsuccess" or booking_status == "Cancelled":
            self.__status = "available"
            return "payment unsuccess"
        return "status unchanged"

class Ticket:
    def __init__(self, ticket_id: str, booking: Booking, seat: SeatBooked):
        self.__ticket_id = ticket_id
        self.__booking = booking
        self.__seat = seat
        self.__status = "available"
  
    @property
    def ticket_id(self):
        return self.__ticket_id
    
    @property
    def status(self):
        return self.__status
    
    @status.setter
    def status(self, new_status):
        self.__status = new_status
    
    def generate_barcode(self):
        # Generate barcode for the ticket
        pass
    
    def validate(self):
        # Validate if ticket is valid
        return self.__status == "available"
    
    def cancel_ticket(self):
        self.__status = "cancelled"
        return True
    
    def use_ticket(self):
        self.__status = "used"
        return True
    
    def generate_ticket(self):
        # Generate ticket details
        return {
            "ticket_id": self.__ticket_id,
            "booking": self.__booking.get_booking_id(),
            "seat": self.__seat.seat_id,
            "status": self.__status
        }
    
    def send_ticket(self):
        # Send ticket to customer
        pass
    
# class Visitor:
#     def __init__(self, name: str):
#         self.__name = name
        
#     @property
#     def name(self):
#         return self.__name
        
#     def search_movie(self, booking_controller, movie_name):
#         return booking_controller.search_movie(movie_name)    
    
#     def view_movie_details(self, movie):
#         # View details of a movie
#         return {
#             "name": movie.name,
#             "genre": movie.genre,
#             "year": movie.year,
#             "duration": movie.duration,
#             "description": movie.description
#         }
    
#     def view_showtimes(self, movie):
#         # View showtimes of a movie
#         return movie.get_showtimes()
    
# class Guest(Visitor):
#     def register(self, customer_id, name, email, password):
#         return Customer(customer_id, name, email, password)
    
#     def login(self, email, password, booking_controller):
#         for customer in booking_controller.customer_list:
#             if customer.__email == email and customer.compare_password(password):
#                 return customer
#         return None
    
# class Customer(Visitor):
#     def __init__(self, customer_id: str, name: str, email: str, password: str):
#         super().__init__(name)
#         self.__customer_id = customer_id
#         self.__email = email
#         self.__password = password
#         self.__booking_list = []
#         self.__ticket_list = []
    
#     @property
#     def password(self):
#         return self.__password

#     @property
#     def customer_id(self):
#         return self.__customer_id
    
#     @property
#     def email(self):
#         return self.__email
    
#     @property
#     def ticket_list(self):
#         return self.__ticket_list
    
#     def check_password(self, password_to_check):
#         return self.__password == password_to_check
    
#     def book_ticket(self, booking_controller, showtime, seats, food_items=None):
#         food_items = food_items or []
#         booking = booking_controller.confirm_booking(self, showtime, seats, food_items)
#         self.__booking_list.append(booking)
#         return booking
    
#     def cancel_ticket(self, booking_controller, booking_id):
#         booking = booking_controller.get_booking_id(booking_id)
#         if booking:
#             result = booking_controller.cancel_booking(booking)
#             if result:
#                 self.__booking_list.remove(booking)
#                 return True
#         return False
    
#     def view_booking_history(self):
#         return self.__booking_list
    
#     def view_tickets(self):
#         return self.__ticket_list
    
#     def sign_out(self):
#         # Sign out logic
#         return True

class Guest:
    def __init__(self, name: str = "Guest"):
        self.__name = name
    
    @property
    def name(self):
        return self.__name
    
    def search_movie(self, booking_controller, movie_name):
        return booking_controller.search_movie(movie_name)    
    
    def view_movie_details(self, movie):
        return {
            "name": movie.name,
            "genre": movie.genre,
            "year": movie.year,
            "duration": movie.duration,
            "description": movie.description
        }
    
    def view_showtimes(self, movie):
        return movie.get_showtimes()
    
    def register(self, booking_controller, name, email, password):
        new_id = f"C{len(booking_controller.customer_list) + 1:03d}"
        new_customer = Customer(new_id, name, email, password)
        booking_controller.append_customer(new_customer)
        print(f"[DEBUG] Registered Customer: {new_customer.name}, {new_customer.email}")
        return new_customer

    
    def login(self, email, password, booking_controller):
        for customer in booking_controller.customer_list:
            if customer.email == email and customer.check_password(password):
                return customer
        return None
    
    def register(self, booking_controller, name: str, email: str, password: str):
        """Register a new customer account"""
        try:
            # Check if email already exists
            if booking_controller.find_customer_by_email(email):
                print(f"[DEBUG] Email already exists: {email}")
                return None
                
            # Generate new customer ID
            customer_id = f"C{len(booking_controller.customer_list) + 1:03d}"
            
            # Create new customer
            new_customer = Customer(customer_id, name, email, password)
            
            # Add to booking controller
            if booking_controller.append_customer(new_customer):
                print(f"[DEBUG] Successfully registered customer: {name}")
                return new_customer
            
            return None
            
        except Exception as e:
            print(f"[DEBUG] Error during registration: {str(e)}")
            return None

class Customer:
    def __init__(self, customer_id: str, name: str, email: str, password: str):
        self.__customer_id = customer_id
        self.__name = name
        self.__email = email
        self.__password = password
        self.__booking_list = []
        self.__ticket_list = []
        self.__points = 0

    @property
    def points(self):
        return self.__points
    
    @property
    def name(self):
        return self.__name
    
    @property
    def password(self):
        return self.__password

    @property
    def customer_id(self):
        return self.__customer_id
    
    @property
    def email(self):
        return self.__email
    
    @property
    def ticket_list(self):
        return self.__ticket_list
    
    @property
    def booking_list(self):
        return self.__booking_list
    
    def compare_password(self, password_to_check):
        """Verify if the provided password matches the stored password"""
        return self.__password == password_to_check
    
    def search_movie(self, booking_controller, movie_name):
        return booking_controller.search_movie(movie_name)
    
    def view_movie_details(self, movie):
        return {
            "name": movie.name,
            "genre": movie.genre,
            "year": movie.year,
            "duration": movie.duration,
            "description": movie.description
        }
    
    def check_password(self, password_to_check: str) -> bool:
        """Verify if the provided password matches"""
        return self.__password == password_to_check
    
    def add_booking(self, booking):
        """Add a booking to the customer's booking list"""
        self.__booking_list.append(booking)
        print(f"[DEBUG] Added booking {booking.booking_id} to customer {self.customer_id}")
    
    def view_showtimes(self, movie):
        return movie.get_showtimes()
    
    def book_ticket(self, booking_controller, showtime, seats, food_items=None):
        food_items = food_items or []
        booking = booking_controller.confirm_booking(self, showtime, seats, food_items)
        self.__booking_list.append(booking)
        return booking
    
    def cancel_ticket(self, booking_controller, booking_id):
        booking = booking_controller.get_booking_id(booking_id)
        if booking:
            result = booking_controller.cancel_booking(booking)
            if result:
                self.__booking_list.remove(booking)
                return True
        return False
    
    def view_booking_history(self):
        return self.__booking_list
    
    def view_tickets(self):
        return self.__ticket_list
    
    def sign_out(self):
        return True
    
    def redeem_points(self, amount):
        if self.__points >= amount:
            self.__points -= amount
            return True
        return False
    
    def earn_points(self, amount):
        self.__points += amount
        return self.__points
    
    def get_points_balance(self):
        return self.__points
    
    def customer_to_member(self, birthday: str = None):
        return Member(self.__customer_id, self.__name, self.__email, self.__password, self.__points, birthday)
    
class Member(Customer):
    def __init__(self, customer_id: str, name: str, email: str, password: str, points: int = 0, birthday: str = None):
        super().__init__(customer_id, name, email, password)
        self.__points = points
        self.__payment_details = []
        self.__birthday = birthday
    
    @property
    def birthday(self):
        return self.__birthday
    
    @birthday.setter
    def birthday(self, value):
        self.__birthday = value
    
    # Override these methods to use the Member's __points attribute
    def redeem_points(self, amount):
        if self.__points >= amount:
            self.__points -= amount
            return True
        return False
    
    def earn_points(self, amount):
        # Members earn 3x points
        self.__points += amount
        return self.__points
    
    def get_points_balance(self):
        return self.__points


    