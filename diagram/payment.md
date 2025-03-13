```mermaid
sequenceDiagram
  participant Customer
  participant UI
  participant Payment
  participant Booking as BookingController
  participant Card
  participant Qrpayment
  participant SeatBooked
%%   participant Theater

  Customer ->>+ UI: กดปุ่มชำระเงิน
    alt
    UI ->>+ Payment: make_payment(Card)
    Payment->>+Card: validate_Card()
    Card-->>-Payment:return Card
    Payment->>Payment: process_payment
    else 
    UI ->> Payment: make_payment(QrParment)
    Payment->>+QrPayment:generate_qr_code
    QrPayment-->>-Payment:return qr_payment
    Payment->>Payment: process_payment
    end
Note over Booking: เริ่มจับเวลา (Timer)
  alt ชำระเงินทันเวลา
    Payment->>+Booking:update_booking_status("success")
    Booking->>+SeatBooked:update_status("booked")
    SeatBooked-->>-Booking:Payment Success
    Booking -->>- Payment: return Payment Success
    Payment-->>UI: display_Success
    UI ->> Customer: แสดงข้อความ Confirmed
  else เวลาหมดก่อนชำระเงิน
    Payment->>+Booking:cancel_payment
    Booking->>+SeatBooked:update_status("available")
    SeatBooked-->>-Booking:Payment Unsuccess
    Booking -->>-Payment: return Payment Unsuccess
    Payment-->>-UI: display_Unsuccess
    UI ->>- Customer: แสดงข้อความ cancelled
  end
```mermaid

