from fasthtml.common import *
from Classes.ce_house import *
from datetime import datetime
from typing import List
from fastapi.responses import RedirectResponse
from fastapi.responses import HTMLResponse


# ================================ INSTANCES =======================================================
booking_controller = BookingController()

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

def create_instance():
    global booking_controller
    booking_controller = BookingController()

    # Add movies
    movie1 = Movie("Decision to Leave", "Mystery", 2022, "138", "A detective investigating a man's death falls for the man's mysterious wife.", "Images/decision_to_leave.jpg")
    movie2 = Movie("Burning", "Drama", 2018, "148", "A mysterious thriller about a young deliveryman, his childhood friend, and a rich stranger.", "Images/burning.jpg")
    movie3 = Movie("Past Lives", "Drama", 2023, "106", "A woman is reunited with her childhood friend and first love while her American husband watches on.", "Images/past_lives.jpg")
    movie4 = Movie("After Yang", "Science Fiction", "96", 2021, "A father and daughter try to save their robot family member.", "Images/after_yang.jpg")
    movie5 = Movie("12 Angry Men", "Drama", 1957, "97", "A jury of 12 men must decide the fate of a young man accused of murder.", "Images/12_angry_men.jpg")
    movie6 = Movie("Memories of Murder", "Crime", "131", 2003, "Detectives struggle to catch a serial killer in rural South Korea in the 1980s.", "Images/memories_of_murder.jpg")
    movie7 = Movie("Dune", "Science Fiction", "155", 2021, "A noble family becomes embroiled in a war for control over the galaxy's most valuable resource.", "Images/dune.jpg")
    movie8 = Movie("Spirited Away", "Fantasy", "125", 2001, "A young girl enters a world of spirits and must work to free herself and her parents.", "Images/spirited_away.jpg")

    booking_controller.append_movie(movie1)
    booking_controller.append_movie(movie2)
    booking_controller.append_movie(movie3)
    booking_controller.append_movie(movie4)
    booking_controller.append_movie(movie5)
    booking_controller.append_movie(movie6)
    booking_controller.append_movie(movie7)
    booking_controller.append_movie(movie8)

    # Add theaters
    theater1 = Theater("Theater 1")
    theater2 = Theater("Theater 2")
    booking_controller.append_theater(theater1)
    booking_controller.append_theater(theater2)

    # Add showtimes to movies
    movie1.add_showtime(Showtime(movie1, "18:00", theater1))
    movie1.add_showtime(Showtime(movie1, "20:30", theater1))
    movie2.add_showtime(Showtime(movie2, "16:45", theater2))
    movie3.add_showtime(Showtime(movie3, "19:00", theater1))
    movie4.add_showtime(Showtime(movie4, "21:00", theater2))

    # Add customers
    customer1 = Customer("C001", "John Doe", "john@example.com", "john123456@")
    customer2 = Customer("C002", "Jane Smith", "jane@example.com", "jane123456@")
    booking_controller.append_customer(customer1)
    booking_controller.append_customer(customer2)

    # Add foods
    food1 = Food("F001", "Popcorn", "Large popcorn", 5.0, 100)
    food2 = Food("F002", "Soda", "Cold soda", 3.0, 100)
    food3 = Food("F003", "Nachos", "Cheese nachos", 4.5, 50)
    booking_controller.append_food(food1)
    booking_controller.append_food(food2)
    booking_controller.append_food(food3)
 
create_instance()                                   
# ===============================================================================================

# Function to display a movie card
def MovieCard(movie: Movie): #cat
    return Div(
        H3(movie.name),
        A(
            Img(src=movie.image_url, style="width:100%;max-width:200px;height:auto;"),
            href=f"/showtime/{movie.movie_id}"
        ),
        style="display: flex; flex-direction: column; align-items: center; flex-wrap: wrap; gap: 20px; justify-content: center; width: 200px;"
    )

