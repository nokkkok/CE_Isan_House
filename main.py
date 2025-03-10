from fasthtml.common import *
from datetime import datetime
from typing import List
import time
import random
import uuid
import qrcode
import base64
from io import BytesIO

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
    
    def get_all_movies(self): #this or just take from movie_list?
        yield from get.movie_list
    
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
        return next((movie for movie in self.__movie_list if movie.id == movie_id), None)
    
    def select_showtime(self, showtime_id):
        return next((showtime for movie in self.__movie_list for showtime in movie.get_showtimes() if showtime.id == showtime_id), None)
    
    def choose_seats(self, showtime, seats):
        return showtime.get_available_seats()[:seats]
    
    def confirm_booking(self, customer, showtime, seats, food_items):
        booking = Booking(customer, showtime, seats, food_items)
        self.add_booking(booking)
        return booking
    
    def search_movie(self, movie_name):
        result = [movie for movie in self.__movie_list if movie_name.lower() in movie.title.lower()]
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
        booking = Booking(booking_id, showtime, total_price)
        self.__booking_list.append(booking)
        return booking
    
    def process_refund(self, booking):
        if booking and booking.status == "Confirmed":
            booking.status = "Refunded"
            return True
        return False
    
    def update_ticket_status(self, ticket_id, status):
        for customer in self.__customer_list:
            for ticket in customer.ticket_list:
                if ticket.ticket_id == ticket_id:
                    ticket.status = status
                    return True
        return False
    
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

class Movie:
    next_id = 1
    def __init__(self, name, genre, year, duration, description, image_url=None):
        self.__movie_id = Movie.next_id
        self.__name = name
        self.__genre = genre
        self.__year = year
        self.__duration = duration
        self.__description = description
        self.__image_url = image_url or "https://placehold.co/300x450"
        self.__showtimes = []  # Store showtimes for the movie
        Movie.next_id += 1
        
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
        return self.__movie_id
    
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
    def __init__(self, booking_id: str, showtime: Showtime, total_price: float, status: str, created_at):
        self.__booking_id = booking_id
        self.__showtime = showtime
        self.__selected_seats = []  # List of SeatBooked
        self.__food_list = []  # List of FoodOrder
        self.__total_price = total_price
        self.__status = status
        self.__created_at = datetime.now()

    def get_booking_id(self):
        return self.__booking_id

    @property    
    def status(self):
        return self.__status

    @status.setter
    def status(self, new_status):
        self.__status = new_status
    
    @property
    def total_price(self):
        return self.__total_price
    
    def calculate_total_price(self):
    # Calculate total price based on seats and food
        pass
    
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
    
    # if food ordered < quantity -> is_available = True
    @property
    def is_available(self):
        pass
    
    # TODO update class diagram
    def update_quantity(self):
        pass

class FoodOrder:
    def __init__(self, food: Food, quantity: int):
        self.__food = food
        self.__quantity = quantity
        self.__subtotal = 0 #calculate_subtotal(food.__price, quantity)
        
    def update_quantity(self):
        pass
    
    def calculate_subtotal(self):
        pass
    
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
        pass
    
    def get_status(self):
        return self.__status
    
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

class QrTicket: #?
    def __init__(self, qr_code_id: str, content: str):
        self.__qr_code_id = qr_code_id
        self.__content = content
    
    def generate():
        pass
    
    def validate():
        pass

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
    
    def book(self):
        """Mark the seat as booked"""
        if self.__status == "available":
            self.__status = "booked"
            return True  # Booking successful
        return False  # Seat already booked

class SeatBooked(Seat):
    def __init__(self, seat_id: str, row: str, number: int, type: str, price: float, status: str, booking_id: str):
        super().__init__(seat_id, row, number, type, price)
        self.__booking_id = booking_id
        self.__status = status
    
    @property
    def status(self):
        return self.__status
    
    @status.setter
    def status(self, new_status):
        self.__status = new_status
    
    def update_status(self, booking_status):
        if booking_status == "success":
            self.__status = "unavailable"
            return "payment success"
        else:
            self.__status = "available"
            return "payment unsuccess"
        
    @property
    def booking_id(self):
        return self.__booking_id
    
    def reserve_seats(self): 
        self.__status = "reserved"
        return True
    
