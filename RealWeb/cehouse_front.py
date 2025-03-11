from fasthtml.common import *
from Classes.ce_house import *
from datetime import datetime
from typing import List
from fastapi.responses import RedirectResponse
# from fastapi.responses import HTMLResponse
import qrcode

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
    movie1 = Movie("Decision to Leave", "Mystery", 2022, "138", "A detective investigating a man's death falls for the man's mysterious wife.", "Images/decision_to_leave.jpg", "https://www.youtube.com/watch?v=A33AdB4u8GQ")
    movie2 = Movie("Burning", "Drama", 2018, "148", "A mysterious thriller about a young deliveryman, his childhood friend, and a rich stranger.", "Images/burning.jpg", "https://www.youtube.com/watch?v=oihHs2Errwk")
    movie3 = Movie("Past Lives", "Drama", 2023, "106", "A woman is reunited with her childhood friend and first love while her American husband watches on.", "Images/past_lives.jpg", "https://www.youtube.com/watch?v=kA244xewjcI")
    movie4 = Movie("After Yang", "Science Fiction", "96", 2021, "A father and daughter try to save their robot family member.", "Images/after_yang.jpg", "https://www.youtube.com/watch?v=Kwp32zLc08c")
    movie5 = Movie("12 Angry Men", "Drama", 1957, "97", "A jury of 12 men must decide the fate of a young man accused of murder.", "Images/12_angry_men.jpg", "https://www.youtube.com/watch?v=TEN-2uTi2c0&t=2s")
    movie6 = Movie("Memories of Murder", "Crime", "131", 2003, "Detectives struggle to catch a serial killer in rural South Korea in the 1980s.", "Images/memories_of_murder.jpg", "https://www.youtube.com/watch?v=0n_HQwQU8ls")
    movie7 = Movie("Dune", "Science Fiction", "155", 2021, "A noble family becomes embroiled in a war for control over the galaxy's most valuable resource.", "Images/dune.jpg", "https://www.youtube.com/watch?v=n9xhJrPXop4")
    movie8 = Movie("Spirited Away", "Fantasy", "125", 2001, "A young girl enters a world of spirits and must work to free herself and her parents.", "Images/spirited_away.jpg", "https://www.youtube.com/watch?v=ByXuk9QqQkk")

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
        Li(A("Home", href="/", style="display:block;padding:10px;color:#333;text-decoration:none;border-radius:4px;transition:background-color 0.3s;")),
        Li(A("Showtimes", href="/showtimeall", style="display:block;padding:10px;color:#333;text-decoration:none;border-radius:4px;transition:background-color 0.3s;")),
    ]
    
    if is_logged_in:
        # Add profile and history for logged in users
        sidebar_menu_items.extend([
            Li(A("Profile", href="/profile", style="display:block;padding:10px;color:#333;text-decoration:none;border-radius:4px;transition:background-color 0.3s;")),
            Li(A("Booking History", href="/history", style="display:block;padding:10px;color:#333;text-decoration:none;border-radius:4px;transition:background-color 0.3s;")),
        ])
        
        # Add separator
        sidebar_menu_items.append(
            Li(
                Div(
                    style="height:1px;background-color:#ddd;margin:10px 0;"
                ),
                style="list-style:none;padding:0;"
            )
        )
        
        # Add logout button
        sidebar_menu_items.append(
            Li(
                A(
                    "Log Out", 
                    href="/logout",
                    style="display:block;background-color:#f44336;color:white;padding:10px;text-align:center;text-decoration:none;border-radius:4px;margin-top:10px;transition:background-color 0.3s;"
                )
            )
        )
    else:
        # Add contact for non-logged in users
        sidebar_menu_items.append(
            Li(A("Contact", href="/contact", style="display:block;padding:10px;color:#333;text-decoration:none;border-radius:4px;transition:background-color 0.3s;"))
        )
        
        # Add login/signup options
        sidebar_menu_items.extend([
            Li(A("Login", href="/login", style="display:block;padding:10px;color:#333;text-decoration:none;border-radius:4px;transition:background-color 0.3s;")),
            Li(A("Sign Up", href="/signup", style="display:block;padding:10px;color:#333;text-decoration:none;border-radius:4px;transition:background-color 0.3s;"))
        ])
    
    return [
        Title("CE ISAN HOUSE"),
        # Top Navigation Bar
        Nav(
            Div(
                A("CE ISAN HOUSE", href="/", cls="top-navbar-brand", style="font-size:1.5rem;"),
                style="display:flex;align-items:center;"
            ),
            # User status and hamburger menu
            Div(
                Ul(
                    *user_menu_items,
                    cls="top-navbar-menu",
                    style="display:flex;list-style:none;margin:0;margin-right:20px;padding:0;"
                ),
                Button("☰", onclick="toggleMenu()", cls="hamburger-btn"),
                style="display:flex;align-items:center;"
            ),
            cls="top-navbar"
        ),

        # Sidebar Menu
        Div(
            # Login status indicator
            Div(
                H4(f"Logged in as {customer_name}", style="color:#4CAF50;margin:0 0 10px 0;"),
                style="margin-bottom:15px;padding-bottom:10px;border-bottom:1px solid #ddd;"
            ) if is_logged_in else None,
            
            H3("Menu", style="margin-bottom:20px;color:#333;"),
            Ul(
                *sidebar_menu_items,
                cls="sidebar-menu",
                style="list-style:none;padding:0;margin:0;"
            ),
            cls="sidebar",
            style="padding:20px;background-color:white;"
        ),

        # Overlay
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

                        A(
                            Div(
                                Span("▶", style="font-size:1.2em;margin-right:5px;"),
                                "Watch Trailer",
                                style="display:flex;align-items:center;justify-content:center;"
                            ),
                            href=movie.trailer_url,
                            target="_blank",  # Opens in new tab
                            style="display:inline-block;background-color:#FF0000;color:white;padding:10px 20px;text-decoration:none;border-radius:4px;margin-top:20px;"
                        ),

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
    # Get error parameter from URL if present
    error = request.query_params.get("error") if hasattr(request, "query_params") else None
    
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
        return Titled(
            "Showtime Not Found",
            *create_page_structure(
                Container(
                    H1("Showtime Not Found", style="text-align:center;color:#f44336;"),
                    P("The showtime you are looking for doesn't exist.", style="text-align:center;"),
                    A("Back to Homepage", href="/", 
                      style="display:block;text-align:center;margin-top:20px;color:#4CAF50;")
                ),
                request=request
            )
        )
    
    # Get list of already booked seats for this showtime
    booked_seats = []
    if hasattr(booking_controller, 'bookings'):
        for booking in booking_controller.bookings:
            if booking.showtime.id == id and booking.status != "Cancelled":
                booked_seats.extend(booking.seats)
    
    return Titled(
        f"Select Seats - {found_showtime.movie.name}",
        *create_page_structure(
            Container(
                H1(f"Select Seats for {found_showtime.movie.name}", style="text-align:center;"),
                
                # Error message for no seats selected
                Div(
                    P("Please select at least one seat to continue.", 
                      style="color:white;text-align:center;"),
                    style="background-color:#f44336;padding:10px;border-radius:4px;margin-bottom:20px;"
                ) if error == "no_seats" else None,
                
                # Movie poster
                Div(
                    Img(src=found_showtime.movie.image_url, alt=f"{found_showtime.movie.name} poster", 
                        style="width:200px;height:auto;border-radius:8px;box-shadow:0 4px 8px rgba(0,0,0,0.2);"),
                    style="text-align:center;margin-bottom:30px;"
                ),
                
                # Showtime info
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
                
                # Seat selection form
                Form(
                    # Seat legend
                    Div(
                        Span("□ Available", style="margin-right:15px;"),
                        Span("■ Selected", style="margin-right:15px;color:#4CAF50;font-weight:bold;"),
                        Span("■ Booked", style="color:#ff3333;font-weight:bold;"),
                        style="margin-bottom:20px;text-align:center;"
                    ),
                    
                    # Seat grid
                    *[
                        Div(
                            Span(f"Row {chr(65+row)}", style="margin-right:20px;font-weight:bold;width:70px;display:inline-block;"),
                            *[
                                Label(
                                    seat_id := f"{chr(65+row)}{seat}",
                                    Input(
                                        type="checkbox", 
                                        id=f"seat-{seat_id}", 
                                        name="seats", 
                                        value=seat_id,
                                        disabled="disabled" if seat_id in booked_seats else None,
                                        style="display:none;"
                                    ),
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
                    onsubmit="return validateSeats(event)",
                    style="max-width:600px;margin:0 auto;"
                ),
                
                # JavaScript validation
                Script("""
                    function validateSeats(event) {
                        const selectedSeats = document.querySelectorAll('input[name="seats"]:checked');
                        if (selectedSeats.length === 0) {
                            alert('Please select at least one seat to continue.');
                            event.preventDefault();
                            return false;
                        }
                        return true;
                    }
                """),
                
                # Seat styles
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
            ),
            request=request
        )
    )

@rt('/book-seats/{showtime_id}', methods=["POST"])
def book_seats_post(request, showtime_id: int, seats: List[str] = Form([])):
    # First check for empty seats with stronger validation
    if not seats or len(seats) == 0:
        return RedirectResponse(
            url=f"/seats/{showtime_id}?error=no_seats",
            status_code=303
        )
    
    # Check if user is logged in
    customer_id = request.cookies.get("customer_id")
    if not customer_id:
        # User is not logged in - store seats in the redirect URL
        seats_str = ",".join(seats)
        return RedirectResponse(url=f"/login?required=true&redirect=/complete-booking/{showtime_id}?seats={seats_str}", status_code=303)
    
    # Find the logged in customer
    found_customer = None
    for customer in booking_controller.customer_list:
        if str(customer.customer_id) == str(customer_id):
            found_customer = customer
            break
    
    if not found_customer:
        # Invalid customer ID - redirect to login
        response = RedirectResponse(url="/login?error=invalid_session", status_code=303)
        response.delete_cookie(key="customer_id")
        return response
    
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
        return Titled(
            "Error",
            *create_page_structure(
                Container(
                    H1("Error", style="color:red;text-align:center;"),
                    P("Showtime not found!", style="text-align:center;"),
                    A("Back to Homepage", href="/", 
                      style="display:block;text-align:center;margin-top:20px;color:#4CAF50;")
                ),
                request=request
            )
        )
    
    # Calculate price
    price_per_seat = 10.0  # Basic price
    total_price = len(seats) * price_per_seat
    
    # Create booking ID
    if not hasattr(booking_controller, 'bookings'):
        booking_controller.bookings = []
    
    booking_id = f"BK{len(booking_controller.bookings) + 1:03d}"
    
    # Create new booking
    new_booking = Booking(
        booking_id=booking_id,
        customer=found_customer,
        showtime=found_showtime,
        seats=seats,
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        status="Pending",
        total_price=total_price
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
    
    # Redirect to food selection
    return RedirectResponse(
        url=f"/select-food/{booking_id}",
        status_code=303
    )

@rt('/select-food/{booking_id}')
def get(request, booking_id: str):
    # Find the booking
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
                request=request
            )
        )
    
    return Titled(
        "Add Food & Beverages - CE ISAN HOUSE",
        *create_page_structure(
            Container(
                H1("Add Food & Beverages", style="text-align:center;margin-bottom:30px;"),
                
                # Booking summary
                Div(
                    H3("Booking Summary", style="margin-bottom:15px;"),
                    P(f"Movie: {booking.showtime.movie.name}", style="margin:5px 0;"),
                    P(f"Time: {booking.showtime.time}", style="margin:5px 0;"),
                    P(f"Seats: {', '.join(booking.seats)}", style="margin:5px 0;"),
                    P(f"Ticket Total: ${booking.total_price:.2f}", style="margin:5px 0;"),
                    style="background-color:#f8f8f8;padding:15px;border-radius:8px;margin-bottom:30px;"
                ),
                
                # Food selection form
                Form(
                    H3("Select Your Food & Beverages", style="margin-bottom:20px;"),
                    
                    # Food items
                    *[
                        Div(
                            Div(
                                H4(food.name, style="margin:0;"),
                                P(food.description, style="color:#666;margin:5px 0;"),
                                P(f"${food.price:.2f}", style="font-weight:bold;color:#4CAF50;margin:5px 0;"),
                                style="flex:1;"
                            ),
                            Div(
                                Input(
                                    type="number",
                                    name=f"food_{food.food_id}",
                                    value="0",
                                    min="0",
                                    max=str(food.quantity),
                                    style="width:60px;padding:5px;border:1px solid #ddd;border-radius:4px;"
                                ),
                                style="margin-left:15px;"
                            ),
                            style="display:flex;align-items:center;padding:15px;background-color:#f9f9f9;border-radius:8px;margin-bottom:10px;"
                        ) for food in booking_controller.food_list if food.is_available
                    ],
                    
                    # Hidden booking ID
                    Input(type="hidden", name="booking_id", value=booking_id),
                    
                    # Buttons
                    Div(
                        Button(
                            "Continue to Payment", 
                            type="submit",
                            style="background-color:#4CAF50;color:white;padding:12px 30px;border:none;border-radius:4px;cursor:pointer;font-size:16px;margin-right:15px;"
                        ),
                        # Fix: Changed to href with payment method parameters for "Skip Food Selection" 
                        A(
                            "Skip Food Selection",
                            href=f"/payment?booking_id={booking_id}&amount={booking.total_price}",
                            style="display:inline-block;background-color:#999;color:white;padding:12px 30px;text-decoration:none;border-radius:4px;font-size:16px;"
                        ),
                        style="margin-top:30px;text-align:center;"
                    ),
                    
                    action="/process-food-selection",
                    method="post",
                    style="max-width:600px;margin:0 auto;"
                ),
                
                style="max-width:800px;margin:0 auto;padding:30px;background-color:white;border-radius:8px;box-shadow:0 2px 10px rgba(0,0,0,0.1);"
            ),
            request=request
        )
    )

@rt('/process-food-selection', methods=["POST"])
def process_food_selection(request, booking_id: str = Form(...)):
    # Find the booking
    booking = None
    if hasattr(booking_controller, 'bookings'):
        for b in booking_controller.bookings:
            if b.booking_id == booking_id:
                booking = b
                break
    
    if not booking:
        return RedirectResponse(url="/", status_code=303)
    
    # First save the original ticket price
    ticket_price = booking.total_price
    food_total = 0
    food_orders = []
    
    try:
        # Get form data without accessing ._dict property
        form_data = dict(request.form())
        
        # Process each food item
        for key, value in form_data.items():
            if key.startswith('food_') and value.isdigit() and int(value) > 0:
                food_id = key.replace('food_', '')
                quantity = int(value)
                
                # Find food item
                food_item = None
                for food in booking_controller.food_list:
                    if str(food.food_id) == str(food_id):
                        food_item = food
                        break
                
                if food_item and food_item.is_available and quantity <= food_item.quantity:
                    subtotal = food_item.price * quantity
                    food_total += subtotal
                    
                    # Create food order with the proper structure
                    food_order = FoodOrder(food_item, quantity)
                    food_orders.append(food_order)
                    
    except Exception as e:
        print(f"Error processing food selection: {str(e)}")
    
    # Store food orders in booking
    booking.food_orders = food_orders
    
    # Calculate grand total (tickets + food)
    total_amount = ticket_price + food_total
    
    # Store the ticket price and food total separately in the booking object
    # This avoids issues with read-only properties
    booking.ticket_price = ticket_price  # Original ticket price
    booking.food_total = food_total      # Food total
    
    # Redirect to payment page with correct combined total
    return RedirectResponse(
        url=f"/payment?booking_id={booking_id}&amount={total_amount}",
        status_code=303
    )

@rt('/complete-booking/{showtime_id}')
def complete_booking(request, showtime_id: int, seats: str = ""):
    # Split the seats string back into a list and check immediately
    seat_list = seats.split(',') if seats else []
    
    # Check for empty seats
    if not seat_list:
        return Titled(
            "No Seats Selected",
            *create_page_structure(
                Container(
                    H1("No Seats Selected", style="text-align:center;color:#f44336;margin-bottom:30px;"),
                    P("Please select at least one seat to continue.", style="text-align:center;margin-bottom:30px;"),
                    A("Back to Seat Selection", href=f"/seats/{showtime_id}", 
                      style="display:inline-block;background-color:#4CAF50;color:white;padding:10px 15px;text-decoration:none;border-radius:4px;margin-top:20px;text-align:center;"),
                    style="padding:30px;max-width:600px;margin:0 auto;background-color:white;border-radius:8px;box-shadow:0 2px 10px rgba(0,0,0,0.1);"
                ),
                request=request
            )
        )
    
    # Validate seat format and existence
    valid_rows = [chr(65+i) for i in range(7)]  # A through G
    valid_numbers = range(1, 11)  # 1 through 10
    invalid_seats = []
    
    for seat in seat_list:
        if (len(seat) < 2 or 
            seat[0] not in valid_rows or 
            not seat[1:].isdigit() or 
            int(seat[1:]) not in valid_numbers):
            invalid_seats.append(seat)
    
    if invalid_seats:
        return Titled(
            "Invalid Seats Selected",
            *create_page_structure(
                Container(
                    H1("Invalid Seats Selected", style="text-align:center;color:#f44336;margin-bottom:30px;"),
                    P(f"The following seats are invalid: {', '.join(invalid_seats)}", 
                      style="text-align:center;margin-bottom:15px;"),
                    P("Please select only valid seats from the seating chart.", 
                      style="text-align:center;margin-bottom:30px;"),
                    A("Back to Seat Selection", href=f"/seats/{showtime_id}", 
                      style="display:inline-block;background-color:#4CAF50;color:white;padding:10px 15px;text-decoration:none;border-radius:4px;margin-top:20px;text-align:center;"),
                    style="padding:30px;max-width:600px;margin:0 auto;background-color:white;border-radius:8px;box-shadow:0 2px 10px rgba(0,0,0,0.1);"
                ),
                request=request
            )
        )
    
    customer_id = request.cookies.get("customer_id")

    # Find the logged in customer
    found_customer = None
    for customer in booking_controller.customer_list:
        if str(customer.customer_id) == str(customer_id):
            found_customer = customer
            break
    
    # Find showtime
    found_showtime = None
    for movie in booking_controller.movie_list:
        for showtime in movie.get_showtimes():
            if showtime.id == showtime_id:
                found_showtime = showtime
                break
        if found_showtime:
            break
    
    if not found_showtime or not found_customer:
        return RedirectResponse(url=f"/seats/{showtime_id}", status_code=303)
    
    # Calculate price (simple example) - BEFORE creating the booking
    price_per_seat = 10.0  # Basic price
    total_price = len(seat_list) * price_per_seat
    
    # Create booking ID
    if not hasattr(booking_controller, 'bookings'):
        booking_controller.bookings = []
    
    booking_id = f"BK{len(booking_controller.bookings) + 1:03d}"
    
    # Create new booking
    new_booking = Booking(
        booking_id=booking_id,
        customer=found_customer,
        showtime=found_showtime,
        seats=seat_list,
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        status="Pending",
        total_price=total_price  # Pass total_price here
    )
    
    # Add booking to controller
    booking_controller.bookings.append(new_booking)
    
    # Create seat bookings
    if not hasattr(booking_controller, 'seat_bookings'):
        booking_controller.seat_bookings = []
    
    # Create a SeatBooked object for each seat
    for seat in seat_list:
        seat_booked = SeatBooked(
            seat_id=f"{booking_id}-{seat}",
            booking=new_booking,
            seat_number=seat
        )
        booking_controller.seat_bookings.append(seat_booked)
    
    # Redirect to the same payment UI as in book_seats_post
    return Titled(
        f"Booking Confirmation - {found_showtime.movie.name}",
        *create_page_structure(
            Container(
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
                        P(f"Seats: {', '.join(seat_list)}", style="margin:8px 0;"),
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
            ),
            request=request
        )
    )

@rt('/process-payment', methods=["POST"])
def process_payment(booking_id: str = Form(...), payment_method: str = Form(...), amount: str = Form(...)):
    # Redirect to the appropriate payment method page based on selection
    if payment_method == "card":
        return RedirectResponse(url=f"/card-payment?booking_id={booking_id}&amount={amount}", status_code=303)
    else:  # QR Code
        return RedirectResponse(url=f"/qrcode-payment?booking_id={booking_id}&amount={amount}", status_code=303)

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
                            P(f"Status: {booking.status}", 
                              style=f"margin:5px 0;font-weight:bold;color:" + 
                                    {"Confirmed": "#4CAF50", "Pending": "#FF9800", 
                                     "Cancelled": "#f44336", "Refunded": "#2196F3"}.get(booking.status, "#000")),
                            
                            # Action buttons based on status
                            Div(
                                # Add "Complete Payment" button for pending bookings
                                A(
                                    "Complete Payment",
                                    href=f"/repay?booking_id={booking.booking_id}&amount={booking.total_price}",
                                    style="display:inline-block;background-color:#4CAF50;color:white;padding:8px 15px;border-radius:4px;text-decoration:none;margin-right:10px;"
                                ) if booking.status == "Pending" else None,
                                
                                # Add "Request Refund" button for confirmed bookings
                                A(
                                    "Request Refund",
                                    href=f"/refund/{booking.booking_id}",
                                    style="display:inline-block;background-color:#FF5722;color:white;padding:8px 15px;border-radius:4px;text-decoration:none;"
                                ) if booking.status == "Confirmed" else None,
                                
                                style="margin-top:15px;"
                            ),
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

@rt('/refund/{booking_id}')
def refund_page(request, booking_id: str):
    # Check if user is logged in
    customer_id = request.cookies.get("customer_id")
    if not customer_id:
        return RedirectResponse(url="/login")
    
    # Find the booking
    booking = None
    if hasattr(booking_controller, 'bookings'):
        for b in booking_controller.bookings:
            if b.booking_id == booking_id:
                booking = b
                break
    
    # Check if booking exists and belongs to this user
    if not booking or str(booking.customer.customer_id) != str(customer_id):
        return Titled(
            "Error",
            *create_page_structure(
                Container(
                    H1("Error", style="color:red;text-align:center;"),
                    P("Booking not found or unauthorized access.", style="text-align:center;"),
                    A("Back to Profile", href="/profile", 
                      style="display:block;text-align:center;margin-top:20px;color:#4CAF50;")
                ),
                request=request
            )
        )
    
    # Check if booking is refundable (confirmed status only)
    if booking.status != "Confirmed":
        return Titled(
            "Refund Not Available",
            *create_page_structure(
                Container(
                    H1("Refund Not Available", style="color:red;text-align:center;"),
                    P("This booking cannot be refunded.", style="text-align:center;margin-bottom:15px;"),
                    P(f"Reason: This booking has status '{booking.status}'", style="text-align:center;"),
                    P("Only confirmed bookings can be refunded.", style="text-align:center;margin-bottom:30px;"),
                    A("Back to Profile", href="/profile", 
                      style="display:inline-block;background-color:#4CAF50;color:white;padding:10px 15px;text-decoration:none;border-radius:4px;"),
                    style="padding:30px;max-width:600px;margin:0 auto;background-color:white;border-radius:8px;box-shadow:0 2px 10px rgba(0,0,0,0.1);"
                ),
                request=request
            )
        )
    
    # Show simplified refund confirmation page
    return Titled(
        "Confirm Refund - CE ISAN HOUSE",
        *create_page_structure(
            Container(
                H1("Confirm Refund", style="text-align:center;margin-bottom:30px;"),
                
                # Booking details
                Div(
                    H3("Booking Details", style="margin-bottom:15px;"),
                    P(f"Booking ID: {booking.booking_id}", style="margin:5px 0;"),
                    P(f"Movie: {booking.showtime.movie.name}", style="margin:5px 0;"),
                    P(f"Time: {booking.showtime.time}", style="margin:5px 0;"),
                    P(f"Theater: {booking.showtime.theater.name}", style="margin:5px 0;"),
                    P(f"Seats: {', '.join(booking.seats)}", style="margin:5px 0;"),
                    P(f"Total Price: ${booking.total_price:.2f}", style="margin:5px 0;font-weight:bold;"),
                    style="background-color:#f8f8f8;padding:15px;border-radius:8px;margin-bottom:30px;"
                ),
                
                # Warning message
                P("Are you sure you want to refund this booking? This action cannot be undone.", 
                  style="text-align:center;color:#f44336;font-weight:bold;margin-bottom:30px;"),
                
                # Simple form with just the buttons
                Form(
                    # Hidden booking ID field
                    Input(type="hidden", name="booking_id", value=booking_id),
                    
                    # Buttons side by side
                    Div(
                        Button("Confirm Refund", type="submit", 
                               style="background-color:#f44336;color:white;padding:10px 25px;border:none;border-radius:4px;cursor:pointer;margin-right:15px;font-weight:bold;"),
                        A("Cancel", href="/profile", 
                          style="display:inline-block;background-color:#999;color:white;padding:10px 25px;text-decoration:none;border-radius:4px;"),
                        style="text-align:center;"
                    ),
                    
                    action="/process-refund",
                    method="post",
                ),
                
                style="max-width:600px;margin:0 auto;padding:30px;background-color:white;border-radius:8px;box-shadow:0 2px 10px rgba(0,0,0,0.1);"
            ),
            request=request
        )
    )


@rt('/process-refund', methods=["POST"])
def process_refund(booking_id: str = Form(...)):
    # Find the booking
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
                    A("Back to Profile", href="/profile", 
                      style="display:block;text-align:center;margin-top:20px;color:#4CAF50;")
                ),
                request=None
            )
        )
    
    # Process the refund
    booking.status = "Refunded"
    
    # Show simple confirmation
    return Titled(
        "Refund Successful",
        *create_page_structure(
            Container(
                H1("Refund Successful!", style="text-align:center;color:#4CAF50;margin-bottom:30px;"),
                P("Your booking has been refunded successfully.", 
                  style="text-align:center;margin-bottom:30px;"),
                P(f"Refund Amount: ${booking.total_price:.2f}", 
                  style="text-align:center;font-weight:bold;margin-bottom:30px;"),
                A("Return to Profile", href="/profile", 
                  style="display:inline-block;background-color:#4CAF50;color:white;padding:10px 20px;text-decoration:none;border-radius:4px;text-align:center;"),
                style="max-width:500px;margin:0 auto;padding:30px;background-color:white;border-radius:8px;box-shadow:0 2px 10px rgba(0,0,0,0.1);"
            ),
            request=None
        )
    )

@rt('/repay')
def repay(request, booking_id: str = "", amount: str = ""):
    # Check if user is logged in
    customer_id = request.cookies.get("customer_id")
    if not customer_id:
        return RedirectResponse(url="/login")
    
    # Find the booking
    booking = None
    if hasattr(booking_controller, 'bookings'):
        for b in booking_controller.bookings:
            if b.booking_id == booking_id:
                booking = b
                break
    
    # Check if booking exists and belongs to this user
    if not booking or str(booking.customer.customer_id) != str(customer_id):
        return Titled(
            "Error",
            *create_page_structure(
                Container(
                    H1("Error", style="color:red;text-align:center;"),
                    P("Booking not found or unauthorized access.", style="text-align:center;"),
                    A("Back to Profile", href="/profile", 
                      style="display:block;text-align:center;margin-top:20px;color:#4CAF50;")
                ),
                request=request
            )
        )
    
    # Check if booking is pending
    if booking.status != "Pending":
        return Titled(
            "Error",
            *create_page_structure(
                Container(
                    H1("Error", style="color:red;text-align:center;"),
                    P("This booking doesn't require payment.", style="text-align:center;"),
                    A("Back to Profile", href="/profile", 
                      style="display:block;text-align:center;margin-top:20px;color:#4CAF50;")
                ),
                request=request
            )
        )
    
    # Redirect to the payment page
    return Titled(
        "Complete Payment - CE ISAN HOUSE",
        *create_page_structure(
            Container(
                H1("Complete Your Payment", style="text-align:center;margin-bottom:30px;"),
                
                # Booking details summary
                Div(
                    H3("Booking Details", style="margin-bottom:15px;"),
                    P(f"Booking ID: {booking_id}", style="margin:5px 0;"),
                    P(f"Movie: {booking.showtime.movie.name}", style="margin:5px 0;"),
                    P(f"Date: {booking.timestamp}", style="margin:5px 0;"),
                    P(f"Time: {booking.showtime.time}", style="margin:5px 0;"),
                    P(f"Theater: {booking.showtime.theater.name}", style="margin:5px 0;"),
                    P(f"Seats: {', '.join(booking.seats)}", style="margin:5px 0;"),
                    P(f"Total Amount: ${amount}", style="margin:5px 0;font-weight:bold;"),
                    style="background-color:#f8f8f8;padding:15px;border-radius:8px;margin-bottom:30px;"
                ),
                
                # Payment method selection
                Form(
                    # Credit card option
                    Div(
                        Input(type="radio", id="card", name="payment_method", value="card", checked="checked"),
                        Label("Credit/Debit Card", for_="card", style="margin-left:10px;"),
                        style="margin:15px 0;padding:15px;background-color:#f9f9f9;border-radius:5px;border:1px solid #ddd;cursor:pointer;"
                    ),
                    
                    # QR code option
                    Div(
                        Input(type="radio", id="qrcode", name="payment_method", value="qrcode"),
                        Label("QR Code Payment", for_="qrcode", style="margin-left:10px;"),
                        style="margin:15px 0;padding:15px;background-color:#f9f9f9;border-radius:5px;border:1px solid #ddd;cursor:pointer;"
                    ),
                    
                    # Hidden fields to pass booking info
                    Input(type="hidden", name="booking_id", value=booking_id),
                    Input(type="hidden", name="amount", value=str(amount)),
                    
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
                
                # Back to profile link
                Div(
                    A("← Back to Profile", href="/profile", 
                      style="color:#333;text-decoration:none;"),
                    style="margin-top:20px;text-align:center;"
                ),
                
                style="padding:30px;max-width:800px;margin:0 auto;background-color:white;border-radius:8px;box-shadow:0 2px 10px rgba(0,0,0,0.1);"
            ),
            request=request
        )
    )

@rt('/login')
def get(request=None):
    # Get query parameters
    required = request.query_params.get("required") if request else None
    redirect_url = request.query_params.get("redirect") if request else None
    message = request.query_params.get("message") if request else None
    error = request.query_params.get("error") if request else None
    
    return Titled(
        "Login - CE ISAN HOUSE",
        *create_page_structure(
            Container(
                H1("Login", style="text-align:center;margin-bottom:30px;"),
                
                # Show message if login is required for booking
                Div(
                    P("Please log in to continue with your booking.", 
                      style="color:white;text-align:center;"),
                    style="background-color:#ff9800;padding:10px;border-radius:4px;margin-bottom:20px;"
                ) if required else None,
                
                # Success message
                Div(
                    P("Your account has been created successfully. Please log in.", 
                      style="color:white;text-align:center;"),
                    style="background-color:#4CAF50;padding:10px;border-radius:4px;margin-bottom:20px;"
                ) if message == "account_created" else None,
                
                # Error message
                Div(
                    P("Invalid email or password. Please try again.", 
                      style="color:white;text-align:center;"),
                    style="background-color:#f44336;padding:10px;border-radius:4px;margin-bottom:20px;"
                ) if error == "invalid_credentials" else None,
                
                # Session error
                Div(
                    P("Your session has expired. Please log in again.", 
                      style="color:white;text-align:center;"),
                    style="background-color:#f44336;padding:10px;border-radius:4px;margin-bottom:20px;"
                ) if error == "invalid_session" else None,
                
                Form(
                    # Hidden field to pass the redirect URL if needed
                    Input(type="hidden", name="redirect", value=redirect_url) if redirect_url else None,
                    
                    # Regular login fields
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
            ),
            request=request
        )
    )

@rt('/login', methods=["POST"])
def login_post(email: str = Form(...), password: str = Form(...), redirect: str = Form(None)):
    # Find customer with matching email
    found_customer = None
    for customer in booking_controller.customer_list:
        if customer.email == email:
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
    
    # Check password
    if not found_customer.check_password(password):
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
    
    # Login successful - redirect to the requested page or profile page
    redirect_url = redirect if redirect else "/profile"
    response = RedirectResponse(url=redirect_url, status_code=303)
    response.set_cookie(key="customer_id", value=found_customer.customer_id)
    return response

# Signup Page Route
@rt('/signup')
def get():
    return Titled(
        "Sign Up - CE ISAN HOUSE",
        *create_page_structure(
            Container(
                H1("Create an Account", style="text-align:center;margin-bottom:30px;"),
                Form(
                    Div(
                        Label("Full Name", for_="name", style="display:block;margin-bottom:5px;font-weight:bold;"),
                        Input(type="text", id="name", name="name", placeholder="Enter your full name", 
                              required="required", style="width:100%;padding:10px;margin-bottom:20px;border:1px solid #ddd;border-radius:4px;"),
                    ),
                    Div(
                        Label("Email", for_="email", style="display:block;margin-bottom:5px;font-weight:bold;"),
                        Input(type="email", id="email", name="email", placeholder="Enter your email", 
                              required="required", style="width:100%;padding:10px;margin-bottom:20px;border:1px solid #ddd;border-radius:4px;"),
                    ),
                    Div(
                        Label("Password", for_="password", style="display:block;margin-bottom:5px;font-weight:bold;"),
                        Input(type="password", id="password", name="password", placeholder="Choose a password",
                              required="required", style="width:100%;padding:10px;margin-bottom:20px;border:1px solid #ddd;border-radius:4px;"),
                    ),
                    Div(
                        Label("Confirm Password", for_="confirm_password", style="display:block;margin-bottom:5px;font-weight:bold;"),
                        Input(type="password", id="confirm_password", name="confirm_password", placeholder="Confirm your password",
                              required="required", style="width:100%;padding:10px;margin-bottom:20px;border:1px solid #ddd;border-radius:4px;"),
                    ),
                    Div(
                        Button("Sign Up", type="submit", style="background-color:#4CAF50;color:white;padding:10px 20px;border:none;border-radius:4px;cursor:pointer;font-size:16px;width:100%;"),
                        style="margin-top:20px;"
                    ),
                    Div(
                        P("Already have an account?", style="display:inline;margin-right:5px;"),
                        A("Login", href="/login", style="color:#4CAF50;text-decoration:none;"),
                        style="margin-top:20px;text-align:center;"
                    ),
                    method="post",
                    action="/signup",
                    style="max-width:400px;margin:0 auto;padding:20px;background-color:#f9f9f9;border-radius:8px;box-shadow:0 2px 10px rgba(0,0,0,0.1);"
                )
            )
        )
    )

# Signup Post Handler
@rt('/signup', methods=["POST"])
def signup_post(name: str = Form(...), email: str = Form(...), 
               password: str = Form(...), confirm_password: str = Form(...)):
    
    # Validate input
    errors = []
    
    if len(name.strip()) < 2:
        errors.append("Name must be at least 2 characters long")
    
    # Check if email is valid format
    if '@' not in email or '.' not in email:
        errors.append("Please enter a valid email address")
    
    # Check if email already exists
    for customer in booking_controller.customer_list:
        if customer.email == email:
            errors.append("This email is already registered")
            break
    
    # Validate password
    if len(password) < 5:
        errors.append("Password must be at least 5 characters long")
    
    # Check if passwords match
    if password != confirm_password:
        errors.append("Passwords do not match")
    
    # If there are validation errors, show them
    if errors:
        return Titled(
            "Sign Up Failed",
            *create_page_structure(
                Container(
                    H1("Sign Up Failed", style="text-align:center;color:#f44336;"),
                    Div(
                        H3("Please fix the following errors:", style="margin-bottom:10px;"),
                        Ul(*[Li(error, style="color:#f44336;margin-bottom:5px;") for error in errors]),
                        style="background-color:#ffebee;padding:15px;border-radius:8px;margin-bottom:20px;"
                    ),
                    A("Back to Sign Up", href="/signup", 
                      style="display:inline-block;background-color:#4CAF50;color:white;padding:10px 20px;border-radius:4px;text-decoration:none;text-align:center;")
                )
            )
        )
    
    # Create new customer
    customer_id = f"C{uuid.uuid4().hex[:8].upper()}"
    new_customer = Customer(customer_id, name, email, password)
    booking_controller.append_customer(new_customer)
    
    # Show success message and redirect to login
    return Titled(
        "Sign Up Successful",
        *create_page_structure(
            Container(
                H1("Account Created Successfully!", style="text-align:center;color:#4CAF50;"),
                P("Your account has been created. You can now log in with your email and password.", 
                  style="text-align:center;margin-bottom:30px;"),
                Div(
                    A("Log In Now", href="/login", 
                      style="background-color:#4CAF50;color:white;padding:10px 20px;border-radius:4px;text-decoration:none;"),
                    style="text-align:center;"
                )
            )
        )
    )

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
    
### history ###
@rt("/history")
def history_page(request=None):
    # Get all bookings from the booking controller
    all_bookings = booking_controller.booking_list if hasattr(booking_controller, 'booking_list') else []
    
    # Sort bookings by timestamp (most recent first)
    sorted_bookings = sorted(all_bookings, 
                           key=lambda x: datetime.strptime(x.timestamp, "%Y-%m-%d %H:%M:%S"),
                           reverse=True)

    return Titled(
        "Booking History - CE ISAN HOUSE",
        *create_page_structure(
            Container(
                H1("Booking History", style="text-align:center;margin-bottom:30px;"),
                
                # Filters and search (could be expanded later)
                Div(
                    Form(
                        Input(type="search", name="search", 
                              placeholder="Search bookings...",
                              style="padding:8px;width:200px;margin-right:10px;border:1px solid #ddd;border-radius:4px;"),
                        Button("Search", type="submit",
                               style="padding:8px 15px;background-color:#4CAF50;color:white;border:none;border-radius:4px;cursor:pointer;"),
                        method="get",
                        style="margin-bottom:20px;"
                    ),
                    style="text-align:right;"
                ),
                
                # Bookings table
                Div(
                    Table(
                        # Table header
                        Tr(
                            Th("Booking ID", style="padding:12px;background-color:#f5f5f5;"),
                            Th("Movie", style="padding:12px;background-color:#f5f5f5;"),
                            Th("Date & Time", style="padding:12px;background-color:#f5f5f5;"),
                            Th("Seats", style="padding:12px;background-color:#f5f5f5;"),
                            Th("Status", style="padding:12px;background-color:#f5f5f5;"),
                            Th("Total Price", style="padding:12px;background-color:#f5f5f5;"),
                            style="border-bottom:2px solid #ddd;"
                        ),
                        # Table rows
                        *[
                            Tr(
                                Td(booking.booking_id, 
                                   style="padding:12px;border-bottom:1px solid #eee;"),
                                Td(booking.showtime.movie.name, 
                                   style="padding:12px;border-bottom:1px solid #eee;"),
                                Td(booking.timestamp, 
                                   style="padding:12px;border-bottom:1px solid #eee;"),
                                Td(", ".join(booking.seats), 
                                   style="padding:12px;border-bottom:1px solid #eee;"),
                                Td(
                                    Span(
                                        booking.status,
                                        style=f"padding:4px 8px;border-radius:4px;font-size:0.9em;color:white;background-color:" + 
                                              {"Confirmed": "#4CAF50",
                                               "Pending": "#FFA500",
                                               "Cancelled": "#f44336",
                                               "Refunded": "#2196F3"}.get(booking.status, "#999")
                                    ),
                                    style="padding:12px;border-bottom:1px solid #eee;"
                                ),
                                Td(f"${booking.total_price:.2f}", 
                                   style="padding:12px;border-bottom:1px solid #eee;"),
                                style="transition:background-color 0.3s;"
                            ) for booking in sorted_bookings
                        ],
                        style="width:100%;border-collapse:collapse;margin-bottom:30px;box-shadow:0 1px 3px rgba(0,0,0,0.1);"
                    ) if sorted_bookings else Div(
                        P("No booking history found.", 
                          style="text-align:center;color:#666;font-style:italic;padding:20px;")
                    ),
                    style="overflow-x:auto;"  # Makes table scrollable on mobile
                ),
                
                # Summary statistics
                Div(
                    H3("Summary", style="margin-bottom:15px;"),
                    P(f"Total Bookings: {len(sorted_bookings)}", style="margin:5px 0;"),
                    P(f"Confirmed Bookings: {len([b for b in sorted_bookings if b.status == 'Confirmed'])}", 
                      style="margin:5px 0;"),
                    P(f"Total Revenue: ${sum(b.total_price for b in sorted_bookings):.2f}", 
                      style="margin:5px 0;font-weight:bold;"),
                    style="background-color:#f9f9f9;padding:20px;border-radius:8px;margin-top:20px;"
                ),
                
                style="max-width:1200px;margin:0 auto;padding:20px;"
            ),
            request=request
        )
    )

@rt("/payment")
def payment_page(request=None, booking_id: str = "", amount: str = ""):
    # Find the booking
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
                request=request
            )
        )
    
    return Titled(
        "Payment Options - CE ISAN HOUSE",
        *create_page_structure(
            Container(
                H1("Select Payment Method", style="text-align:center;margin-bottom:30px;"),
                
                Div(
                    H3("Booking Details", style="margin-bottom:15px;"),
                    P(f"Booking ID: {booking_id}", style="margin:5px 0;"),
                    P(f"Total Amount: ${amount}", style="margin:5px 0;font-weight:bold;"),
                    style="background-color:#f8f8f8;padding:15px;border-radius:8px;margin-bottom:30px;"
                ),
                
                Form(
                    Div(
                        Input(type="radio", id="card", name="payment_method", value="card", checked="checked"),
                        Label("Credit/Debit Card", for_="card", style="margin-left:10px;"),
                        style="margin:15px 0;padding:15px;background-color:#f9f9f9;border-radius:5px;border:1px solid #ddd;cursor:pointer;"
                    ),
                    Div(
                        Input(type="radio", id="qrcode", name="payment_method", value="qrcode"),
                        Label("QR Code Payment", for_="qrcode", style="margin-left:10px;"),
                        style="margin:15px 0;padding:15px;background-color:#f9f9f9;border-radius:5px;border:1px solid #ddd;cursor:pointer;"
                    ),
                    Input(type="hidden", name="booking_id", value=booking_id),
                    Input(type="hidden", name="amount", value=amount),
                    Div(
                        Button(
                            "Continue to Payment", 
                            type="submit",
                            style="background-color:#4CAF50;color:white;padding:12px 30px;border:none;border-radius:4px;cursor:pointer;font-size:16px;width:100%;"
                        ),
                        style="margin-top:30px;"
                    ),
                    
                    action="/process-payment-method",
                    method="post",
                    style="max-width:500px;margin:0 auto;"
                ),
                
                style="padding:30px;max-width:800px;margin:0 auto;background-color:white;border-radius:8px;box-shadow:0 2px 10px rgba(0,0,0,0.1);"
            ),
            request=request
        )
    )

@rt("/process-payment-method", methods=["POST"])
def process_payment_method(payment_method: str = Form(...), booking_id: str = Form(...), amount: str = Form(...)):
    if payment_method == "card":
        return RedirectResponse(url=f"/card-payment?booking_id={booking_id}&amount={amount}", status_code=303)
    else:
        return RedirectResponse(url=f"/qrcode-payment?booking_id={booking_id}&amount={amount}", status_code=303)

@rt("/card-payment")
def card_payment_page(request, booking_id: str = "", amount: str = ""):
    # Find the booking
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
                request=request
            )
        )
    
    return Titled(
        "Card Payment - CE ISAN HOUSE",
        *create_page_structure(
            Container(
                H1("Card Payment", style="text-align:center;margin-bottom:30px;"),
                
                # Booking details summary
                Div(
                    H3("Booking Details", style="margin-bottom:15px;"),
                    P(f"Booking ID: {booking_id}", style="margin:5px 0;"),
                    P(f"Total Amount: ${amount}", style="margin:5px 0;font-weight:bold;"),
                    style="background-color:#f8f8f8;padding:15px;border-radius:8px;margin-bottom:30px;"
                ),
                
                # Credit card form
                Form(
                    # Card details
                    H3("Enter Card Details", style="margin-bottom:20px;"),
                    
                    Div(
                        Label("Card Number", for_="card_number", style="display:block;margin-bottom:5px;"),
                        Input(type="text", id="card_number", name="card_number", 
                              placeholder="1234 5678 9012 3456", required="required",
                              style="width:100%;padding:10px;border:1px solid #ddd;border-radius:4px;"),
                        style="margin-bottom:15px;"
                    ),
                    
                    Div(
                        Div(
                            Label("Expiration Date", for_="exp_date", style="display:block;margin-bottom:5px;"),
                            Input(type="text", id="exp_date", name="exp_date", 
                                  placeholder="MM/YY", required="required",
                                  style="width:100%;padding:10px;border:1px solid #ddd;border-radius:4px;"),
                            style="flex:1;margin-right:10px;"
                        ),
                        Div(
                            Label("CVC", for_="cvc", style="display:block;margin-bottom:5px;"),
                            Input(type="text", id="cvc", name="cvc", 
                                  placeholder="123", required="required",
                                  style="width:100%;padding:10px;border:1px solid #ddd;border-radius:4px;"),
                            style="flex:1;"
                        ),
                        style="display:flex;margin-bottom:15px;"
                    ),
                    
                    Div(
                        Label("Cardholder Name", for_="name", style="display:block;margin-bottom:5px;"),
                        Input(type="text", id="name", name="name", 
                              placeholder="John Doe", required="required",
                              style="width:100%;padding:10px;border:1px solid #ddd;border-radius:4px;"),
                        style="margin-bottom:25px;"
                    ),
                    
                    # Hidden fields
                    Input(type="hidden", name="booking_id", value=booking_id),
                    Input(type="hidden", name="amount", value=amount),
                    
                    # Submit button
                    Div(
                        Button("Complete Payment", type="submit", 
                               style="background-color:#4CAF50;color:white;padding:12px 0;border:none;border-radius:4px;cursor:pointer;font-size:16px;width:100%;"),
                        style="margin-top:15px;"
                    ),
                    
                    action="/verify-card-payment",
                    method="post",
                    style="max-width:400px;margin:0 auto;"
                ),
                
                # Back link
                Div(
                    A("← Back to Payment Methods", href=f"/payment?booking_id={booking_id}&amount={amount}", 
                      style="color:#333;text-decoration:none;"),
                    style="margin-top:20px;text-align:center;"
                ),
                
                style="padding:30px;max-width:800px;margin:0 auto;background-color:white;border-radius:8px;box-shadow:0 2px 10px rgba(0,0,0,0.1);"
            ),
            request=request
        )
    )