# Function to create common page structure
def create_page_structure(content, request=None):
    # Check if user is logged in by getting customer_id from cookies
    customer_id = None
    customer_name = None
    is_logged_in = False
    
    if request and request.cookies:
        customer_id = request.cookies.get("customer_id")
        
        if customer_id:
            # Find the customer in our list
            for customer in booking_controller.customer_list:
                if str(customer.customer_id) == str(customer_id):
                    customer_name = customer.name
                    is_logged_in = True
                    break
    
    # Create user menu items based on login status
    user_menu_items = []
    if is_logged_in:
        user_menu_items = [
            Li(A(f"Welcome, {customer_name}", href="/profile", style="font-weight:bold;")),
            Li(
                A("Log Out", href="/logout", style="color:white;text-decoration:underline;"),
            )
        ]
    else:
        user_menu_items = [
            Li(A("Login", href="/login")),
            Li(A("Sign Up", href="/signup"))
        ]

    
    # Create sidebar menu items based on login status
    # Start with common navigation items
    sidebar_menu_items = [
        Li(A("Home", href="/")),
        Li(A("Showtimes", href="/showtimeall")),
        Li(A("Profile", href="/profile")),
        Li(A("Contact", href="/contact")),
    ]
    
    if is_logged_in:
        # Add a separator before logout
        sidebar_menu_items.append(
            Li(
                Div(
                    style="height:1px;background-color:#ddd;margin:10px 0;"
                ),
                style="list-style:none;padding:0;"
            )
        )
        
        # Add logout as last item - as a link instead of a form
        sidebar_menu_items.append(
            Li(
                A(
                    "Log Out", 
                    href="/logout",
                    style="display:block;background-color:#f44336;color:white;padding:8px 15px;border:none;border-radius:4px;cursor:pointer;font-size:14px;width:100%;text-align:center;text-decoration:none;"
                ),
                style="margin-top:10px;"
            )
        )
    
    # Add login-related items at the end
    
    else:
        sidebar_menu_items.extend([
            Li(A("Login", href="/login")),
            Li(A("Sign Up", href="/signup"))
        ])
    
    return [
        Title("CE ISAN HOUSE"),
        # Top Navigation Bar
        Nav(
            Div(
                A("CE ISAN HOUSE", href="/", cls="top-navbar-brand", style="font-size: 1.5rem;"),
                style="display:flex;align-items:center;"
            ),
            # User status and hamburger menu
            Div(
                # User status on large screens
                Ul(
                    *user_menu_items,
                    cls="top-navbar-menu",
                    style="display:flex;list-style:none;margin:0;margin-right:20px;padding:0;"
                ),
                # Hamburger Menu Button
                Button("☰", onclick="toggleMenu()", cls="hamburger-btn"),
                style="display:flex;align-items:center;"
            ),
            cls="top-navbar"
        ),

        # Sidebar Menu
        Div(
            # Add login status indicator at top of sidebar
            Div(
                H4(f"Logged in as {customer_name}", style="color:#4CAF50;margin:0 0 10px 0;"),
                style="margin-bottom:15px;padding-bottom:10px;border-bottom:1px solid #ddd;"
            ) if is_logged_in else None,
            
            H3("Menu", style="margin-bottom:20px;border-bottom:1px solid #ddd;padding-bottom:10px;"),
            Ul(
                *sidebar_menu_items,
                cls="sidebar-menu"
            ),
            cls="sidebar"
        ),

        # Overlay for clicking outside to close menu
        Div(onclick="toggleMenu()", cls="overlay"),

        # Main content 
        Div(content)
    ]

# Homepage Route 
@rt('/') 
def get(request):  # Add request parameter
    return Titled(
        *create_page_structure(
            Container(
                Form(
                    Input(placeholder="Search movies...", name="search"),
                    Button("Search", type="submit"),
                    action="/search",
                    method="get",
                    cls="grid"
                ),
                H1("Now Showing"),
                Div(
                    *[MovieCard(movie) for movie in booking_controller.movie_list],
                    style="display: flex; flex-wrap: wrap; gap: 20px; justify-content: center;"
                ),
                
            ),
            request=request  # Pass the request to create_page_structure
        )
    )


@rt('/showtime/{id}')
def showtime_page(id: int, request=None):
    movie = next((st for st in booking_controller.movie_list if st.movie_id == id), None)
    if not movie:
        return Titled(
            "Movie Not Found",
            *create_page_structure(
                Container(
                    H1("Movie Not Found", style="text-align:center;color:#f44336;"),
                    P("The movie you are looking for doesn't exist.", style="text-align:center;"),
                    A("Back to Homepage", href="/", 
                      style="display:block;text-align:center;margin-top:20px;color:#4CAF50;")
                ),
                request=request
            )
        )
    
    return Titled(
        f"{movie.name} - CE ISAN HOUSE",
        *create_page_structure(
            Container(
                # Movie details section with poster
                Div(
                    # Movie poster
                    Div(
                        Img(src=movie.image_url, alt=f"{movie.name} poster", 
                            style="width:100%;max-width:300px;height:auto;border-radius:8px;box-shadow:0 4px 8px rgba(0,0,0,0.2);"),
                        style="margin-right:30px;"
                    ),
                    
                    # Movie details
                    Div(
                        H1(movie.name, style="margin-top:0;color:#333;"),
                        P(f"Genre: {movie.genre}", style="margin:8px 0;"),
                        P(f"Year: {movie.year}", style="margin:8px 0;"),
                        P(f"Duration: {movie.duration} minutes", style="margin:8px 0;"),
                        P(movie.description, style="margin-top:15px;line-height:1.5;"),
                        style="flex:1;"
                    ),
                    
                    style="display:flex;flex-wrap:wrap;margin-bottom:40px;align-items:flex-start;"
                ),
                
                # Showtimes section
                H2("Available Showtimes", style="margin-top:30px;text-align:center;"),
                
                # Showtimes grid
                Div(
                    *[
                        Div(
                            H3(st.theater.name, style="margin-top:0;"),
                            P(f"Time: {st.time}", style="margin:5px 0;"),
                            A(
                                "Select Seats",
                                href=f"/seats/{st.id}",
                                style="display:inline-block;background-color:#4CAF50;color:white;padding:10px 15px;text-decoration:none;border-radius:4px;margin-top:10px;"
                            ),
                            style="background-color:#f8f8f8;padding:20px;border-radius:8px;margin:10px;flex:1;min-width:200px;box-shadow:0 2px 5px rgba(0,0,0,0.1);"
                        ) for st in movie.get_showtimes()
                    ],
                    style="display:flex;flex-wrap:wrap;justify-content:center;margin:30px 0;"
                ),
                
                # Back button
                Div(
                    A(
                        "← Back to Movies",
                        href="/",
                        style="display:inline-block;background-color:#333;color:white;padding:10px 15px;text-decoration:none;border-radius:4px;"
                    ),
                    style="margin-top:30px;text-align:center;"
                )
            ),
            request=request
        )
    )