class Theater:
    def __init__(self, name, total_seats=30):
        self.__name = name
        self.__seats = [f"S{i}" for i in range(1, total_seats + 1)]
    
    @property
    def name(self):
        return self.__name
    
    def get_seat_map(self):
        return self.__seats

class Ticket:
    def __init__(self, ticket_id: str, booking: Booking, seat: SeatBooked):
        self.__ticket_id = ticket_id
        self.__booking = booking
        self.__seat = seat
        self.__status = "available"
  
    def generate_barcode(self):
        pass
    
    # what for?
    def validate():
        pass
    
    # TODO update class diagram
    def cancel_ticket(self):
        self__status = "cancelled"
    
    def use_ticket(self):
        self.__status = "used"
    
    # what
    def generate_ticket(self):
        pass
    
    def send_ticket():
        pass
    
class Visitor:
    def __init__(self, name: str):
        self.__name = name
        
    def search_movie(self, booking_controller, movie_name):
        return booking_controller.search_movie(movie_name)    
    
    def view_movie_details():
        pass
    
    def view_showtimes():
        pass
    
class Guest(Visitor):
    def register():
        pass
    
    def login():
        pass
    
class Customer(Visitor):
    def __init__(self, customer_id: str, name: str, email: str, password: str):
        self.__customer_id = customer_id
        self.__name = name
        self.__email = email
        self.__password = password
        self.__booking_list = []
        self.__ticket_list = []
    
    @properties
    def customer_id(self):
        return self.__customer_id
    
    def compare_password(self, password):
        if self.__password == password:
            return True
        else: return False
    
    def book_ticket():
        pass
    
    def cancel_ticket():
        pass
    
    def view_booking_history():
        pass
    
    def view_tickets():
        pass
    
    def sign_out():
        pass
    
class Regular(Customer):
    def upgrade_membership():
        pass
    
class Member(Customer):
    def __init__(self, customer_id: str, name: str, email: str, points: int):
        super().__init__(customer_id, name, email)
        self.__points = points
        self.__payment_details = []
        
    def redeem_points():
        pass
    
    def earn_points():
        pass
    
    def get_points_balance():
        pass
# ==================================================================================================

# ================================ INSTANCES =======================================================
booking_controller = BookingController()
movies = [
    #pentor
    Movie("Decision to Leave", "Mystery", 2022, "90", "A detective investigating a man's death falls for the man's mysterious wife.", "Images/decision_to_leave.jpg"),
    Movie("Burning", "Drama", 2018, "90", "A mysterious thriller about a young deliveryman, his childhood friend, and a rich stranger.", "Images/burning.jpg"),
    Movie("Past Lives", "Drama", 2023, "90", "A woman is reunited with her childhood friend and first love while her American husband watches on.", "Images/past_lives.jpg"),
    Movie("After Yang", "Science Fiction", "90", 2021, "A father and daughter try to save their robot family member.", "Images/after_yang.jpg"),
    Movie("12 Angry Men", "Drama", 1957, "90", "A jury of 12 men must decide the fate of a young man accused of murder.", "Images/12_angry_men.jpg"),
    Movie("Memories of Murder", "Crime", "90", 2003, "Detectives struggle to catch a serial killer in rural South Korea in the 1980s.", "Images/memories_of_murder.jpg"),
    Movie("Dune", "Science Fiction", "90", 2021, "A noble family becomes embroiled in a war for control over the galaxy's most valuable resource.", "Images/dune.jpg"),
    Movie("Spirited Away", "Fantasy", "90", 2001, "A young girl enters a world of spirits and must work to free herself and her parents.", "Images/spirited_away.jpg"),
    Movie("The Apothecary Diaries", "Fantasy", "90", 2020, "A young girl enters a world of spirits and must work to free herself and her parents.", "Images/theapothecarydiaries.webp")
    ]

