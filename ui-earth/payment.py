from datetime import datetime
import time
import random
import uuid
import qrcode
import base64
from io import BytesIO
from fasthtml.common import *

class Booking:
    def __init__(self, booking_id: str, showtime, total_price: float, status: str = "Pending"):
        self.__booking_id = booking_id
        self.__showtime = showtime
        self.__selected_seats = []  # List of SeatBooked
        self.__food_list = []  # List of FoodOrder
        self.__total_price = total_price
        self.__status = status
        self.__created_at = datetime.now()
        
    def get_booking_id(self):
        return self.__booking_id
    
    @property    
    def status(self):
        return self.__status
    
    @status.setter
    def status(self, new_status):
        self.__status = new_status
    
    @property
    def total_price(self):
        return self.__total_price
    
    def calculate_total_price(self):
        # Calculate total price based on seats and food
        pass
    
    def confirm_booking(self):
        self.__status = "Confirmed"
        return True
    
    def cancel_booking(self):
        self.__status = "Cancelled"
        return True

class BookingController:
    def __init__(self):
        self.__movie_list = []  # List of Movie
        self.__theater_list = []  # List of Theater
        self.__booking_list = []  # List of Booking
        self.__customer_list = []  # List of Customer
        self.__food_list = []  # List of Food
        
    def get_booking_id(self, booking_id):
        for booking in self.__booking_list:
            if booking.get_booking_id() == booking_id:
                return booking
        return None
    
    def get_bookings(self):
        return self.__booking_list
        
    def search_movie(self, movie_name):
        result = [movie for movie in self.__movie_list if movie_name.lower() in movie.title.lower()]
        return result
    
    def update_booking_status(self, booking_id, status):
        booking = self.check_booking_id(booking_id)
        if isinstance(booking, Booking):
            if status == "success":
                booking.status = "Confirmed"
                # Update seat status
                return True
            else:
                booking.status = "Cancelled"
                # Update seat status
                return True
        return False
        
    def check_booking_id(self, booking_id):
        booking = self.get_booking_id(booking_id)
        if booking:
            return booking
        else:
            return "Booking ID not found"
    
    def create_booking(self, showtime, seats, total_price):
        booking_id = f"BK{uuid.uuid4().hex[:8].upper()}"
        booking = Booking(booking_id, showtime, total_price)
        self.__booking_list.append(booking)
        return booking
    
    def process_refund(self, booking):
        if booking and booking.status == "Confirmed":
            booking.status = "Refunded"
            return True
        return False     
    
    def update_ticket_status(self, ticket_id, status):
        for customer in self.__customer_list:
            for ticket in customer.ticket_list:
                if ticket.ticket_id == ticket_id:
                    ticket.status = status
                    return True
        return False
    
    def check_Movie(self, movie_id):
        for movie in self.__movie_list:
            if movie.movie_id == movie_id:
                return movie
        return None
    
    def append_movie(self, movie):
        self.__movie_list.append(movie)

    def append_theater(self, theater):
        self.__theater_list.append(theater)

    def append_booking(self, booking):
        self.__booking_list.append(booking)

    def append_customer(self, customer):
        self.__customer_list.append(customer)

    def append_food(self, food):
        self.__food_list.append(food)
    
class Payment:
    def __init__(self, payment_id: str, booking: Booking, amount: float, method: str, status: str = "Pending"):
        self.__payment_id = payment_id
        self.__booking = booking
        self.__amount = amount
        self.__method = method
        self.__status = status
        
    @property
    def method(self):
        return self.__method
    
    @property
    def status(self):
        return self.__status
    
    @status.setter
    def status(self, new_status):
        self.__status = new_status
    
    @property
    def amount(self):
        return self.__amount
        
    def make_payment(self, payment_method, booking_controller):
        start_time = time.time()
        timeout = 60
        
        if isinstance(payment_method, Card):
            validated_card = payment_method.validate_Card()
            if validated_card:
                result = self.process_payment(payment_method, booking_controller, start_time, timeout)
            else:
                result = "unsuccess"
        
        elif isinstance(payment_method, QrPayment):
            qr_code = payment_method.generate_qr_code(self.__amount)
            if qr_code:
                result = payment_method.verify_payment()
            else:
                result = "unsuccess"
        
        return result
        
    def process_payment(self, payment_method, booking_controller, start_time, timeout):
        if time.time() - start_time > timeout:
            result = self.cancel_payment(booking_controller)
            return result
        
        if isinstance(payment_method, Card):
            if payment_method.charge_card(self.__amount) == True:
                self.__status = "Success"
                result = booking_controller.update_booking_status(self.__booking.get_booking_id(), "success")
                return result
            else:
                self.__status = "Failed"
                result = booking_controller.update_booking_status(self.__booking.get_booking_id(), "unsuccess")
                return result
            
    def cancel_payment(self, booking_controller):
        cancel_status = booking_controller.update_booking_status(self.__booking.get_booking_id(), "unsuccess")
        return cancel_status
    
    def validate_payment(self):
        # Validate if payment is valid
        pass
    
    def get_status(self):
        return self.__status

