```mermaid
classDiagram
    %% User Management
    Visitor <|-- Guest
    Visitor <|-- Customer
    Customer <|-- Member
    Customer <|-- Regular

    %% Booking Flow
    Customer --> Booking : makes
    Visitor --> Movie : search
    Booking --> Food : orders
    Booking --> Showtime : books
    BookingController --> Booking : manages
    BookingController o-- Movie : manages
    BookingController o-- Theater : manages
    BookingController o-- Customer : manages
    BookingController o-- Food : manages

    %% Theater Management
    Theater *-- Seat : contains
    SeatBooked --|> Seat
    SeatBooked <-- Ticket
    Showtime --> Theater : uses
    Showtime --> SeatBooked : tracks
    Movie o-- Showtime : has
    FoodOrder --|> Food

    %% Payment Flow
    Booking --> Payment : has
    Booking --> Ticket : generates
    Ticket --> QrTicket : generates
    Payment --> Debit_card : uses
    Payment --> Credit_card : uses
    Payment --> QrPayment : uses

    class BookingController{
        -movieList: List~Movie~
        -theaterList: List~Theater~
        -bookingList: List~Booking~
        -customerList: List~Customer~
        -foodList: List~Food~
        +addBooking(Booking)
        +cancelBooking(bookingId)
        +getBooking(bookingId)
        +getCustomerBookings(customerId)
    }

    class Movie{
        -movieId: string
        -title: string
        -trailer: string
        -description: string
        -duration: int
        -genre: string[]
        -showtimeList: List~Showtime~
        +addShowtime(Showtime)
        +getShowtimes()
        +isAvailable()
    }

    class Showtime {
        -showtimeId: string
        -movie: Movie
        -theater: Theater
        -date: Date
        -time: Time
        -price: decimal
        -bookedSeats: List~SeatBooked~
        +getAvailableSeats()
        +isAvailable()
    }

    class Theater {
        -theaterId: string
        -name: string
        -seatList: List~Seat~
        +getSeatMap()
    }


    class Seat{
        -seatId: string
        -row: string
        -number: int
        -type: string
        -price: decimal
        +isAvailable()
    }

    class SeatBooked {
        -seatId: string
        -status: string
        -bookingId: string
        +updateStatus(status)
    }

    class Booking{
        -bookingId: string
        -showtime: Showtime
        -selectedSeats: List~SeatBooked~
        -foodList: List~FoodOrder~
        -totalPrice: decimal
        -status: string
        -createdAt: datetime
        +calculateTotal()
        +confirmBooking()
        +cancelBooking()
    }

    class FoodOrder{
        -food: Food
        -quantity: int
        -subtotal: decimal
        +updateQuantity()
        +calculateSubtotal()
    }

    class Food{
        -foodId: string
        -name: string
        -description: string
        -price: decimal
        -quantity: int
        +isAvailable()
        +updateStock()
    }

    class Ticket{
        -ticketId: string
        -booking: Booking
        -seat: SeatBooked
        -status: string
        +generateQR()
        +validate()
        +cancel()
    }

    class QrTicket{
        -qrCodeId: string
        -content: string
        +generate()
        +validate()
    }

    class Payment{
        -paymentId: string
        -booking: Booking
        -amount: decimal
        -method: string
        -status: string
        +processPayment()
        +validatePayment()
        +getStatus()
    }

    class QrPayment{
        -qrCodeId: string
        -expiryTime: datetime
        +generateQRCode()
        +validateQRCode()
        +checkExpiry()
    }

    class Debit_card{
        -cardId: string
        -cardNumber: string
        -cardHolder: string
        -expiryDate: date
        -cvv: string
        +validateCard()
        +processPayment()
    }

    class Credit_card{
        -cardId: string
        -cardNumber: string
        -cardHolder: string
        -expiryDate: date
        -cvv: string
        +validateCard()
        +processPayment()
    }

    class Visitor{
        +browseMovies()
        +searchMovies()
        +viewShowtimes()
    }

    class Guest{
        +signIn()
        +signUp()
    }

    class Customer {
        -customerId: string
        -name: string
        -email: string
        -bookingList: List~Booking~
        -ticketList: List~Ticket~
        +bookTicket()
        +cancelTicket()
        +viewBookingHistory()
        +viewTickets()
        +signOut()
    }

    class Member{
        -points: int
        -paymentDetails: List~PaymentMethod~
        +redeemPoints()
        +earnPoints()
        +getPointBalance()
    }

    class Regular{
        +upgradeToMember()
    }
```