def create_instance():
    customer = Customer("C001", "John Doe", "johndoe@example.com", "1234")
    food = Food("F001", "Popcorn", "Large Popcorn", 5.0, 50)
    
    theater1 = Theater("Theator 1") #pentor
    movies[0].add_showtime(Showtime(movies[0], "18:00", theater1)) #pentor
    movies[0].add_showtime(Showtime(movies[0], "20:30", theater1)) #pentor
    movies[1].add_showtime(Showtime(movies[1], "16:45", theater1)) #pentor
    
    for movie in movies:
        booking_controller.append_movie(movie)

    booking_controller.append_theater(theater1) #pentor
    booking_controller.append_customer(customer)
    booking_controller.append_food(food)

createInstance = create_instance()
# ===============================================================================================

# Create the FastHTML app with top navigation and hamburger menu
app, rt = fast_app(
    debug=True, live=True,
    hdrs=(
        picolink,
        # Add custom styles directly
        Style("""
        /* Top Navigation Bar */
        .top-navbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background-color: #333;
            color: white;
            padding: 15px 20px;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            z-index: 1000;
        }

        .top-navbar-brand {
            color: white;
            font-size: 1.5rem;
            font-weight: bold;
            text-decoration: none;
        }

        .top-navbar-menu {
            display: flex;
            list-style: none;
            margin: 0;
            padding: 0;
        }

        .top-navbar-menu li {
            margin-left: 20px;
        }

        .top-navbar-menu li a {
            color: white;
            text-decoration: none;
        }

        .top-navbar-menu li a:hover {
            text-decoration: underline;
        }

        /* Hamburger Menu */
        .hamburger-btn {
            background: none;
            border: none;
            color: white;
            font-size: 1.5rem;
            cursor: pointer;
            z-index: 1100;
        }

        .sidebar {
            position: fixed;
            top: 0;
            right: -300px;
            width: 300px;
            height: 100%;
            background-color: white;
            transition: right 0.3s ease-in-out;
            box-shadow: -2px 0 5px rgba(0,0,0,0.1);
            z-index: 1001;
            padding: 20px;
        }

        .sidebar.open {
            right: 0;
        }

        .sidebar-menu {
            list-style: none;
            padding: 0;
        }

        .sidebar-menu li {
            margin-bottom: 15px;
        }

        .sidebar-menu li a {
            text-decoration: none;
            color: #333;
            font-size: 1.1rem;
        }

        .overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.5);
            display: none;
            z-index: 999;
        }

        .overlay.open {
            display: block;
        }

        /* Adjust body to prevent content being hidden behind navbar */
        body {
            padding-top: 70px;
        }
        """),
        # Add JavaScript for menu toggle
        Script("""
        function toggleMenu() {
            var sidebar = document.querySelector('.sidebar');
            var overlay = document.querySelector('.overlay');
            sidebar.classList.toggle('open');
            overlay.classList.toggle('open');
        }
        """)
    )
)

def MovieCard(movie : Movie): #cat
    return Card(
        Div(
            Img(src=movie.image_url, alt=movie.name),
            header = H3(movie.name),
            body = Div(
                P(f"Duration: {movie.duration} mins"),
                A("View Details", href=f"/movie/{movie.movie_id}", cls="secondary")
            )
        )
    )

# Function to create common page structure
def create_page_structure(content):
    return [
        # Top Navigation Bar #
        Nav(
            A("Movie Theater", href="/", cls="top-navbar-brand"),
            # Hamburger Menu Button
            Button("☰", onclick="toggleMenu()", cls="hamburger-btn"),
            cls="top-navbar"
        ),

        # Sidebar Menu
        Div(
            H3("Menu"),
            Ul(
                Li(A("Home", href="/")),
                Li(A("Movies", href="/movies")),
                Li(A("Showtimes", href="/showtimes")),
                Li(A("Profile", href="/profile")),
                Li(A("Contact", href="/contact")),
                cls="sidebar-menu"
            ),
            cls="sidebar"
        ),

        # Overlay for clicking outside to close menu
        Div(onclick="toggleMenu()", cls="overlay"),

        # Main content 
        Div(content)
    ]

# # Homepage Route 
# @rt('/') #cat
# def get():
#     return Titled(
#         *create_page_structure(
#             Container(
#                 Form(
#                     Input(placeholder="Search movies...", name="search"),
#                     Button("Search", type="submit"),
#                     action="/search",
#                     method="get",
#                     cls="grid"
#                 ),
#                 H1("Now Showing"),
#                 Grid(
#                     *[MovieCard(movie) for movie in booking_controller.movie_list], #for every movie 
#                     cls="grid"
#                 ),
#             )
#         )
#     )

