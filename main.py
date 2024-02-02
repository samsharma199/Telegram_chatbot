import telegram.ext
from dotenv import load_dotenv

import os

load_dotenv()
TOKEN = os.getenv('TOKEN')


def start(update, context):
    update.message.reply_text("Welcome to my bot ")


def helps(update, context):
    update.message.reply_text(
        """
        Hi there I'm Telegram bot created by Sameer. Please follow there command:-
        
        /start - to start the conversation
        /content - Information about create
        /contact - Information about how to connect
        /help - to get this help menu
        
        I Hope this helps :)
        """
    )


def content(update, context):
    update.message.reply_text(
        """
        Our bot provides a subscription-based service for delivering daily news updates. Users can subscribe to different categories of news, manage their subscriptions, and receive daily news summaries
        """
    )


def contact(update, context):
    contact_info = """
    Contact Us:
    - Email: support@example.com
    - Twitter: @example_twitter
    - Website: https://example.com
    """
    update.message.reply_text(contact_info)

updater = telegram.ext.Updater(TOKEN, use_context=True)
dispatch = updater.dispatcher

dispatch.add_handler(telegram.ext.CommandHandler("start", start))
dispatch.add_handler(telegram.ext.CommandHandler("help", helps))
dispatch.add_handler(telegram.ext.CommandHandler("content", content))
dispatch.add_handler(telegram.ext.CommandHandler("contact", contact))

updater.start_polling()
updater.idle()