@rt('/showtimeall')
def all_showtimes(request=None):
    # Collect all movies with their showtimes
    movies_with_showtimes = []
    for movie in booking_controller.movie_list:
        if movie.get_showtimes():
            movies_with_showtimes.append(movie)
    
    return Titled(
        "All Showtimes - CE ISAN HOUSE",
        *create_page_structure(
            Container(
                H1("All Showtimes", style="text-align:center;margin-bottom:30px;"),
                
                # Display each movie with its showtimes
                *[
                    Div(
                        # Movie title and poster
                        Div(
                            H2(movie.name, style="margin-top:0;"),
                            Div(
                                Img(src=movie.image_url, alt=f"{movie.name} poster", 
                                    style="width:120px;height:auto;border-radius:6px;"),
                                style="margin-bottom:15px;"
                            ),
                            style="margin-bottom:15px;"
                        ),
                        
                        # Showtimes for this movie
                        Div(
                            *[
                                Div(
                                    P(f"{st.time} - {st.theater.name}", style="margin:0;"),
                                    A(
                                        "Book Seats",
                                        href=f"/seats/{st.id}",
                                        style="color:#4CAF50;font-size:0.9rem;"
                                    ),
                                    style="margin:5px 0;padding:8px;background-color:#f8f8f8;border-radius:4px;"
                                ) for st in movie.get_showtimes()
                            ],
                            style="margin-left:20px;"
                        ),
                        
                        # View movie details link
                        Div(
                            A(
                                "View Movie Details",
                                href=f"/showtime/{movie.movie_id}",
                                style="color:#333;text-decoration:underline;"
                            ),
                            style="margin-top:10px;"
                        ),
                        
                        style="display:flex;flex-wrap:wrap;align-items:flex-start;padding:15px;margin-bottom:20px;border-bottom:1px solid #eee;"
                    ) for movie in movies_with_showtimes
                ],
                
                # Show message if no showtimes available for any movie
                Div(
                    P("No showtimes currently scheduled.", 
                      style="font-style:italic;color:#777;text-align:center;"),
                    style="padding:30px;"
                ) if not movies_with_showtimes else None,
                
                style="max-width:800px;margin:0 auto;"
            ),
            request=request
        )
    )

@rt('/seats/{id}')
def seats_page(request, id: int):
    # Find showtime with matching ID across all movies
    found_showtime = None
    for movie in booking_controller.movie_list:
        for showtime in movie.get_showtimes():
            if showtime.id == id:
                found_showtime = showtime
                break
        if found_showtime:
            break
    
    # Handle case when showtime is not found
    if not found_showtime:
        return H1("Showtime Not Found")
    
    # Get list of already booked seats for this showtime
    booked_seats = []
    if hasattr(booking_controller, 'bookings'):
        for booking in booking_controller.bookings:
            # Only include active bookings for this showtime
            if booking.showtime.id == id and booking.status != "Cancelled":
                booked_seats.extend(booking.seats)
    
    # Return seat selection form
    return Container(
        H1(f"Select Seats for {found_showtime.movie.name}", style="text-align:center;"),
        # Movie poster with proper styling
        Div(
            Img(src=found_showtime.movie.image_url, alt=f"{found_showtime.movie.name} poster", 
                style="width:200px;height:auto;border-radius:8px;box-shadow:0 4px 8px rgba(0,0,0,0.2);"),
            style="text-align:center;margin-bottom:30px;"
        ),
        # Movie info
        Div(
            P(f"Time: {found_showtime.time}", style="font-weight:bold;text-align:center;"),
            P(f"Theater: {found_showtime.theater.name}", style="font-weight:bold;text-align:center;"),
            style="margin-bottom:20px;"
        ),
        # Theater screen visual
        Div(
            P("SCREEN", style="text-align:center;color:#fff;font-weight:bold;"),
            style="background-color:#555;padding:5px;width:80%;max-width:500px;margin:0 auto 30px;border-radius:5px;"
        ),
        # Seat selection form with a cinema layout
        Form(
            # Seat legend
            Div(
                Span("□ Available", style="margin-right:15px;"),
                Span("■ Selected", style="margin-right:15px;color:#4CAF50;font-weight:bold;"),
                Span("■ Booked", style="color:#ff3333;font-weight:bold;"),
                style="margin-bottom:20px;text-align:center;"
            ),
            # Seat rows with labels
            *[
                Div(
                    # Row label
                    Span(f"Row {chr(65+row)}", style="margin-right:20px;font-weight:bold;width:70px;display:inline-block;"),
                    # Seats in this row
                    *[
                        Label(
                            # Create seat ID
                            seat_id := f"{chr(65+row)}{seat}",
                            # Create checkbox (hidden if seat is booked)
                            Input(
                                type="checkbox", 
                                id=f"seat-{seat_id}", 
                                name="seats", 
                                value=seat_id,
                                disabled="disabled" if seat_id in booked_seats else None,
                                style="display:none;"
                            ),
                            # Create visual seat element
                            Span(
                                f"{seat}",
                                cls="seat-booked" if seat_id in booked_seats else "seat-label"
                            ),
                            style="margin:0 3px;cursor:pointer;"
                        ) for seat in range(1, 11)
                    ],
                    style="margin-bottom:8px;display:flex;align-items:center;justify-content:center;"
                ) for row in range(7)
            ],
            # Submit button
            Div(
                Button(
                    "Book Selected Seats", 
                    type="submit",
                    style="background-color:#4CAF50;color:white;padding:12px 20px;border:none;border-radius:4px;cursor:pointer;font-size:16px;"
                ),
                style="margin-top:20px;text-align:center;"
            ),
            action=f"/book-seats/{found_showtime.id}",
            method="post",
            style="max-width:600px;margin:0 auto;"
        ),
        # Improved CSS for interactive seat selection
        Style("""
            .seat-label {
                display: inline-block;
                width: 28px;
                height: 28px;
                background-color: #ddd;
                border-radius: 4px;
                margin: 0 5px;
                cursor: pointer;
                text-align: center;
                line-height: 28px;
                font-size: 12px;
                transition: all 0.2s;
            }
            
            .seat-booked {
                display: inline-block;
                width: 28px;
                height: 28px;
                background-color: #ff3333;
                color: white;
                border-radius: 4px;
                margin: 0 5px;
                text-align: center;
                line-height: 28px;
                font-size: 12px;
                cursor: not-allowed;
            }
            
            input[type='checkbox']:checked + .seat-label {
                background-color: #4CAF50;
                color: white;
                font-weight: bold;
            }
            
            input[type='checkbox']:focus + .seat-label {
                box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.5);
            }
            
            .seat-label:hover {
                background-color: #bbb;
                transform: scale(1.1);
            }
        """),
        style="padding:20px;max-width:800px;margin:0 auto;"
    )

