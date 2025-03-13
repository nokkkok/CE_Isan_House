```mermaid
sequenceDiagram

    Customer->>+UI: select movie
    UI->>+BookingController: select_movie(movie_id)
    loop
    BookingController->>+Movie: check_Movie(movie_id)
    Movie-->>-BookingController: Movie
    end
    BookingController->>+Movie: get_showtimes
    Movie-->>-BookingController: Showtime_list
    BookingController-->>-UI:Movie Showtime_list
    UI->>Customer:display Movie Showtime
    UI->>+BookingController: select_showtime(showtime_id)
    BookingController->>+Showtime: get_available_seats()
    Showtime-->>-BookingController: available_seats_list
    BookingController-->>-UI: available_seats_list
    UI->>Customer: display available seats
    UI->>+BookingController: choose_seats(seat_list)
    BookingController->>BookingController: confirm_booking
    BookingController->>+Payment: make_payment
    Payment-->>-BookingController: Confirm
    BookingController->>+QrTicket:  generate
    QrTicket-->>-BookingController: return qr_ticket
    BookingController-->>-UI:qr_code
    UI->>-Customer:display qr_code
    ```mermaid