@rt("/qrcode-payment")
def qrcode_payment_page(request, booking_id: str = "", amount: str = ""):
    # Find the booking
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
                request=request
            )
        )
    
    # Generate QR code
    import qrcode
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(f"CE-ISAN-HOUSE-PAYMENT:{booking_id}:{amount}")
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Save to BytesIO
    import io
    from base64 import b64encode
    
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    qr_image_b64 = b64encode(buffer.getvalue()).decode('utf-8')
    
    return Titled(
        "QR Code Payment - CE ISAN HOUSE",
        *create_page_structure(
            Container(
                H1("QR Code Payment", style="text-align:center;margin-bottom:30px;"),
                
                # Booking details summary
                Div(
                    H3("Booking Details", style="margin-bottom:15px;"),
                    P(f"Booking ID: {booking_id}", style="margin:5px 0;"),
                    P(f"Total Amount: ${amount}", style="margin:5px 0;font-weight:bold;"),
                    style="background-color:#f8f8f8;padding:15px;border-radius:8px;margin-bottom:30px;"
                ),
                
                # QR code display
                Div(
                    H3("Scan QR Code to Pay", style="margin-bottom:15px;text-align:center;"),
                    P("Use your banking app to scan this QR code and complete the payment.", 
                      style="text-align:center;margin-bottom:20px;"),
                    Div(
                        Img(src=f"data:image/png;base64,{qr_image_b64}", 
                            alt="QR Code for payment",
                            style="max-width:250px;margin:0 auto;display:block;"),
                        style="text-align:center;margin-bottom:30px;"
                    ),
                    P("The QR code is valid for 15 minutes.", style="text-align:center;color:#777;font-style:italic;"),
                    style="background-color:#f9f9f9;padding:20px;border-radius:8px;margin-bottom:30px;"
                ),
                
                Form(
                    Input(type="hidden", name="booking_id", value=booking_id),
                    Input(type="hidden", name="amount", value=amount),
                    Div(
                        Button(
                            "I've Completed the Payment", 
                            type="submit",
                            style="background-color:#4CAF50;color:white;padding:12px 30px;border:none;border-radius:4px;cursor:pointer;font-size:16px;"
                        ),
                        style="margin-top:20px;text-align:center;"
                    ),
                    
                    action="/verify-qr-payment",
                    method="post",
                    style="max-width:500px;margin:0 auto;"
                ),
                
                Div(
                    A("← Back to Payment Methods", href=f"/payment?booking_id={booking_id}&amount={amount}", 
                      style="color:#333;text-decoration:none;"),
                    style="margin-top:20px;text-align:center;"
                ),
                
                style="padding:30px;max-width:800px;margin:0 auto;background-color:white;border-radius:8px;box-shadow:0 2px 10px rgba(0,0,0,0.1);"
            ),
            request=request
        )
    )

