from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask_mail import Mail, Message
import mysql.connector
import stripe
from pdf import hi

app = Flask(__name__)
app.secret_key = "your_secure_key_here"  # Ensure this is set

# Stripe API Key
stripe.api_key = "sk_test_51QreFNJRU2FVlSQlyKuQG297bHhNDfspewEbo0p7KQJ3ehfEfK1mMsh05MfokPtl0wPSznQ5ecFrIti7pEou5XjQ00vLewlHRG"

# Flask-Mail Configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'gajanan19022000@gmail.com'
app.config['MAIL_PASSWORD'] = 'jost higa wtmc wzlr'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

# Database Configuration
db_host = 'localhost'
db_user = 'root'
db_password = 'gaju1234?'
db_name = 'data'

# Connect to MySQL
def get_db_connection():
    conn = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )
    return conn

# Create 'online' Table If Not Exists
def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS online (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            number VARCHAR(20),
            email VARCHAR(100),
            address TEXT,
            price_per_day INT,
            item_name VARCHAR(100),
            payment_method VARCHAR(20)
        );
    ''')
    conn.commit()
    conn.close()
# //////////////////////////////////////////////////////////////////////////////
@app.route('/')
def home():
    return render_template("index.html")

@app.route('/about')
def about():
        return render_template("about.html")

@app.route('/shop')
def shop():
        return render_template("shop.html")

@app.route('/blog')
def blog():
        return render_template("blog.html")

# //////////////////////////////////////////////////////////////////////////////////////////

@app.route('/place_order', methods=["POST"])
def place_order():
    name = request.form['name']
    number = request.form['number']
    email = request.form['email']
    address = request.form['address']
    payment_method = request.form['payment_method']
    item_name = request.form['item_name']
    price_per_day = float(request.form['price_per_day'])

    if payment_method == "Cards":
        session['order_data'] = {
            "name": name,
            "number": number,
            "email": email,
            "address": address,
            "price_per_day": price_per_day,
            "item_name": item_name,
            "payment_method": payment_method
        }
        return redirect(url_for('stripe_payment'))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO online (name, number, email, address, price_per_day, item_name, payment_method)
                      VALUES (%s, %s, %s, %s, %s, %s, %s)''', 
                   (name, number, email, address, int(price_per_day), item_name, payment_method))
    conn.commit()
    conn.close()

    send_order_confirmation_email(name, email, item_name, price_per_day)
    return """
    <script>
        alert("Order Successful! Your order has been placed. Check your email for details.");
        window.location.href = "/";
    </script>
    """
@app.route('/stripe_payment')
def stripe_payment():
    order_data = session.get('order_data')
    if not order_data:
        return """
    <script>
        alert("Order Successful! Your order has been placed. Check your email for details.");
        window.location.href = "/";
    </script>
    """
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'inr',
                'product_data': {'name': order_data["item_name"]},
                'unit_amount': int(order_data["price_per_day"] * 100),  # Convert to cents
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=url_for('payment_success', _external=True),
        cancel_url=url_for('payment_cancel', _external=True),
    )
    return redirect(checkout_session.url)

@app.route('/payment_success')
def payment_success():
    order_data = session.pop('order_data', None)
    if not order_data:
        return redirect('/')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO online (name, number, email, address, price_per_day, item_name, payment_method)
                      VALUES (%s, %s, %s, %s, %s, %s, %s)''', 
                   (order_data["name"], order_data["number"], order_data["email"], order_data["address"], 
                    int(order_data["price_per_day"]), order_data["item_name"], "Online Payment"))
    conn.commit()
    conn.close()

    send_order_confirmation_email(order_data["name"], order_data["email"], order_data["item_name"], order_data["price_per_day"])
    return """
    <script>
        alert("Order Successful! Your order has been placed. Check your email for details.");
        window.location.href = "/";
    </script>
    """
@app.route('/payment_cancel')
def payment_cancel():
    return """
    <script>
        alert("Payment Cancelled. Please try again.");
        window.location.href = "/";
    </script>
    """
# //////////////////////////////////////////////////////////////////////////////////

def send_order_confirmation_email(name, email, item_name, price_per_day):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id FROM online ORDER BY id DESC LIMIT 1
    """)
    last_order = cursor.fetchone()
    conn.close()

    if last_order:
        pdf_file = hi(last_order[0])  # Generate PDF invoice
    
        subject = "Order Confirmation"
        message_body = f"""Hello {name},

        ORDER SUCCESSFUL

        Thank you for your order! Your order is being processed and will be on its way to you soon.

        If you have any questions, reply to this email.
        
        Happy shopping! 😊😊
        """
        with open(pdf_file, "rb") as attachment:
            pdf_content = attachment.read()

        msg = Message(subject=subject, sender=app.config['MAIL_USERNAME'], recipients=[email])
        msg.body = message_body
        msg.attach(filename="order_invoice.pdf", content_type="application/pdf", data=pdf_content)
        mail.send(msg)


# //////////////////////////////////////////////////////////////////////////////////////////
@app.route('/send_contact', methods=["POST"])
def send_email():
    name = request.form['name']
    email = request.form['email']
    subject = request.form['subject']
    message = request.form['message']
    phone = request.form['phone']
    # Create email message
    msg = Message(subject=f"New Contact Messge from {name}: {subject}",  # Include name in subject
                  sender=app.config['MAIL_USERNAME'],             # Must be your verified sender email
                  recipients=['gajanan19022000@gmail.com'])        # Use your email as recipient
                  
    # Include user details in the body of the email
    msg.body = f"Message from :- {name}\n\n Email:-{email}\n\Requirment:-{subject}\n\nmessage:-{message}\n\nNumber:-{phone}"

    # Optionally set the reply-to header to the user's email
    msg.reply_to = email

    mail.send(msg)
    return redirect('/')
# //////////////////////////////////////////////////////////////////


if __name__ == '__main__':
    create_table()
    app.run(debug=True)
