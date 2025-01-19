
from flask import Flask, render_template, request, redirect, session, flash
from flask_mail import Mail, Message
import mysql.connector

app = Flask(__name__)

# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# Configuring Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'gajanan19022000@gmail.com'  # Your Gmail address
app.config['MAIL_PASSWORD'] = 'jost higa wtmc wzlr'  # Your App Password
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)
# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

 # Setting up SQL database URI
db_host='localhost'
db_user='root'
db_password='gaju1234?'
db_name='data'

# Function to connect to the MySQL database
def get_db_connection():
    conn = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )
    return conn

# Create the database table if it doesn't exist

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
            price_per_day int,
            item_name VARCHAR(100),
            payment_method VARCHAR(20)
        );
    ''')

    conn.commit()
    conn.close()


# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

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



# ////////////////////////////////////////////////////////////////////////////////////

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

# /////////////////////////////////////////////////////
@app.route('/place_order', methods=["POST"])
def place_order():
    # Fetch data from the form
    name = request.form['name']
    number = request.form['number']
    email = request.form['email']
    address = request.form['address']
    payment_method = request.form['payment_method']
    item_name = request.form['item_name']  # Now populated with item name
    price_per_day = request.form['price_per_day']  # Now populated with price per day

    # You can now process the order as before
    # Connect to the database and insert the order details
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO online (name, number, email, address, price_per_day, item_name, payment_method)
                       VALUES (%s, %s, %s, %s, %s, %s, %s)''', 
                   (name, number, email, address, price_per_day, item_name, payment_method))
    conn.commit()
    conn.close()

    # Send email confirmation and return to home
    subject = "Order Confirmation"
    message_body = f"""Hello {name},
    ORDER SUCCESSFUL

    Thank you for your order!
    Here’s a summary of your order:
    - Item Name: {item_name}
    - Price per Day: ${price_per_day}
    - Payment Method: {payment_method}
    - Shipping Address: {address}
    
    If you have any questions, feel free to contact us.
    
    Happy shopping! 😊😊
    """
    msg = Message(subject=subject, sender=app.config['MAIL_USERNAME'], recipients=[email])
    msg.body = message_body
    mail.send(msg)

    return redirect('/')
# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

if __name__ == '__main__':
    create_table()
    app.run(debug=True)