@rt('/book-seats/{showtime_id}', methods=["POST"])
def book_seats_post(showtime_id: int, seats: List[str] = Form([])):
    # Find showtime with matching ID across all movies
    found_showtime = None
    for movie in booking_controller.movie_list:
        for showtime in movie.get_showtimes():
            if showtime.id == showtime_id:
                found_showtime = showtime
                break
        if found_showtime:
            break
    
    if not found_showtime:
        return Container(
            H1("Error"),
            P("Showtime not found"),
            A("Back to Homepage", href="/")
        )
    
    if not seats or len(seats) == 0:
        return Container(
            H1("No Seats Selected"),
            P("Please select at least one seat to continue."),
            A("Back to Seat Selection", href=f"/seats/{showtime_id}", 
              style="display:inline-block;background-color:#4CAF50;color:white;padding:10px 15px;text-decoration:none;border-radius:4px;margin-top:20px;")
        )
    
    # For now, use first customer as the logged-in user
    # In a real app, you'd get the customer from the session
    customer = booking_controller.customer_list[0]
    
    # Create booking ID
    # Make sure the bookings attribute exists on the controller
    if not hasattr(booking_controller, 'bookings'):
        booking_controller.bookings = []
    
    booking_id = f"BK{len(booking_controller.bookings) + 1:03d}"
    
    # Create new booking
    new_booking = Booking(
        booking_id=booking_id,
        customer=customer,
        showtime=found_showtime,
        seats=seats,
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        status="Pending"
    )
    
    # Add booking to controller
    booking_controller.bookings.append(new_booking)
    
    # Create seat bookings
    if not hasattr(booking_controller, 'seat_bookings'):
        booking_controller.seat_bookings = []
    
    # Create a SeatBooked object for each seat
    for seat in seats:
        seat_booked = SeatBooked(
            seat_id=f"{booking_id}-{seat}",
            booking=new_booking,
            seat_number=seat
        )
        booking_controller.seat_bookings.append(seat_booked)
    
    # Calculate price (simple example)
    price_per_seat = 10.0  # Basic price
    total_price = len(seats) * price_per_seat
    
    # Redirect to a confirmation page with payment options
    return Container(
        H1("Booking Confirmation", style="text-align:center;color:#333;margin-bottom:30px;"),
        
        # Movie and showtime details
        Div(
            H2(f"{found_showtime.movie.name}", style="margin-bottom:15px;color:#333;"),
            
            # Movie poster
            Div(
                Img(src=found_showtime.movie.image_url, 
                    alt=f"{found_showtime.movie.name} poster",
                    style="width:200px;height:auto;border-radius:8px;box-shadow:0 4px 8px rgba(0,0,0,0.2);"),
                style="text-align:center;margin-bottom:20px;"
            ),
            
            # Booking details
            Div(
                P(f"Date: {datetime.now().strftime('%Y-%m-%d')}", style="margin:8px 0;"),
                P(f"Time: {found_showtime.time}", style="margin:8px 0;"),
                P(f"Theater: {found_showtime.theater.name}", style="margin:8px 0;"),
                P(f"Seats: {', '.join(seats)}", style="margin:8px 0;"),
                P(f"Total Price: ${total_price:.2f}", style="margin:8px 0;font-weight:bold;color:#4CAF50;font-size:18px;"),
                style="background-color:#f8f8f8;padding:20px;border-radius:8px;margin-bottom:30px;"
            ),
            
            style="margin-bottom:30px;"
        ),
        
        # Payment options
        H3("Choose Payment Method", style="text-align:center;margin-bottom:20px;"),
        Form(
            # Credit card option
            Div(
                Input(type="radio", id="card", name="payment_method", value="card", checked="checked"),
                Label("Credit/Debit Card", for_="card", style="margin-left:10px;"),
                style="margin:15px 0;padding:15px;background-color:#f9f9f9;border-radius:5px;border:1px solid #ddd;"
            ),
            
            # QR code option
            Div(
                Input(type="radio", id="qrcode", name="payment_method", value="qrcode"),
                Label("QR Code Payment", for_="qrcode", style="margin-left:10px;"),
                style="margin:15px 0;padding:15px;background-color:#f9f9f9;border-radius:5px;border:1px solid #ddd;"
            ),
            
            # Hidden fields to pass booking info
            Input(type="hidden", name="booking_id", value=booking_id),
            Input(type="hidden", name="amount", value=str(total_price)),
            
            # Submit button
            Div(
                Button(
                    "Continue to Payment", 
                    type="submit",
                    style="background-color:#4CAF50;color:white;padding:12px 30px;border:none;border-radius:4px;cursor:pointer;font-size:16px;width:100%;"
                ),
                style="margin-top:30px;"
            ),
            
            action="/process-payment",
            method="post",
            style="max-width:500px;margin:0 auto;"
        ),
        
        style="padding:30px;max-width:800px;margin:0 auto;background-color:white;border-radius:8px;box-shadow:0 2px 10px rgba(0,0,0,0.1);"
    )

