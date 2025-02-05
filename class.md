<!-- Movies Ticket Reserved System -->

```mermaid
classDiagram

    %% AuthControllers
    AuthController --> BookingController : use
    Customer --> Booking : make

    %% Booking and Payment System
    BookingController --> Booking : handle
    BookingController o-- Movie : manage
    BookingController o-- Theater : manage

    Theater *-- Seat : has
    Movie o-- Showtime : has

    Booking --> Payment : has
    Booking --> Ticket : generates
    Ticket --> QrTicket : generates

    Payment --> Debit_card : uses
    Payment --> Credit_card : uses
    Payment --> QrPayment : uses

    %%User Roles and Authentication
    AuthController <-- Visitor
    Visitor <|-- Guest
    Visitor <|-- Customer
    Customer <|-- Member
    Customer <|-- Not_member


    class BookingController{
        -movie_list: list
        -theater_list: list
        -booking_list: list
        +add_booking()
        +cancel_booking()
        +show_booking()
    }
    
    class Movie{
        -movie_id
        -title
        -trailer
        -description
        -duration
        -genre
        -showtime_list: list
        +add_showtime()
        +get_showtime()
        -validate_showtime()
    }

    class Showtime{
        -showtime_id
        -Movie movie
        -Theater theater
        -date
        -time
    }

    class Theater{
        -theater_id
        -seat_list: list
        +get_available_seat(showtime_id)
        -validate_theater()
    }

    class Seat{
        -seat_id
        -seat_type
        -status
        +validate_seat()
    }

    class Booking{
        -booking_id
        -Showtime showtime
        -selected_seat_list: list
        -total_price
        -status
    }

    class Ticket{
        -ticket_id
        -Booking booking
        -status
        +validate_ticket()
    }

    class QrTicket{
        -qr_code_id
    }

    class Payment{
        -payment_id
        -booking
        -payment_method
        -status
        +make_payment()
        +cancel_payment()
        +update_member_point()
        +validate_payment()
    }

    class QrPayment{
        -qr_code_id
        -booking
        -status
        +generate_qr_code()
        +validate_qr_code()
    }

    class Debit_card{
        -card_id
        -card_no
        -card_holder
        -expire_date
        -cvv
        -balance
        +validate_card()
        +make_payment()
    }

    class Credit_card{
        -card_id
        -card_no
        -card_holder
        -expire_date
        -cvv
        -balance
        +validate_card()
        +make_payment()
    }

    class AuthController{
        +sign_in()
        +sign_up()
        +sign_out()
    }

    class Visitor{
        +browse_movie()
    }

    class Guest{
        
    }

    class Customer {
        -name
        -email
        -customer_id
        -membership_status
        +book_ticket()
        +refund_ticket()
    }

    class Member{
        -Point
        +redeem_point()
    }

    class Not_member{
        +upgrade_to_member()
    }
```