# @rt('/') #cat
# def get():
#     return Titled(
#         *create_page_structure(
#             Container(
#                 H1("Welcome to CE ISAN HOUSE"),
#                 Div(
#                     *[Div(
#                         # *[movie.name for movie in booking_controller.movie_list],
#                         A(Img(src=movie.image_url, style="width:100%;max-width:200px;height:auto;"), href=f"/showtime/{movie.id}")
#                     ) for movie in booking_controller.movie_list],
#                     style="display: flex; flex-wrap: wrap; gap: 20px; justify-content: center; max-width: 100%;"
#                 ),
#                 style="display: flex; flex-wrap: wrap; gap: 20px; justify-content: center;"
#             )
#         )
#     )

# @rt('/') #pentor
# def home():
#     return Container(
#         H1("Welcome to CE ISAN HOUSE"),
#         Div(
#             *[Div(
#                 H3(movie.name),
#                 A(Img(src=movie.image_url, style="width:100%;max-width:200px;height:auto;"), href=f"/showtime/{movie.id}")
#             ) for movie in movies],
#             style="display: flex; flex-wrap: wrap; gap: 20px; justify-content: center; max-width: 100%;"
#         ),
#         style="display: flex; flex-wrap: wrap; gap: 20px; justify-content: center;"
#     )

# @rt('/showtime/{id}')
# def showtime_page(id: int):
#     movie = next((m for m in movies if m.id == id), None)
#     if not movie:
#         return H1("Movie Not Found")
    
#     return Container(
#         H1(f"Showtimes for {movie.name}"),
#         Div(*[A(H3(f"{s.time} - {s.theater.name}"), href=f"/seats/{s.id}") for s in movie.get_showtimes()])
#     )



# Movie Details Route
# @rt('/movie/{movie_id}')
# def get(movie_id: str):
    # Find the movie by ID
    # movie = next((m for m in movies if m.movie_id == movie_id), None)
    
    # if not movie:
    #     return Titled("Movie Not Found", P("Sorry, the movie you're looking for doesn't exist."))
    
    # return Titled(
    #     movie.title,
    #     *create_page_structure(
    #         Container(
    #             H1(movie.title),
    #             Grid(
    #                 Div(
    #                     Img(src=movie.poster, alt=movie.title, style="width: 100%; max-height: 500px; object-fit: cover;"),
    #                     cls="grid-item"
    #                 ),
    #                 Div(
    #                     H2("Movie Details"),
    #                     P(f"Duration: {movie.duration} minutes"),
    #                     P(f"Genres: {', '.join(movie.genre)}"),
    #                     H3("Synopsis"),
    #                     P(movie.description),
    #                     A("Book Now", href=f"/book/{movie.movie_id}", cls="button"),
    #                     cls="grid-item"
    #                 ),
    #                 cls="grid"
    #             )
    #         )
    #     )
    # )

# Search Route
# @rt('/search')
# def get(search: str = ""):
    # if not search:
    #     return RedirectResponse('/')
    
    # # Case-insensitive search across title and genre
    # found_movies = [
    #     movie for movie in movies 
    #     if search.lower() in movie.title.lower() or 
    #        any(search.lower() in genre.lower() for genre in movie.genre)
    # ]
    
    # return Titled(
    #     "Search Results",
    #     *create_page_structure(
    #         Container(
    #             H1(f"Search Results for '{search}'"),
    #             Grid(
    #                 *[MovieCard(movie) for movie in found_movies],
    #                 cls="grid"
    #             ) if found_movies else P("No movies found.")
    #         )
    #     )
    # )

# @rt('/login')
# def get():
#     return Titled(
#         *create_page_structure(
#             Container(
#                 H1("Login"),
#                 Form(
#                     Label("Email"),
#                     Input(type="email", name="email"),
#                     Label("Password"),
#                     Input(type="password", name="password"),
#                     Button("Login", type="submit")
#                 )
#             )
#         )
#     )