@rt('/process-payment', methods=["POST"])
def process_payment(booking_id: str = Form(...), payment_method: str = Form(...), amount: str = Form(...)):
    # Find booking with this ID
    booking = None
    if hasattr(booking_controller, 'bookings'):
        for b in booking_controller.bookings:
            if b.booking_id == booking_id:
                booking = b
                break
    
    if not booking:
        return Titled(
            "Error",
            *create_page_structure(
                Container(
                    H1("Error", style="color:red;text-align:center;"),
                    P("Booking not found!", style="text-align:center;"),
                    A("Back to Homepage", href="/", 
                      style="display:block;text-align:center;margin-top:20px;color:#4CAF50;")
                ),
                request=None
            )
        )
    
    # Update booking status
    booking.status = "Confirmed"
    
    # Create a payment receipt page
    return Titled(
        "Payment Successful",
        *create_page_structure(
            Container(
                H1("Payment Successful!", style="text-align:center;color:#4CAF50;margin-bottom:30px;"),
                
                # Payment receipt
                Div(
                    H2("Receipt", style="text-align:center;margin-bottom:20px;"),
                    
                    P(f"Booking ID: {booking_id}", style="margin:8px 0;"),
                    P(f"Movie: {booking.showtime.movie.name}", style="margin:8px 0;"),
                    P(f"Date: {datetime.now().strftime('%Y-%m-%d')}", style="margin:8px 0;"),
                    P(f"Time: {booking.showtime.time}", style="margin:8px 0;"),
                    P(f"Theater: {booking.showtime.theater.name}", style="margin:8px 0;"),
                    P(f"Seats: {', '.join(booking.seats)}", style="margin:8px 0;"),
                    P(f"Amount Paid: ${amount}", style="margin:8px 0;font-weight:bold;"),
                    P(f"Payment Method: {payment_method.capitalize()}", style="margin:8px 0;"),
                    P(f"Transaction ID: TXN{booking_id}", style="margin:8px 0;"),
                    
                    style="background-color:#f9f9f9;padding:20px;border-radius:8px;margin-bottom:30px;border:1px solid #ddd;"
                ),
                
                # Success message and links
                Div(
                    P("Your booking is confirmed! A confirmation email has been sent to your registered email address.", 
                      style="text-align:center;margin-bottom:30px;"),
                    
                    Div(
                        A("View My Bookings", href="/profile", 
                          style="display:inline-block;background-color:#4CAF50;color:white;padding:10px 20px;text-decoration:none;border-radius:4px;margin-right:15px;"),
                        A("Back to Homepage", href="/", 
                          style="display:inline-block;background-color:#333;color:white;padding:10px 20px;text-decoration:none;border-radius:4px;"),
                        style="text-align:center;"
                    ),
                ),
                
                style="max-width:600px;margin:0 auto;padding:30px;background-color:white;border-radius:8px;box-shadow:0 2px 10px rgba(0,0,0,0.1);"
            ),
            request=None
        )
    )


# Search Route
@rt('/search')
def get(request, search: str = ""):  # Add request parameter
    if not search:
        return RedirectResponse('/')
    
    # Case-insensitive search across movie names and genres
    found_movies = []
    for movie in booking_controller.movie_list:
        # Access name using property (not as a method call)
        if search.lower() in movie.name.lower():
            found_movies.append(movie)
        # Access genre properly based on your class definition
        elif hasattr(movie, 'genre') and search.lower() in movie.genre.lower():
            found_movies.append(movie)
    
    return Titled(
        "Search Results",
        *create_page_structure(
            Container(
                H1(f"Search Results for '{search}'"),
                Div(
                    *[MovieCard(movie) for movie in found_movies],
                    style="display: flex; flex-wrap: wrap; gap: 20px;"
                ) if found_movies else P("No movies found matching your search.")
            ),
            request=request  # Pass the request to create_page_structure
        )
    )

