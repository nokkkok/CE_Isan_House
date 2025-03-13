```mermaid
sequenceDiagram
    User ->>+ UI: เลือกใช้แต้ม (Redeem Points)
    loop
    UI ->>+ BookingController: check_booking_id (booking_id)
    BookingController -->>- UI: booking
    end
    UI ->>+ Customer: get_points_balance
    Customer -->>- UI: Point
    alt แต้มเพียงพอ
        UI ->>+ Customer: redeem_points
        Customer -->>- UI: True
        UI ->> User: อัปเดตราคา + Redirect ไปหน้า Payment
    else แต้มไม่พอ
        UI ->> User: แสดงข้อผิดพลาด + Redirect ไปหน้า Payment
    end
```mermaid