class QrPayment:
    def __init__(self, qr_code_id: str, expiry_time):
        self.__qr_code_id = qr_code_id
        self.__expiry_time = expiry_time
        
    def generate_qr_code(self, amount):
        payment_data = f"CE_ISAN_PAYMENT:{self.__qr_code_id}:{amount or 0}"
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(payment_data)
        qr.make(fit=True)
    
        img = qr.make_image(fill_color="black", back_color="white")
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        return f"data:image/png;base64,{img_str}"

    def verify_payment(self):
        return random.choice([True, False])
    
    def check_expiry_time(self):
        current_time = datetime.now().timestamp()
        return current_time < self.__expiry_time
        
class Card:
    def __init__(self, card_id: str, card_number: str, card_holder: str, expiry_date, cvv: str):
        self.__card_id = card_id
        self.__card_number = card_number
        self.__card_holder = card_holder
        self.__expiry_date = expiry_date
        self.__cvv = cvv
     
    def validate_Card(self):
        if len(self.__card_number.replace(" ", "")) == 16 and len(self.__cvv) == 3:
            return True
        return False
    
    def charge_card(self, amount):
        return random.choice([True, False])
        
class Seat:
    def __init__(self, seat_id: str, row: str, number: int, type: str, price: float):
        self.__seat_id = seat_id
        self.__row = row
        self.__number = number
        self.__type = type
        self.__price = price
        
    @property
    def seat_id(self):
        return self.__seat_id
    
    @property
    def row(self):
        return self.__row
    
    @property
    def number(self):
        return self.__number
    
    @property
    def type(self):
        return self.__type
    
    @property
    def price(self):
        return self.__price

class SeatBooked(Seat):
    def __init__(self, seat_id: str, row: str, number: int, type: str, price: float, status: str, booking_id: str):
        super().__init__(seat_id, row, number, type, price)
        self.__status = status
        self.__booking_id = booking_id
        
    @property
    def status(self):
        return self.__status
    
    @status.setter
    def status(self, new_status):
        self.__status = new_status
    
    def update_status(self, booking_status):
        if booking_status == "success":
            self.__status = "unavailable"
            return "payment success"
        else:
            self.__status = "available"
            return "payment unsuccess"
    
    def reserve_seats(self): 
        self.__status = "reserved"
        return True

# Initialize the booking controller
booking_controller = BookingController()

app, rt = fast_app()

@rt("/")
def get():
    return Container(
        H1("CE Isan house - ระบบชำระเงิน"),
        P("กรุณาเลือกวิธีการชำระเงิน:"),
        Form(
            Div(
                Label(
                    Input(type="radio", name="paymentMethod", value="card", 
                          checked="checked", hx_get="/payment-form?method=card", 
                          hx_target="#payment-details", hx_swap="innerHTML"), 
                    "บัตรเครดิต/เดบิต"
                ),
                Label(
                    Input(type="radio", name="paymentMethod", value="qrcode", 
                          hx_get="/payment-form?method=qrcode", 
                          hx_target="#payment-details", hx_swap="innerHTML"), 
                    "QR Code"
                ),
            ),
            Div(id="payment-details"),
            hx_get="/payment-form?method=card", hx_trigger="load", hx_target="#payment-details",
            method="post",
            action="/submit"
        ),
        Hr(),
        P("Booking ID: BK123456", id="booking-info"),
        P("ราคารวม: 500 บาท", id="total-price")
    )

@rt("/payment-form")
def get(method: str):
    if method == "card":
        return Div(
            Label("ชื่อบนบัตร:", Input(type="text", name="card_holder", placeholder="กรุณาระบุชื่อบนบัตร")),
            Label("เลขบัตร:", Input(type="text", name="card_number", placeholder="xxxx-xxxx-xxxx-xxxx")),
            Label("รหัส CVV:", Input(type="text", name="cvv", placeholder="xxx")),
            Label("วันหมดอายุ:", Input(type="text", name="expiry", placeholder="MM/YYYY")),
            Button("ชำระเงิน", type="button", hx_post="/process-card-payment", hx_target="#payment-result"),
            Div(id="payment-result")
        )
    else:  # method == "qrcode"
        # สร้าง QR Code สำหรับการชำระเงิน
        booking_id =   # ในระบบจริงควรดึงจากการจองที่ถูกสร้างขึ้น
        payment_amount =  # ในระบบจริงควรดึงจากการจอง
        payment_data = f"CE_ISAN_PAYMENT:{booking_id}:{payment_amount}"
        qr_code = QrPayment(qr_code_id=booking_id, expiry_time=time.time() + 600)
        qr_code_img = qr_code.generate_qr_code(payment_data)
        
        
        return Div(
            P("สแกน QR Code เพื่อชำระเงิน:"),
            P(f"ยอดเงิน: {payment_amount} บาท"),
            Img(src=qr_code_img, alt="QR Code for payment", style="width:200px;height:200px;"),
            P("QR Code จะหมดอายุใน 10 นาที"),
            Button("ฉันได้ชำระเงินแล้ว", type="button", hx_post="/verify-qr-payment", hx_target="#payment-result"),
            Div(id="payment-result")
        )

