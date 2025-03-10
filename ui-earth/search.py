from fasthtml.common import *

# ตัวอย่างข้อมูลหนัง
movie_data = [
    {"name": "The shawshank edemption", "year": 1994},
    {"name": "The Godfather", "year": 1972},
    {"name": "The Dark Knight", "year": 2008},
    {"name": "Pulp Fiction", "year": 1994},
    {"name": "Forrest Gump", "year": 1994},
    {"name": "Inception", "year": 2010},
    {"name": "The Matrix", "year": 1999},
    {"name": "Interstellar", "year": 2014},
]

class Visitor:
    def __init__(self, name: str):
        self.__name = name
        
    def search_movie(self, booking_controller, movie_name):
        return booking_controller.search_movie(movie_name)

class BookingController:
    def __init__(self):
        self.__movie_list = movie_data  # กำหนดข้อมูลหนังที่ใช้ค้นหา
    
    def search_movie(self, movie_name):
        # ค้นหาภาพยนตร์ที่มีชื่อคล้ายกับคำค้นหา
        result = [movie for movie in self.__movie_list if movie_name.lower() in movie['name'].lower()]
        return result

app, rt = fast_app()

@rt('/')
def get():
    return Titled("Movie",
        Form(
            Div(
                Input(id="search", placeholder="Search movie..."),
                Button("Search", type="submit")
            ),
            hx_get="/search", target_id="results", hx_trigger="submit"
        ),
        Div(id="results"),
        Div(id="selected-movie")
    )
    
@rt('/search')
def get(search: str):
    visitor = Visitor("guest")
    booking_controller = BookingController()
    results = visitor.search_movie(booking_controller, search)
    # return Div(*[Card(H3(p["name"]), P(p["year"]))for p in results])
    
    movie_cards = []
    for p in results:
        movie_card = Card(
            H3(p["name"]),
            P(f"Year: {p['year']}"),
            Button("Select", hx_get=f"/select-movie?id={p['name']}", hx_target="#selected-movie")
        )
        movie_cards.append(movie_card)
    
    return Div(*movie_cards, Div(id="selected-movie"))

@rt('/select-movie')
def get(id: str):
    # ในสถานการณ์จริง คุณอาจจะใช้ ID จริงๆ แทนที่จะใช้ชื่อหนัง
    # และคุณอาจจะต้องค้นหาข้อมูลเพิ่มเติมจากฐานข้อมูล
    
    visitor = Visitor("guest")
    booking_controller = BookingController()
    movies = booking_controller.search_movie(id)
    
    if movies:
        movie = movies[0]  # เอาหนังตัวแรกที่ตรงกับชื่อ
        return Div(
            H2(f"Selected Movie: {movie['name']}"),
            P(f"Year: {movie['year']}"),
            Button("Book Now", hx_post="/book-movie", hx_vals=f'{{"movie_name": "{movie["name"]}"}}')
        )
    else:
        return Div(P("Movie not found"))

serve()