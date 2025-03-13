```mermaid
sequenceDiagram
  participant Guest/Customer as Guest/Customer
  participant UI as UI
  participant BookingController as BookingController
  participant Movie as Movie

  Guest/Customer ->>+ UI: กดค้นหาหนัง
  UI ->>+ BookingController: search_movie
  loop 
    BookingController ->>+ Movie: search_movie(movie_name)
    Movie -->>- BookingController: return movie
  end
  BookingController -->>- UI: return_Movie_details()
  UI -->>- Guest/Customer: แสดงรายละเอียดและตัวอย่างหนัง

```mermaid