@rt('/contact')
def contact_page(request=None):
    return Titled(
        "Contact Us - CE ISAN HOUSE",
        *create_page_structure(
            Container(
                H1("Contact Us", style="text-align:center;margin-bottom:30px;"),
                
                Div(
                    # Contact information
                    Div(
                        H2("Cinema Information", style="margin-bottom:20px;"),
                        P("CE ISAN HOUSE Cinema", style="margin:5px 0;font-weight:bold;"),
                        P("123 Movie Street", style="margin:5px 0;"),
                        P("Khon Kaen, Thailand 40000", style="margin:5px 0;"),
                        P("Phone: (66) 123-456-7890", style="margin:5px 0;"),
                        P("Email: info@ceisanhouse.com", style="margin:5px 0;"),
                        style="flex:1;min-width:300px;margin-right:30px;"
                    ),
                    
                    # Contact form
                    Div(
                        H2("Send Us a Message", style="margin-bottom:20px;"),
                        Form(
                            Div(
                                Label("Name", for_="name", style="display:block;margin-bottom:5px;"),
                                Input(type="text", id="name", name="name", placeholder="Your name", 
                                      required="required", style="width:100%;padding:8px;margin-bottom:15px;border:1px solid #ddd;border-radius:4px;"),
                            ),
                            Div(
                                Label("Email", for_="email", style="display:block;margin-bottom:5px;"),
                                Input(type="email", id="email", name="email", placeholder="Your email", 
                                      required="required", style="width:100%;padding:8px;margin-bottom:15px;border:1px solid #ddd;border-radius:4px;"),
                            ),
                            Div(
                                Label("Subject", for_="subject", style="display:block;margin-bottom:5px;"),
                                Input(type="text", id="subject", name="subject", placeholder="Subject", 
                                      required="required", style="width:100%;padding:8px;margin-bottom:15px;border:1px solid #ddd;border-radius:4px;"),
                            ),
                            Div(
                                Label("Message", for_="message", style="display:block;margin-bottom:5px;"),
                                # Replace TextArea with Input of type="textarea" or a custom HTML string
                                Input(type="textarea", id="message", name="message", placeholder="Your message", 
                                      required="required", style="width:100%;padding:8px;margin-bottom:15px;border:1px solid #ddd;border-radius:4px;height:150px;"),
                            ),
                            Button(
                                "Send Message", 
                                type="submit",
                                style="background-color:#4CAF50;color:white;padding:10px 20px;border:none;border-radius:4px;cursor:pointer;font-size:16px;"
                            ),
                            method="post",
                            action="/contact-submit"
                        ),
                        style="flex:1;min-width:300px;"
                    ),
                    
                    style="display:flex;flex-wrap:wrap;margin-bottom:40px;"
                ),
                
                # Map (a placeholder image)
                H2("Find Us", style="text-align:center;margin:30px 0 20px;"),
                Div(
                    Div(
                        "Map Placeholder - In a real application, embed Google Maps here",
                        style="background-color:#f0f0f0;height:300px;display:flex;align-items:center;justify-content:center;border-radius:8px;"
                    ),
                    style="width:100%;max-width:800px;margin:0 auto;"
                ),
                
                style="max-width:800px;margin:0 auto;padding:0 20px;"
            ),
            request=request
        )
    )

@rt('/contact-submit', methods=["POST"])
def contact_submit(name: str = Form(...), email: str = Form(...), subject: str = Form(...), message: str = Form(...)):
    # In a real application, you would save this to a database or send an email
    # For now, just return a thank you page
    return Titled(
        "Message Sent - CE ISAN HOUSE",
        *create_page_structure(
            Container(
                H1("Thank You!", style="text-align:center;color:#4CAF50;margin-bottom:30px;"),
                P("Your message has been sent. We'll get back to you shortly.", 
                  style="text-align:center;font-size:18px;margin-bottom:30px;"),
                Div(
                    A("Back to Homepage", href="/", 
                      style="display:inline-block;background-color:#4CAF50;color:white;padding:10px 20px;text-decoration:none;border-radius:4px;"),
                    style="text-align:center;"
                ),
                style="max-width:600px;margin:0 auto;padding:30px;"
            ),
            request=None
        )
    )


@rt('/profile')
def profile_page(request):  # Keep the request parameter
    # Get customer ID from cookies
    customer_id = request.cookies.get("customer_id")
    
    if not customer_id:
        # Not logged in - redirect to login page
        return RedirectResponse(url="/login")
    
    # Find customer with this ID
    found_customer = None
    for customer in booking_controller.customer_list:
        if str(customer.customer_id) == str(customer_id):
            found_customer = customer
            break
    
    if not found_customer:
        # Customer not found (invalid cookie) - redirect to login
        response = RedirectResponse(url="/login")
        response.delete_cookie(key="customer_id")
        return response
    
    # Access properties directly since they're defined in your class
    customer_name = found_customer.name
    customer_email = found_customer.email
    
    # Get customer bookings
    customer_bookings = []
    if hasattr(booking_controller, 'bookings'):
        for booking in booking_controller.bookings:
            if booking.customer.customer_id == customer_id:
                customer_bookings.append(booking)
    
    # Display profile page
    return Titled(
        f"Profile - {customer_name}",
        *create_page_structure(
            Container(
                H1(f"Welcome, {customer_name}!", style="text-align:center;margin-bottom:30px;"),
                
                # User info section
                Div(
                    H2("Your Information", style="margin-bottom:20px;"),
                    Div(
                        P(f"Customer ID: {customer_id}", style="margin:8px 0;"),
                        P(f"Email: {customer_email}", style="margin:8px 0;"),
                        style="background-color:#f8f8f8;padding:15px;border-radius:8px;margin-bottom:30px;"
                    ),
                    
                    # Booking history section with simplified access
                    H2("Your Bookings", style="margin-bottom:20px;"),
                    *[
                        Div(
                            H3(f"Booking #{booking.booking_id}", style="margin-bottom:10px;"),
                            P(f"Movie: {booking.showtime.movie.name}", style="margin:5px 0;"),
                            P(f"Date: {booking.timestamp}", style="margin:5px 0;"),
                            P(f"Time: {booking.showtime.time}", style="margin:5px 0;"),
                            P(f"Theater: {booking.showtime.theater.name}", style="margin:5px 0;"),
                            P(f"Seats: {', '.join(booking.seats)}", style="margin:5px 0;"),
                            P(f"Status: {booking.status}", style="margin:5px 0;font-weight:bold;"),
                            style="background-color:#f8f8f8;padding:15px;border-radius:8px;margin-bottom:15px;"
                        ) for booking in customer_bookings
                    ] if customer_bookings else [
                        P("You don't have any bookings yet.", style="font-style:italic;color:#777;")
                    ],
                    
                    style="max-width:800px;margin:0 auto;"
                )
            ),
            request=request  # Pass the request to create_page_structure
        )
    )