@rt("/process-card-payment")
def post(card_holder: str = "", card_number: str = "", cvv: str = "", expiry: str = ""):
    # จำลองการประมวลผลการชำระเงินด้วยบัตร
    booking_id = "BK123456"  # ในระบบจริงควรดึงจากการจองที่ถูกสร้างขึ้น
    
    # สร้าง Card object
    card = Card(str(uuid.uuid4()), card_number, card_holder, expiry, cvv)
    
    # ดึง booking จาก controller
    booking = booking_controller.check_booking_id(booking_id)
    
    # ถ้าไม่มีการจองในระบบ ให้จำลองการสร้างขึ้นมาสำหรับการทดสอบ
    if booking == "Booking ID not found":
        # สร้างการจองใหม่
        booking = create_sample_booking()
    
    # สร้าง Payment object
    payment_id = f"PMT{uuid.uuid4().hex[:8].upper()}"
    payment = Payment(payment_id, booking, booking.total_price, "card")
    
    # ประมวลผลการชำระเงิน
    if card.validate_Card():
        # จำลองการเรียกเก็บเงิน
        if card.charge_card(payment.amount):
            booking.status = "Confirmed"
            payment.status = "Success"
            result = "success"
        else:
            payment.status = "Failed"
            result = "failed"
    else:
        payment.status = "Invalid Card"
        result = "invalid_card"
    
    # แสดงผลลัพธ์
    if result == "success":
        return Div(
            P("การชำระเงินสำเร็จ!", style="color:green;font-weight:bold;"),
            P(f"ขอบคุณ {card_holder} สำหรับการชำระเงิน"),
            P(f"หมายเลขการชำระเงิน: {payment_id}"),
            A("กลับสู่หน้าหลัก", href="/", style="color:blue;text-decoration:underline;")
        )
    elif result == "invalid_card":
        return Div(
            P("ข้อมูลบัตรไม่ถูกต้อง!", style="color:red;font-weight:bold;"),
            P("กรุณาตรวจสอบข้อมูลบัตรและลองใหม่อีกครั้ง"),
            Button("ลองอีกครั้ง", type="button", hx_get="/payment-form?method=card", hx_target="#payment-details")
        )
    else:
        return Div(
            P("การชำระเงินไม่สำเร็จ!", style="color:red;font-weight:bold;"),
            P("เกิดข้อผิดพลาดในการประมวลผลการชำระเงิน โปรดลองอีกครั้ง"),
            Button("ลองอีกครั้ง", type="button", hx_get="/payment-form?method=card", hx_target="#payment-details")
        )

@rt("/verify-qr-payment")
def post():
    # จำลองการตรวจสอบการชำระเงินผ่าน QR Code
    booking_id = "BK123456"  # ในระบบจริงควรดึงจากการจองที่ถูกสร้างขึ้น
    
    # สร้าง QR Payment object
    qr_expiry = datetime.now().timestamp() + 600  # หมดอายุใน 10 นาที
    qr_payment = QrPayment(str(uuid.uuid4()), qr_expiry)
    
    # ดึง booking จาก controller
    booking = booking_controller.check_booking_id(booking_id)
    
    # ถ้าไม่มีการจองในระบบ ให้จำลองการสร้างขึ้นมาสำหรับการทดสอบ
    if booking == "Booking ID not found":
        booking = create_sample_booking()
    
    # สร้าง Payment object
    payment_id = f"PMT{uuid.uuid4().hex[:8].upper()}"
    payment = Payment(payment_id, booking, booking.total_price, "qrcode")
    
    # จำลองการตรวจสอบการชำระเงิน
    payment_verified = qr_payment.verify_payment()
    
    if payment_verified:
        booking.status = "Confirmed"
        payment.status = "Success"
        result = "success"
    else:
        payment.status = "Failed"
        result = "failed"
    
    # แสดงผลลัพธ์
    if result == "success":
        return Div(
            P("การชำระเงินสำเร็จ!", style="color:green;font-weight:bold;"),
            P("ขอบคุณสำหรับการชำระเงินผ่าน QR Code"),
            P(f"หมายเลขการชำระเงิน: {payment_id}"),
            A("กลับสู่หน้าหลัก", href="/", style="color:blue;text-decoration:underline;")
        )
    else:
        return Div(
            P("ยังไม่พบการชำระเงิน!", style="color:red;font-weight:bold;"),
            P("ระบบยังไม่พบการชำระเงินของคุณ โปรดลองอีกครั้งหรือเลือกวิธีการชำระเงินอื่น"),
            Button("ตรวจสอบอีกครั้ง", type="button", hx_post="/verify-qr-payment", hx_target="#payment-result"),
            Button("เลือกวิธีการชำระเงินอื่น", type="button", hx_get="/", hx_target="body")
        )

serve()