# @rt('/profile')
# def get():
#     account = next(booking_controller.check_customer_id())
    
#     if not account:
#         return Titled("Account Not Found", P("Register or login to view your profile."))
    
#     return Titled(
#         *create_page_structure(
#             Container(
#                 H1("Profile"),
#                 *[]
#             )
#         )
#     )

# @rt("/earthpay")
# def get():
#     return Container(
#         H1("CE Isan house - ระบบชำระเงิน"),
#         P("กรุณาเลือกวิธีการชำระเงิน:"),
#         Form(
#             Div(
#                 Label(
#                     Input(type="radio", name="paymentMethod", value="card", 
#                           checked="checked", hx_get="/payment-form?method=card", 
#                           hx_target="#payment-details", hx_swap="innerHTML"), 
#                     "บัตรเครดิต/เดบิต"
#                 ),
#                 Label(
#                     Input(type="radio", name="paymentMethod", value="qrcode", 
#                           hx_get="/payment-form?method=qrcode", 
#                           hx_target="#payment-details", hx_swap="innerHTML"), 
#                     "QR Code"
#                 ),
#             ),
#             Div(id="payment-details"),
#             hx_get="/payment-form?method=card", hx_trigger="load", hx_target="#payment-details",
#             method="post",
#             action="/submit"
#         ),
#         Hr(),
#         P("Booking ID: BK123456", id="booking-info"),
#         P("ราคารวม: 500 บาท", id="total-price")
#     )

# @rt("/payment-form")
# def get(method: str):
#     if method == "card":
#         return Div(
#             Label("ชื่อบนบัตร:", Input(type="text", name="card_holder", placeholder="กรุณาระบุชื่อบนบัตร")),
#             Label("เลขบัตร:", Input(type="text", name="card_number", placeholder="xxxx-xxxx-xxxx-xxxx")),
#             Label("รหัส CVV:", Input(type="text", name="cvv", placeholder="xxx")),
#             Label("วันหมดอายุ:", Input(type="text", name="expiry", placeholder="MM/YYYY")),
#             Button("ชำระเงิน", type="button", hx_post="/process-card-payment", hx_target="#payment-result"),
#             Div(id="payment-result")
#         )
#     else:  # method == "qrcode"
#         # สร้าง QR Code สำหรับการชำระเงิน
#         booking_id =   # ในระบบจริงควรดึงจากการจองที่ถูกสร้างขึ้น
#         payment_amount =  # ในระบบจริงควรดึงจากการจอง
#         payment_data = f"CE_ISAN_PAYMENT:{booking_id}:{payment_amount}"
#         qr_code = QrPayment(qr_code_id=booking_id, expiry_time=time.time() + 600)
#         qr_code_img = qr_code.generate_qr_code(payment_data)
        
        
#         return Div(
#             P("สแกน QR Code เพื่อชำระเงิน:"),
#             P(f"ยอดเงิน: {payment_amount} บาท"),
#             Img(src=qr_code_img, alt="QR Code for payment", style="width:200px;height:200px;"),
#             P("QR Code จะหมดอายุใน 10 นาที"),
#             Button("ฉันได้ชำระเงินแล้ว", type="button", hx_post="/verify-qr-payment", hx_target="#payment-result"),
#             Div(id="payment-result")
#         )

# @rt("/process-card-payment")
# def post(card_holder: str = "", card_number: str = "", cvv: str = "", expiry: str = ""):
#     # จำลองการประมวลผลการชำระเงินด้วยบัตร
#     booking_id = "BK123456"  # ในระบบจริงควรดึงจากการจองที่ถูกสร้างขึ้น
    
#     # สร้าง Card object
#     card = Card(str(uuid.uuid4()), card_number, card_holder, expiry, cvv)
    
#     # ดึง booking จาก controller
#     booking = booking_controller.check_booking_id(booking_id)
    
#     # ถ้าไม่มีการจองในระบบ ให้จำลองการสร้างขึ้นมาสำหรับการทดสอบ
#     if booking == "Booking ID not found":
#         # สร้างการจองใหม่
#         booking = create_sample_booking()
    
