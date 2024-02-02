from flask import Flask, request, redirect
from google.oauth2 import service_account
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from datetime import datetime, timedelta
import requests

app = Flask(__name__)

GOOGLE_AUTH_SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

botToken = '<your_bot_token>'
sheetId = '<your_sheet_id>'
insiderChatId = '<your_insider_chat_id>'

creds = None


def get_sheet_token():
    global creds
    if creds is None or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            creds = service_account.Credentials.from_service_account_file(
                '<path_to_service_account_json>',
                scopes=GOOGLE_AUTH_SCOPES
            )
    return creds.token


def api_call(method, payload):
    """
    Make an API call to the Telegram Bot API.

    Parameters:
    - method: The Telegram Bot API method (e.g., 'sendMessage').
    - payload: The payload to be sent in the API call.

    Returns:
    - The response from the Telegram Bot API.
    """
    bot_url = f'https://api.telegram.org/bot{botToken}/{method}'
    response = requests.post(bot_url, json=payload)

    if not response.ok:
        raise Exception(f"Telegram API call failed. Response: {response.text}")

    return response.json()


def update_subscription_status(email, is_subscribed):
    """
    Update the subscription status in Google Sheets (placeholder).

    Parameters:
    - email: The user's email.
    - is_subscribed: Boolean indicating whether the user is subscribed or not.

    Returns:
    - None
    """
    # Placeholder for updating the subscription status in Google Sheets
    # Replace with actual Google Sheets API code
    sheet_service = build('sheets', 'v4', credentials=get_sheet_token())
    # Implement your logic to update the sheet based on the email and is_subscribed status


def get_subscription_expiration(email):
    """
    Get the subscription expiration date from Google Sheets (placeholder).

    Parameters:
    - email: The user's email.

    Returns:
    - A datetime object representing the subscription expiration date.
    """
    # Placeholder for getting subscription expiration date from Google Sheets
    # Replace with actual Google Sheets API code
    sheet_service = build('sheets', 'v4', credentials=get_sheet_token())
    # Implement your logic to retrieve the expiration date based on the email


def send_subscription_reminder(chat_id, days_until_expiration):
    """
    Send a subscription reminder to the user via Telegram.

    Parameters:
    - chat_id: The Telegram chat ID of the user.
    - days_until_expiration: The number of days until the subscription expires.

    Returns:
    - None
    """
    reminder_text = f"Your subscription will expire in {days_until_expiration} days. Renew now!"
    api_call('sendMessage', {'chat_id': chat_id, 'text': reminder_text})

def get_or_generate_invite_link():
    # Replace with your actual logic to fetch or generate an invite link
    return '<your_generated_or_fetched_invite_link>'


def kick_user_from_chat(user_id):
    # Replace with your actual logic to kick a user from the chat
    pass


def get_emails_from_sheets():
    # Replace with your actual logic to fetch emails from Google Sheets
    return ['email1@example.com', 'email2@example.com', 'email3@example.com']



@app.route('/register')
def register():
    email = request.args.get('email', '')
    email_code = email.encode('ascii').decode('base64')
    me = api_call('getMe', {})

    # Assume the user is subscribing when registering
    update_subscription_status(email, True)

    # Get the subscription expiration date
    expiration_date = get_subscription_expiration(email)
    days_until_expiration = (expiration_date - datetime.now()).days

    # Send a welcome message with an invite link and subscription information
    reply_markup = get_invite_reply_markup()
    text = f"Welcome! You're subscribed until {expiration_date.strftime('%Y-%m-%d')}."
    api_call('sendMessage', {'chat_id': me['id'], 'text': text, 'reply_markup': reply_markup})

    # Send a reminder message to the user
    send_subscription_reminder(me['id'], days_until_expiration)

    return redirect(f'https://telegram.me/{me["username"]}?start={email_code}')


@app.route('/bot', methods=['POST'])
def bot():
    update = request.json
    if 'message' in update:
        message = update['message']
        if 'text' in message and message['chat']['type'] == 'private' and message['text'].startswith('/start'):
            new_user(message)
        elif message['chat']['id'] == insiderChatId and 'new_chat_members' in message:
            verify_members(message)
    return '', 200


def new_user(message):
    chat_id = message['chat']['id']
    email = message['text'].split('/start')[-1].strip()

    # Check if the user is already subscribed
    if get_subscription_expiration(email) is not None:
        api_call('sendMessage', {'chat_id': chat_id, 'text': "You're already subscribed!"})
        return

    # Subscribe the user
    update_subscription_status(email, True)

    # Send a confirmation message
    api_call('sendMessage', {'chat_id': chat_id, 'text': "Subscription confirmed!"})


def verify_members(message):
    if 'new_chat_members' in message:
        new_members = message['new_chat_members']
        emails = get_emails_from_sheets()

        for new_member in new_members:
            if 'id' in new_member and 'first_name' in new_member:
                verify_member(emails, new_member)


def verify_member(emails, new_member):
    user_id = new_member['id']
    email = new_member.get('username', '')

    if email in emails:
        # User is verified, proceed with any additional logic
        pass
    else:
        # User is not verified, kick from the chat
        kick_user_from_chat(user_id)


def get_invite_reply_markup():
    # Implement the equivalent logic in Python for getting invite reply markup
    pass


@app.route('/cancel_subscription', methods=['POST'])
def cancel_subscription():
    email = request.json.get('email', '')

    # Unsubscribe the user
    update_subscription_status(email, False)

    # Send a confirmation message
    api_call('sendMessage', {'chat_id': insiderChatId, 'text': f"Subscription for {email} canceled."})

    return '', 200


if __name__ == '__main__':
    app.run(debug=True)
