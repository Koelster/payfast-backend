from flask import Flask, request
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

@app.route('/ipn_handler.php', methods=['POST'])
def ipn_handler():
    data = request.form.to_dict()

    # Extract info
    email = data.get('custom_str1')
    item_name = data.get('item_name')
    amount = data.get('amount_gross')

    # Prepare email
    subject = "Your Download from MyDigitalStore"
    body = f"""Hi there,\n\nThank you for your purchase of '{item_name}' for R{amount}.\n\nYour file is ready to download:\nhttps://mydigitalstore.co.za/downloads/{item_name}.zip\n\nRegards,\nMyDigitalStore"""

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = "info@mydigitalstore.co.za"
    msg['To'] = email

    try:
        with smtplib.SMTP("s33.registerdomain.net.za", 587) as server:
            server.starttls()
            server.login("info@mydigitalstore.co.za", "YOUR_PASSWORD")
            server.send_message(msg)
        return "✅ Email sent", 200
    except Exception as e:
        return f"❌ Failed to send email: {e}", 500
