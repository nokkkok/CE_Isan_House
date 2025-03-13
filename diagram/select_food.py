```mermaid
sequenceDiagram
    participant User
    participant BookingController
    participant Booking
    participant Food

    User->>BookingController: POST /process-food-selection
    BookingController->>Booking: Find Booking by ID
    BookingController-->>User: Return Booking
    alt Booking Not Found
        BookingController->>User: Redirect to Homepage
    else Booking Found
        Booking->>Booking: Process Food Selection
        loop For Each Food Item in Form
            Booking->>BookingController: Find Food Item by ID
            BookingController-->>Booking: Return Food Item
            alt Food Item Available
                Booking->>Booking: Add Food Order to Booking
                Booking->>Food: Update Food Quantity
            else Food Item Not Available
                Booking->>BookingController: Log Error
            end
        end
        Booking->>Booking: Calculate Total Price
        BookingController->>User: Redirect to Payment Page with Updated Amount
    end
    ```mermaid
