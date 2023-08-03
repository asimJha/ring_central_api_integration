import os
import sys
from dotenv import load_dotenv
from ringcentral import SDK

# Load environment variables from .env file
load_dotenv()

# Instantiate the RingCentral SDK
rcsdk = SDK(
    os.environ.get('RC_CLIENT_ID'),
    os.environ.get('RC_CLIENT_SECRET'),
    os.environ.get('RC_SERVER_URL')
)
platform = rcsdk.platform()

# Authenticate a user using username and password
def login():
    try:
        platform.login(jwt=os.environ.get('RC_JWT'))
        print("Authenticated successfully!")
    except Exception as e:
        print("An error occurred during authentication:", e)
        sys.exit("Unable to authenticate to the platform. Check credentials.")

# Send a text message
def send_sms(from_number, to_number, text):
    try:
        platform.post('/restapi/v1.0/account/~/extension/~/sms',
        {
            'from' : { 'phoneNumber': +19493540728 },
            'to'   : [ {'phoneNumber': +917319746966} ],
            'text' : 'Hello World from Python'
        })
        body_params = {
            'from': {'phoneNumber': from_number},
            'to': [{'phoneNumber': to_number}],
            'text': text
        }
        resp = platform.post('/restapi/v1.0/account/~/extension/~/sms', body_params)
        print("SMS sent successfully. Message ID:", resp.json().id)
    except Exception as e:
        print("An error occurred while sending the SMS:", e)

# Receive messages
def receive_sms():
    try:
        resp = platform.get('/restapi/v1.0/account/~/extension/~/message-store')
        messages = resp.json().records
        for message in messages:
            print("Message ID:", message.id)
            print("From:", message.from_.phoneNumber)
            print("To:", message.to[0].phoneNumber)
            print("Text:", message.subject)
            print("------------")
    except Exception as e:
        print("An error occurred while fetching messages:", e)

if __name__ == "__main__":
    login()

    # Example: Sending an SMS
    send_sms('+19493540728', '+917319746966', 'Hello, this is a test message!')

    # Example: Receiving messages
    receive_sms()
