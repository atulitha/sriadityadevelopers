import csv
import os
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader, select_autoescape

# Load environment variables
load_dotenv()
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 465))

# Property Data
property_data = {
    'image_url': 'https://jntukelearn.in/sriaditya/image.jpg',
    'property_title': 'Nanda Gokulam',
    'property_location': 'Sarpavaram junction, Kakinada',
    'property_price': 'Affordable price starting at ₹50 Lakhs',
    'Villas': "luxury gated community with modern amenities",
    'Apartments': "flats designed for comfort and style",
    'property_area': 1800,
    'property_description': (
        'luxury gated community with modern amenities, villas designed for comfort and style, flats with spacious interiors, '
        'and a spacious backyard—perfect for family living.\n\nSchedule a visit today!'
    ),
    'listing_url': 'https://your-site.com/listings/123-main-st'
}

# Setup Jinja2 Environment
env = Environment(
    loader=FileSystemLoader("templates"),
    autoescape=select_autoescape(["html", "xml"])
)

# Load Template
try:
    template = env.get_template("real_estate_template.html")
except Exception as e:
    print(f"❌ Error loading template: {e}")
    exit(1)

# Send individual email
def send_email(name, email):
    print(f"📤 Sending email to {name} <{email}>...")

    values = {"name": name}
    values.update(property_data)

    html_content = template.render(**values)
    plain_text = f"""
Hello {name},

Check out this amazing property: {property_data['property_title']}

Location: {property_data['property_location']}
Price: {property_data['property_price']}

Listing: {property_data['listing_url']}
"""

    message = MIMEMultipart("alternative")
    message["Subject"] = f"Featured Property: {property_data['property_title']}"
    message["From"] = EMAIL_ADDRESS
    message["To"] = email

    message.attach(MIMEText(plain_text, "plain"))
    message.attach(MIMEText(html_content, "html"))

    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, email, message.as_string())
        print("✅ Email sent successfully.")
    except Exception as e:
        print(f"❌ Failed to send email to {email}: {e}")

# Read recipients and send
def send_bulk_emails(csv_file):
    try:
        with open(csv_file, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                name = row.get("name")
                email = row.get("email")
                if name and email:
                    send_email(name, email)
                else:
                    print(f"⚠️ Skipping invalid row: {row}")
    except Exception as e:
        print(f"❌ Error reading recipients: {e}")

if __name__ == "__main__":
    print("🚀 Starting real estate email campaign...")
    send_bulk_emails("recipients.csv")
    print("🏁 Campaign finished.")