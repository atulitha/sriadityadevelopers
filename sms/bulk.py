from twilio.rest import Client

account_sid = ''
auth_token = ''
client = Client(account_sid, auth_token)

guru_purnima_message = str(
    "Wishing you a very Happy Guru Purnima!\n"
    "Today is a special day to express gratitude to those who guide, inspire, and uplift us.\n"
    "Your mentorship has made a meaningful difference in my journey.\n"
    "From your valuable insights to your constant support and encouragement,\n"
    "Thank you for being a true mentor in every sense."
)

message = client.messages.create(
    from_='+17633733208',
    body=guru_purnima_message,
    to='+919912555505'
)
print(guru_purnima_message, type(guru_purnima_message))
print(message.sid)