@rt('/login')
def get():
    return Titled(
        "Login - CE ISAN HOUSE",
        *create_page_structure(
            Container(
                H1("Login", style="text-align:center;margin-bottom:30px;"),
                Form(
                    Div(
                        Label("Email", for_="email", style="display:block;margin-bottom:5px;font-weight:bold;"),
                        Input(type="email", id="email", name="email", placeholder="Enter your email", 
                              required="required", style="width:100%;padding:10px;margin-bottom:20px;border:1px solid #ddd;border-radius:4px;"),
                    ),
                    Div(
                        Label("Password", for_="password", style="display:block;margin-bottom:5px;font-weight:bold;"),
                        Input(type="password", id="password", name="password", placeholder="Enter your password",
                              required="required", style="width:100%;padding:10px;margin-bottom:20px;border:1px solid #ddd;border-radius:4px;"),
                    ),
                    Div(
                        Button("Login", type="submit", style="background-color:#4CAF50;color:white;padding:10px 20px;border:none;border-radius:4px;cursor:pointer;font-size:16px;width:100%;"),
                        style="margin-top:20px;"
                    ),
                    Div(
                        P("Don't have an account?", style="display:inline;margin-right:5px;"),
                        A("Sign up", href="/signup", style="color:#4CAF50;text-decoration:none;"),
                        style="margin-top:20px;text-align:center;"
                    ),
                    method="post",
                    action="/login",
                    style="max-width:400px;margin:0 auto;padding:20px;background-color:#f9f9f9;border-radius:8px;box-shadow:0 2px 10px rgba(0,0,0,0.1);"
                )
            )
        )
    )

@rt('/login', methods=["POST"])
def login_post(email: str = Form(...), password: str = Form(...)):
    # For debugging purposes - print the credentials
    print(f"Login attempt with email: {email}, password: {password}")
    
    # Find customer with matching email
    found_customer = None
    for customer in booking_controller.customer_list:
        # Debug
        print(f"Checking customer: {customer}")
        
        customer_email = None
        # Try different approaches to get the email
        if hasattr(customer, 'get_email') and callable(getattr(customer, 'get_email')):
            customer_email = customer.get_email()
        elif hasattr(customer, 'email') and isinstance(getattr(type(customer), 'email', None), property):
            customer_email = customer.email
        elif hasattr(customer, '_Customer__email'):  # Access private attribute directly
            customer_email = customer._Customer__email
        
        print(f"Customer email: {customer_email}")
        
        if customer_email == email:
            found_customer = customer
            break
    
    if not found_customer:
        return Titled(
            "Login Failed",
            *create_page_structure(
                Container(
                    H1("Login Failed", style="text-align:center;color:#f44336;"),
                    P("Email address not found. Please check your email or sign up for an account.", 
                      style="text-align:center;margin-bottom:20px;"),
                    Div(
                        A("Try Again", href="/login", 
                          style="background-color:#4CAF50;color:white;padding:10px 20px;border-radius:4px;text-decoration:none;margin-right:20px;"),
                        A("Sign Up", href="/signup",
                          style="background-color:#2196F3;color:white;padding:10px 20px;border-radius:4px;text-decoration:none;"),
                        style="text-align:center;"
                    )
                )
            )
        )
    
    # Debug
    print(f"Found customer: {found_customer}")
    
    # Check password - Try different ways to access the password
    customer_password = None
    
    # Try different approaches to get the password
    if hasattr(found_customer, 'get_password') and callable(getattr(found_customer, 'get_password')):
        customer_password = found_customer.get_password()
    elif hasattr(found_customer, 'password') and isinstance(getattr(type(found_customer), 'password', None), property):
        customer_password = found_customer.password
    elif hasattr(found_customer, '_Customer__password'):  # Access private attribute directly
        customer_password = found_customer._Customer__password
        
    # Debug
    print(f"Customer stored password: {customer_password}")
    print(f"Entered password: {password}")
    print(f"Match: {customer_password == password}")
    
    # Compare the passwords
    if customer_password != password:
        return Titled(
            "Login Failed",
            *create_page_structure(
                Container(
                    H1("Login Failed", style="text-align:center;color:#f44336;"),
                    P("Incorrect password. Please try again.", 
                      style="text-align:center;margin-bottom:20px;"),
                    A("Back to Login", href="/login", 
                      style="display:inline-block;background-color:#4CAF50;color:white;padding:10px 20px;border-radius:4px;text-decoration:none;text-align:center;")
                )
            )
        )
    
    # Login successful - redirect to profile page or homepage
    response = RedirectResponse(url="/profile")
    
    # Get customer ID
    customer_id = None
    if hasattr(found_customer, 'get_customer_id') and callable(getattr(found_customer, 'get_customer_id')):
        customer_id = found_customer.get_customer_id()
    elif hasattr(found_customer, 'customer_id') and isinstance(getattr(type(found_customer), 'customer_id', None), property):
        customer_id = found_customer.customer_id
    elif hasattr(found_customer, '_Customer__customer_id'):  # Access private attribute directly
        customer_id = found_customer._Customer__customer_id
    else:
        # Last resort
        customer_id = found_customer.customer_id
    
    print(f"Setting customer_id cookie: {customer_id}")
    
    response.set_cookie(key="customer_id", value=customer_id)
    return response

@rt('/logout')
def logout_get():
    response = RedirectResponse(url="/")
    response.delete_cookie(key="customer_id")
    return response

@rt('/logout', methods=["POST"])
def logout_post():  # Renamed to be more specific
    response = RedirectResponse(url="/")
    response.delete_cookie(key="customer_id")
    # Set status code to 303 See Other to ensure redirect works with POST
    response.status_code = 303
    return response


