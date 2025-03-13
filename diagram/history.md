```mermaid
sequenceDiagram
  participant Customer
  participant UI
  participant Booking as BookingController

  Customer ->>+ UI: กด Booking History
  loop
  UI ->>+ Booking: get_customer_bookings(customer_id)
  Booking -->>- UI: ส่งรายการ booking_list
  end
  UI ->>- Customer: แสดงรายการประวัติการจอง
```mermaid