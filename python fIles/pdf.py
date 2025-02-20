from fpdf import FPDF
import mysql.connector

# Database Configuration
db_host = 'localhost'
db_user = 'root'
db_password = 'gaju1234?'
db_name = 'data'

def get_db_connection():
    return mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )

def hi(order_id):
    class PDFInvoice(FPDF):
        def header(self):
            self.set_font('Arial', 'B', 16)  # Use default core font
            self.cell(0, 10, 'Order Confirmation', align='C', ln=1)

        def footer(self):
            self.set_y(-15)
            self.set_font('Arial', 'I', 10)  # Use default core font
            self.cell(0, 10, 'Thank you for shopping with us!', align='C')

    # Create instance of FPDF
    pdf = PDFInvoice()
    # Add a page
    pdf.add_page()

    # Set font
    pdf.set_font('Arial', '', 12)

    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT id, item_name, price_per_day, payment_method, address
            FROM online
            WHERE id = %s
        """, (order_id,))

        last_order = cursor.fetchone()

        if last_order:
            order_details = [
                ("Order Id", str(last_order[0])),
                ("Item Name", last_order[1]),
                ("Total Amount", f"${last_order[2]:.2f}"),
                ("Payment Method", last_order[3]),
                ("Address", last_order[4]),
            ]

            pdf.set_font('Arial', 'B', 12)
            pdf.multi_cell(0, 5, " Oredr Description.")
            pdf.ln(10)
            # Table headers for order details
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(95, 10, 'Description', border=1, align='C')
            pdf.cell(95, 10, 'Details', border=1, align='C')
            pdf.ln()

            # Table content for order details
            pdf.set_font('Arial', '', 12)
            for key, value in order_details:
                pdf.cell(95, 10, key, border=1)
                pdf.cell(95, 10, str(value), border=1)
                pdf.ln()

        else:
            pdf.multi_cell(0, 10, "No order details found for this user.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        conn.close()

    pdf.ln(10)
    pdf.multi_cell(0, 10, """If you have any questions or need help, you can reply to this email or reach out to our customer support.
    Happy shopping!""")

    # Save the PDF
    file_name = f"invoice.pdf"
    pdf.output(file_name)

    # print(f"PDF Invoice for Order ID {order_id} generated successfully!")
    return file_name


# Example usage: call the function with an order_id
# Replace with the actual order_id to generate the invoice
# hi(1)