@rt('/signup')
def signup_get(request=None):
    # Get error from query params if present
    error = request.query_params.get('error') if request else None
    
    error_message = None
    if error:
        if error == "missing_fields":
            error_message = "All fields are required"
        elif error == "passwords_dont_match":
            error_message = "Passwords don't match"
        elif error == "password_too_short":
            error_message = "Password must be at least 8 characters"
        elif error == "email_exists":
            error_message = "Email already exists"
        else:
            error_message = f"Error: {error}"
    
    return Titled(
        "Sign Up - CE ISAN HOUSE",
        *create_page_structure(
            Container(
                H1("Create an Account", style="text-align:center;margin-bottom:30px;"),
                
                # Show error message if there is one
                Div(
                    P(error_message, style="color:white;text-align:center;"),
                    style="background-color:#d32f2f;padding:10px;border-radius:4px;margin-bottom:20px;"
                ) if error_message else None,
                
                Form(
                    Div(
                        Label("Full Name", for_="name", style="display:block;margin-bottom:5px;font-weight:bold;"),
                        Input(type="text", id="name", name="name", placeholder="Enter your full name", 
                              required="required", style="width:100%;padding:10px;margin-bottom:20px;border:1px solid #ddd;border-radius:4px;")
                    ),
                    Div(
                        Label("Email", for_="email", style="display:block;margin-bottom:5px;font-weight:bold;"),
                        Input(type="email", id="email", name="email", placeholder="Enter your email", 
                              required="required", style="width:100%;padding:10px;margin-bottom:20px;border:1px solid #ddd;border-radius:4px;")
                    ),
                    Div(
                        Label("Password", for_="password", style="display:block;margin-bottom:5px;font-weight:bold;"),
                        Input(type="password", id="password", name="password", placeholder="Create a password", 
                              required="required", style="width:100%;padding:10px;margin-bottom:20px;border:1px solid #ddd;border-radius:4px;")
                    ),
                    Div(
                        Label("Confirm Password", for_="confirm_password", style="display:block;margin-bottom:5px;font-weight:bold;"),
                        Input(type="password", id="confirm_password", name="confirm_password", placeholder="Confirm your password", 
                              required="required", style="width:100%;padding:10px;margin-bottom:20px;border:1px solid #ddd;border-radius:4px;")
                    ),
                    Div(
                        Button(
                            "Create Account", 
                            type="submit",
                            style="background-color:#4CAF50;color:white;padding:10px 20px;border:none;border-radius:4px;cursor:pointer;font-size:16px;width:100%;"
                        ),
                        style="margin-top:20px;"
                    ),
                    Div(
                        P("Already have an account?", style="display:inline;margin-right:5px;"),
                        A("Log in", href="/login", style="color:#4CAF50;text-decoration:none;"),
                        style="margin-top:20px;text-align:center;"
                    ),
                    method="post",
                    action="/signup",
                    style="max-width:400px;margin:0 auto;padding:20px;background-color:#f9f9f9;border-radius:8px;box-shadow:0 2px 10px rgba(0,0,0,0.1);"
                )
            ),
            request=request
        )
    )

@rt('/signup', methods=["POST"])
def signup_post(name: str = Form(...), email: str = Form(...), password: str = Form(...), confirm_password: str = Form(...)):
    print(f"\n[DEBUG] Starting signup process...")
    print(f"[DEBUG] Received: name={name}, email={email}")
    
    try:
        # Create a Guest instance to handle registration
        guest = Guest()
        
        # Basic validation
        if not all([name, email, password, confirm_password]):
            print("[DEBUG] Missing required fields")
            return RedirectResponse(url="/signup?error=missing_fields", status_code=303)
        
        if password != confirm_password:
            print("[DEBUG] Passwords don't match")
            return RedirectResponse(url="/signup?error=passwords_dont_match", status_code=303)
        
        # Check if email exists using BookingController's method
        existing_customer = booking_controller.find_customer_by_email(email)
        if existing_customer:
            print(f"[DEBUG] Email already exists: {email}")
            return RedirectResponse(url="/signup?error=email_exists", status_code=303)
        
        # Use Guest's register method to create new customer
        new_customer = guest.register(booking_controller, name, email, password)
        
        if new_customer:
            print(f"[DEBUG] Customer created successfully: {new_customer.name}")
            # Redirect to login page
            return RedirectResponse(url="/login?message=account_created", status_code=303)
        else:
            print("[DEBUG] Failed to create customer")
            return RedirectResponse(url="/signup?error=registration_failed", status_code=303)
            
    except Exception as e:
        print(f"[DEBUG] Error during signup: {str(e)}")
        import traceback
        traceback.print_exc()
        return RedirectResponse(url="/signup?error=unknown_error", status_code=303)

    
# Add this route to test customer creation directly
@rt('/test-customer-create')
def test_customer():
    try:
        # Test Customer class directly
        test_id = "TEST123"
        test_name = "Test User"
        test_email = "test@example.com"
        test_password = "password123"
        
        print(f"Testing Customer creation with {test_id}, {test_name}, {test_email}")
        test_customer = Customer(test_id, test_name, test_email, test_password)
        print(f"Customer created: {test_customer}")
        
        # Test properties
        print(f"ID: {test_customer.customer_id}")
        print(f"Name: {test_customer.name}")
        print(f"Email: {test_customer.email}")
        
        # Test adding to controller
        booking_controller.append_customer(test_customer)
        print(f"Added to booking_controller, total customers: {len(booking_controller.customer_list)}")
        
        return Container(
            H1("Customer Creation Test"),
            P(f"Successfully created customer {test_name}"),
            P(f"Current customers in system: {len(booking_controller.customer_list)}")
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        return Container(
            H1("Customer Creation Test Failed"),
            P(f"Error: {str(e)}")
        )

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

serve()
