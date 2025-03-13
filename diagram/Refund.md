```mermaid
sequenceDiagram
  participant Customer as Customer
  participant UI as UI
  participant BookingController as BookingController
  participant Booking as Booking
  participant Payment as Payment
  participant Ticket as Ticket

  Customer ->>+ UI: กดปุ่ม Request Refund
  UI ->>+ BookingController: request_refund
  loop
    BookingController ->>+ Booking: check_booking_id()
    Booking -->>- BookingController: return booking
  end
 
    BookingController ->>+ Payment: process_refund(booking)
    Payment -->>- BookingController: success
    BookingController ->>+ Booking: update_booking_status("refunded")
    Booking -->>- BookingController: status updated
    BookingController ->>+ Ticket: update_ticket_status("cancelled")
    Ticket -->>- BookingController: status updated


  BookingController -->>- UI: return refund result
  UI -->>- Customer: display Refund Successful!
```mermaid