@rt("/process-card-payment", methods=["POST"])
def process_card_payment(booking_id: str = Form(...), amount: str = Form(...), 
                        card_number: str = Form(...), cardholder: str = Form(...),
                        expiry: str = Form(...), cvv: str = Form(...)):
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
    
    # In a real system, you'd validate and process the payment here
    # For this demo, we'll simulate a successful payment
    
    # Update booking status
    booking.status = "Confirmed"
    
    # Generate receipt and confirmation
    return receipt_page(booking_id, amount, "card", cardholder)

@rt("/verify-card-payment", methods=["POST"])
def verify_card_payment(request, booking_id: str = Form(...), amount: str = Form(...), 
                      card_number: str = Form(...), exp_date: str = Form(...), 
                      cvc: str = Form(...), name: str = Form(...)):
    # Find the booking
    booking = None
    if hasattr(booking_controller, 'bookings'):
        for b in booking_controller.bookings:
            if b.booking_id == booking_id:
                booking = b
                break
    
    if not booking:
        return RedirectResponse(url="/", status_code=303)
    
    # In a real system, you would validate the card and process payment
    # For this demo, we'll just mark the booking as confirmed
    booking.status = "Confirmed"
    
    # Generate a transaction ID
    transaction_id = f"TXN{booking.booking_id}"
    
    # Render receipt page
    return Titled(
        "Payment Successful - CE ISAN HOUSE",
        *create_page_structure(
            Container(
                H1("Payment Successful!", style="text-align:center;color:#4CAF50;margin-bottom:30px;"),
                
                # Receipt details
                Div(
                    H2("Receipt", style="text-align:center;margin-bottom:20px;"),
                    P(f"Booking ID: {booking_id}", style="margin:8px 0;"),
                    P(f"Movie: {booking.showtime.movie.name}", style="margin:8px 0;"),
                    P(f"Date: {datetime.now().strftime('%Y-%m-%d')}", style="margin:8px 0;"),
                    P(f"Time: {booking.showtime.time}", style="margin:8px 0;"),
                    P(f"Theater: {booking.showtime.theater.name}", style="margin:8px 0;"),
                    P(f"Seats: {', '.join(booking.seats)}", style="margin:8px 0;"),
                    P(f"Amount Paid: ${amount}", style="margin:8px 0;font-weight:bold;"),
                    P(f"Payment Method: Card", style="margin:8px 0;"),
                    P(f"Card Number: ****{card_number[-4:]}", style="margin:8px 0;"),
                    P(f"Transaction ID: {transaction_id}", style="margin:8px 0;"),
                    P(f"Payment Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", style="margin:8px 0;"),
                    style="background-color:#f9f9f9;padding:20px;border-radius:8px;margin-bottom:30px;border:1px solid #ddd;"
                ),
                
                # E-ticket section - create a simple QR code placeholder
                Div(
                    H3("Your E-Ticket", style="text-align:center;margin-bottom:15px;"),
                    P("Scan this QR code at the cinema.", 
                      style="text-align:center;margin-bottom:20px;"),
                    Div(
                        Img(src=f"https://api.qrserver.com/v1/create-qr-code/?data=CEIsanHouse-Ticket-{booking_id}&size=200x200", 
                            alt="Ticket QR Code",
                            style="max-width:200px;margin:0 auto;display:block;"),
                        style="text-align:center;margin-bottom:30px;"
                    ),
                    style="background-color:#f0f8ff;padding:20px;border-radius:8px;margin-bottom:30px;border:1px solid #cce5ff;"
                ),
                
                # Navigation buttons
                Div(
                    A("View My Bookings", href="/profile", 
                      style="display:inline-block;background-color:#4CAF50;color:white;padding:10px 20px;text-decoration:none;border-radius:4px;margin-right:15px;"),
                    A("Back to Homepage", href="/", 
                      style="display:inline-block;background-color:#333;color:white;padding:10px 20px;text-decoration:none;border-radius:4px;"),
                    style="text-align:center;"
                ),
                
                style="max-width:600px;margin:0 auto;padding:30px;background-color:white;border-radius:8px;box-shadow:0 2px 10px rgba(0,0,0,0.1);"
            ),
            request=request
        )
    )

