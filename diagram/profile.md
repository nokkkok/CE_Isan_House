```mermaid
sequenceDiagram
    User ->>+ UI : กดปุ่ม Profile
    loop
    UI ->> UI : Check customer_id
    end
    alt Customer ID exists
    loop
        UI ->>+ BookingController : find_customer_by_id(customer_id)   
        BookingController ->>+ Customer : Fetch customer data
        Customer -->>- BookingController : Return customer details
        BookingController -->>- UI : Return customer
    end
        UI ->> User : Display Profile Page
    else Customer ID not found
        UI ->>- User : Redirect to Login Page
    end
```mermaid