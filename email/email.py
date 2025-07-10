import smtplib
import pandas as pd
import json
import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader
import yagmail

# --- Configuration ---
EMAIL_ADDRESS = 'domainlookup01@gmail.com'
OAUTH_FILE = 'yagmail.json'  # created by yagmail.register(...)
SUBJECT_TEMPLATE = "Featured Property: {title}"

# --- Property Data ---
property_data = {
    'image_url': 'https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=600&q=80',
    'property_title': 'Charming 3 Bedroom Family Home',
    'property_location': '123 Main St, Pleasantville',
    'property_price': '$399,000',
    'bedrooms': 3,
    'bathrooms': 2,
    'property_area': 1800,
    'property_description': (
        'This beautifully renovated home features an open floor plan, modern kitchen, '
        'and a spacious backyard—perfect for family living.<br><br>'
        'Schedule a visit today!'
    ),
    'listing_url': 'https://your-site.com/listings/123-main-st'
}

# --- Sanitize <br> tags ---
def sanitize_html(value):
    return re.sub(r'<\s*br\s*/?\s*>', '\n', value, flags=re.IGNORECASE)

property_data['property_description'] = sanitize_html(property_data['property_description'])

# --- Jinja2 Setup ---
env = Environment(
    loader=FileSystemLoader('.'),
    variable_start_string='<<',
    variable_end_string='>>'
)
template = env.get_template('real_estate_template.html')

# --- Load recipients.csv ---
recipients = pd.read_csv('recipients.csv')  # columns: email,name

# --- Step 1: Login with yagmail (OAuth2) ---
print("🔐 Authenticating with yagmail...")
yagmail.SMTP(EMAIL_ADDRESS, oauth2_file=OAUTH_FILE)

# --- Step 2: Load access token manually from yagmail.json ---
with open(OAUTH_FILE, 'r') as f:
    token_data = json.load(f)
    access_token = token_data['token']
    if not access_token:
        raise Exception("❌ No access token found in yagmail.json")

# --- Step 3: Prepare XOAUTH2 string ---
def generate_oauth2_string(email, access_token):
    return f"user={email}\1auth=Bearer {access_token}\1\1".encode("utf-8")

xoauth2_string = generate_oauth2_string(EMAIL_ADDRESS, access_token)

# --- Step 4: Connect to Gmail SMTP with OAuth2 ---
print("📡 Connecting to smtp.gmail.com ...")
smtp = smtplib.SMTP('smtp.gmail.com', 587)
smtp.set_debuglevel(1)
smtp.ehlo()
smtp.starttls()
smtp.ehlo()

# --- Step 5: Authenticate with XOAUTH2 ---
print("🔑 Authenticating with XOAUTH2 ...")
code, response = smtp.docmd('AUTH', 'XOAUTH2 ' + xoauth2_string.decode())
if code != 235:
    raise Exception(f"❌ AUTH FAILED: {code} {response}")

# --- Step 6: Send personalized HTML email to each recipient ---
for _, row in recipients.iterrows():
    to_email = row['email']
    name = row.get('name', 'Friend')
    print(f"\n📤 Sending email to {to_email}...")

    values = {'name': name}
    values.update(property_data)
    html_body = template.render(**values)

    # Build MIME email
    msg = MIMEMultipart('alternative')
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_email
    msg['Subject'] = SUBJECT_TEMPLATE.format(title=property_data['property_title'])
    msg.attach(MIMEText(html_body, 'html'))

    # Optional: Save for debug
    debug_filename = f"email_to_{to_email.split('@')[0]}.html"
    with open(debug_filename, "w", encoding="utf-8") as f:
        f.write(html_body)

    # Send the email
    try:
        smtp.sendmail(EMAIL_ADDRESS, to_email, msg.as_string())
        print(f"✅ Email sent to {to_email}")
    except Exception as e:
        print(f"❌ Failed to send to {to_email}: {e}")

# --- Step 7: Close SMTP session ---
smtp.quit()
print("\n📧 All done.")