#     # สร้าง Payment object
#     payment_id = f"PMT{uuid.uuid4().hex[:8].upper()}"
#     payment = Payment(payment_id, booking, booking.total_price, "card")
    
#     # ประมวลผลการชำระเงิน
#     if card.validate_Card():
#         # จำลองการเรียกเก็บเงิน
#         if card.charge_card(payment.amount):
#             booking.status = "Confirmed"
#             payment.status = "Success"
#             result = "success"
#         else:
#             payment.status = "Failed"
#             result = "failed"
#     else:
#         payment.status = "Invalid Card"
#         result = "invalid_card"
    
#     # แสดงผลลัพธ์
#     if result == "success":
#         return Div(
#             P("การชำระเงินสำเร็จ!", style="color:green;font-weight:bold;"),
#             P(f"ขอบคุณ {card_holder} สำหรับการชำระเงิน"),
#             P(f"หมายเลขการชำระเงิน: {payment_id}"),
#             A("กลับสู่หน้าหลัก", href="/", style="color:blue;text-decoration:underline;")
#         )
#     elif result == "invalid_card":
#         return Div(
#             P("ข้อมูลบัตรไม่ถูกต้อง!", style="color:red;font-weight:bold;"),
#             P("กรุณาตรวจสอบข้อมูลบัตรและลองใหม่อีกครั้ง"),
#             Button("ลองอีกครั้ง", type="button", hx_get="/payment-form?method=card", hx_target="#payment-details")
#         )
#     else:
#         return Div(
#             P("การชำระเงินไม่สำเร็จ!", style="color:red;font-weight:bold;"),
#             P("เกิดข้อผิดพลาดในการประมวลผลการชำระเงิน โปรดลองอีกครั้ง"),
#             Button("ลองอีกครั้ง", type="button", hx_get="/payment-form?method=card", hx_target="#payment-details")
#         )

# @rt("/verify-qr-payment")
# def post():
#     # จำลองการตรวจสอบการชำระเงินผ่าน QR Code
#     booking_id = "BK123456"  # ในระบบจริงควรดึงจากการจองที่ถูกสร้างขึ้น
    
#     # สร้าง QR Payment object
#     qr_expiry = datetime.now().timestamp() + 600  # หมดอายุใน 10 นาที
#     qr_payment = QrPayment(str(uuid.uuid4()), qr_expiry)
    
#     # ดึง booking จาก controller
#     booking = booking_controller.check_booking_id(booking_id)
    
#     # ถ้าไม่มีการจองในระบบ ให้จำลองการสร้างขึ้นมาสำหรับการทดสอบ
#     if booking == "Booking ID not found":
#         booking = create_sample_booking()
    
#     # สร้าง Payment object
#     payment_id = f"PMT{uuid.uuid4().hex[:8].upper()}"
#     payment = Payment(payment_id, booking, booking.total_price, "qrcode")
    
#     # จำลองการตรวจสอบการชำระเงิน
#     payment_verified = qr_payment.verify_payment()
    
#     if payment_verified:
#         booking.status = "Confirmed"
#         payment.status = "Success"
#         result = "success"
#     else:
#         payment.status = "Failed"
#         result = "failed"
    
#     # แสดงผลลัพธ์
#     if result == "success":
#         return Div(
#             P("การชำระเงินสำเร็จ!", style="color:green;font-weight:bold;"),
#             P("ขอบคุณสำหรับการชำระเงินผ่าน QR Code"),
#             P(f"หมายเลขการชำระเงิน: {payment_id}"),
#             A("กลับสู่หน้าหลัก", href="/", style="color:blue;text-decoration:underline;")
#         )
#     else:
#         return Div(
#             P("ยังไม่พบการชำระเงิน!", style="color:red;font-weight:bold;"),
#             P("ระบบยังไม่พบการชำระเงินของคุณ โปรดลองอีกครั้งหรือเลือกวิธีการชำระเงินอื่น"),
#             Button("ตรวจสอบอีกครั้ง", type="button", hx_post="/verify-qr-payment", hx_target="#payment-result"),
#             Button("เลือกวิธีการชำระเงินอื่น", type="button", hx_get="/", hx_target="body")
#         )

serve(host='localhost', port=5004)
