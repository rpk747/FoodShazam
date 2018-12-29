import logging
import datetime
import requests
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from Model import FS_model

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def start(bot, update):
    now = datetime.datetime.now()
    today = now.day
    hour = now.hour

    if today == now.day and 0 <= hour < 12:
        bot.send_message(update.message.chat_id,
                         'Good Morning {}! Welcome to Food Shazam, your cooking assistant'.format(
                             update.message.chat.first_name))
        bot.send_message(update.message.chat_id, 'Hope you are doing great this morning :)')


    elif today == now.day and 12 <= hour < 17:
        bot.send_message(update.message.chat_id,
                         'Good Afternoon {}! Welcome to Food Shazam, your cooking assistant'.format(
                             update.message.chat.first_name))
        bot.send_message(update.message.chat_id, 'Hope you are doing great this afternoon :)')


    elif today == now.day and 17 <= hour < 23:
        bot.send_message(update.message.chat_id,
                         'Good Evening {}! Welcome to Food Shazam, your cooking assistant'.format(
                             update.message.chat.first_name))
        bot.send_message(update.message.chat_id, 'Hope you are doing great this evening :)')

    bot.send_message(chat_id=update.message.chat_id, text='Please type the list of ingredients available with you (separated by comma)')
    bot.send_message(chat_id=update.message.chat_id, text='For example: Ginger, garlic, onion')


# def echo(bot, update):
#   splitText=update.message.text.split(', ',len(update.message.text))
#   print(splitText)
#  bot.send_message(chat_id=update.message.chat_id, text=splitText)

splitText = None
def echo(bot, update):
    global splitText
    splitText = update.message.text.split(', ', len(update.message.text))
    print(splitText)

    bot.send_message(chat_id=update.message.chat_id, text="The ingredients entered are: ")
    bot.send_message(chat_id=update.message.chat_id, text=splitText)

    keyboard = [[InlineKeyboardButton("Appetizer", callback_data='Appetizers'),
                 InlineKeyboardButton("Main Course", callback_data='Main Dishes')],
                [InlineKeyboardButton("Dessert", callback_data='Desserts')]]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please select your preference:', reply_markup=reply_markup)


def button(bot, update):
    query = update.callback_query
    bot.send_message(text="Processing...Will be right back!", chat_id=query.message.chat_id,
                     message_id=query.message.message_id)
    if query.data == 'Appetizers':
        result = FS_model('Appetizers',splitText)
        print("Result :",result)
        bot.send_message(text="Selected option: {}".format(query.data),  # "Selected option: {}".format(query.data)
                         chat_id=query.message.chat_id,
                         message_id=query.message.message_id)
    elif query.data == 'Main Dishes':
        result = FS_model('Main Dishes', splitText)
        print("Result :", result)
        bot.send_message(text="Selected option: {}".format(query.data),  # "Selected option: {}".format(query.data)
                         chat_id=query.message.chat_id,
                         message_id=query.message.message_id)

    elif query.data == 'Desserts':
        result = FS_model('Desserts', splitText)
        bot.send_message(text="Selected option: {}".format(query.data),  # "Selected option: {}".format(query.data)
                         chat_id=query.message.chat_id,
                         message_id=query.message.message_id)
    else:
        bot.send_message(text="Sorry,please select one option", chat_id=query.message.chat_id,
                         message_id=query.message.message_id)

    if result:
        bot.send_message(text="You can cook - {}".format(result[1]),  # "Selected option: {}".format(query.data)
                         chat_id=query.message.chat_id,
                         message_id=query.message.message_id)
        bot.send_message(text="Total Ingredients needed are- {}".format(result[2]),  # "Selected option: {}".format(query.data)
                         chat_id=query.message.chat_id,
                         message_id=query.message.message_id)
        bot.send_message(text="For complete recipe- https://www.yummly.com/recipe/{}".format(result[0]),  # "Selected option: {}".format(query.data)
                         chat_id=query.message.chat_id,
                         message_id=query.message.message_id)


def help(bot, update):
    update.message.reply_text("Use /start to test this bot.")


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)


class BotHandler:

    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)

    def get_updates(self, offset=None, timeout=100):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        # print(resp.json());
        result_json = resp.json()['result']
        # print(result_json);
        return result_json

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    def get_last_update(self):
        get_result = self.get_updates()

        if len(get_result) > 0:
            last_update = get_result[-1]
        else:
            last_update = get_result[len(get_result)]

        # print(last_update);
        return last_update


def main():
    # Create the Updater and pass it your bot's token.

    updater = Updater(' botToken')  # bot token here
    dispatcher = updater.dispatcher

    dispatcher.add_handler(MessageHandler(Filters.text, echo))
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CallbackQueryHandler(button))
    dispatcher.add_handler(CommandHandler('help', help))
    updater.dispatcher.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()