@rt("/verify-qr-payment", methods=["POST"])
def verify_qr_payment(request, booking_id: str = Form(...), amount: str = Form(...)):
    # Find the booking
    booking = None
    if hasattr(booking_controller, 'bookings'):
        for b in booking_controller.bookings:
            if b.booking_id == booking_id:
                booking = b
                break
    
    if not booking:
        return RedirectResponse(url="/", status_code=303)
    
    # In a real system, you would verify QR payment status
    # For this demo, we'll just mark the booking as confirmed
    booking.status = "Confirmed"
    
    # Generate a transaction ID
    transaction_id = f"TXN{booking.booking_id}"
    
    # Render receipt page
    return Titled(
        "Payment Successful - CE ISAN HOUSE",
        *create_page_structure(
            Container(
                H1("Payment Successful!", style="text-align:center;color:#4CAF50;margin-bottom:30px;"),
                
                # Receipt details
                Div(
                    H2("Receipt", style="text-align:center;margin-bottom:20px;"),
                    P(f"Booking ID: {booking_id}", style="margin:8px 0;"),
                    P(f"Movie: {booking.showtime.movie.name}", style="margin:8px 0;"),
                    P(f"Date: {datetime.now().strftime('%Y-%m-%d')}", style="margin:8px 0;"),
                    P(f"Time: {booking.showtime.time}", style="margin:8px 0;"),
                    P(f"Theater: {booking.showtime.theater.name}", style="margin:8px 0;"),
                    P(f"Seats: {', '.join(booking.seats)}", style="margin:8px 0;"),
                    P(f"Amount Paid: ${amount}", style="margin:8px 0;font-weight:bold;"),
                    P(f"Payment Method: QR Code", style="margin:8px 0;"),
                    P(f"Transaction ID: {transaction_id}", style="margin:8px 0;"),
                    P(f"Payment Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", style="margin:8px 0;"),
                    style="background-color:#f9f9f9;padding:20px;border-radius:8px;margin-bottom:30px;border:1px solid #ddd;"
                ),
                
                # E-ticket section - create a simple QR code placeholder
                Div(
                    H3("Your E-Ticket", style="text-align:center;margin-bottom:15px;"),
                    P("Scan this QR code at the cinema.", 
                      style="text-align:center;margin-bottom:20px;"),
                    Div(
                        Img(src=f"https://api.qrserver.com/v1/create-qr-code/?data=CEIsanHouse-Ticket-{booking_id}&size=200x200", 
                            alt="Ticket QR Code",
                            style="max-width:200px;margin:0 auto;display:block;"),
                        style="text-align:center;margin-bottom:30px;"
                    ),
                    style="background-color:#f0f8ff;padding:20px;border-radius:8px;margin-bottom:30px;border:1px solid #cce5ff;"
                ),
                
                # Navigation buttons
                Div(
                    A("View My Bookings", href="/profile", 
                      style="display:inline-block;background-color:#4CAF50;color:white;padding:10px 20px;text-decoration:none;border-radius:4px;margin-right:15px;"),
                    A("Back to Homepage", href="/", 
                      style="display:inline-block;background-color:#333;color:white;padding:10px 20px;text-decoration:none;border-radius:4px;"),
                    style="text-align:center;"
                ),
                
                style="max-width:600px;margin:0 auto;padding:30px;background-color:white;border-radius:8px;box-shadow:0 2px 10px rgba(0,0,0,0.1);"
            ),
            request=request
        )
    )

serve()
