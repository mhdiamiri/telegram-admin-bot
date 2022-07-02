from telegram import *
from telegram.ext import *
import time
from datetime import datetime
from exchanges.bitfinex import Bitfinex
import Joke, Quote, TextBio, Corona, HavaShenasi, TabirKhab, FalHafez, Currency, txtSender
import random


owner_id = 129182502
updater = Updater('EMPTY', use_context=True)
dispatcher : Dispatcher = updater.dispatcher

def sendTextMessage(text, chat_id):
    updater.bot.send_message(
        text = text,
        chat_id = chat_id,

    )

def remove_messages(update:Update, number):
    now = update.effective_message.message_id - 1
    chat_id = update.effective_chat.id
    i = 0
    while(i < number):
        try:
            updater.bot.delete_message(message_id = now,
                                        chat_id = chat_id)
            i += 1
        except:
            print('error!')
        now -= 1
    update.message.reply_text('%i messages Deleted successfully!'%(number))

def is_admin(update: Update):
    admins = update.effective_chat.get_administrators()
    user_id = update.effective_user.id
    for user in admins:
        if user.user.id == user_id:
            return True
    return False

def owner(update: Update, context: CallbackContext):
    text = update.effective_message.text
    chat_id = update.effective_chat.id

def show_settings(update: Update, query = None):
    keyboard = [
            [InlineKeyboardButton("Group Info", callback_data='gpinfo')],
            [InlineKeyboardButton("Support", callback_data='support')],
            [InlineKeyboardButton("Close", callback_data='delete')],

        ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    if query is None:
        update.message.reply_text('SETTINGS', reply_markup=reply_markup)
    else:
        query.edit_message_text('SETTINGS', reply_markup=reply_markup)

def text_admin(update: Update, context: CallbackContext):
    text = update.effective_message.text
    chat_id = update.effective_chat.id
    text = text.lower()
    if text == 'settings': show_settings(update)
    if text.startswith('delete:'): 
        number = int(text[7:])
        remove_messages(update, number)
    if update.effective_user.id == owner_id:
        owner(update, context)
    if text == 'price':
        stock_market(update)
    if text == 'error':
        try:
            txtSender.replyer(update)
        except:
            update.message.reply_text('Failed :(')

def text_member(update: Update):
    print("no")

def text_handler(update: Update, context: CallbackContext):
    text = update.effective_message.text 
    
    text = text.lower()
    
    if text.startswith('هواشناسی '): 
        update.message.reply_text(HavaShenasi.search_city(text[9:]))

    if text.startswith('تعبیر '): tabir_khab(update, text[7:])

    if text == 'prices':
        update.message.reply_text(Currency.all_coins())

    if text == 'bio':
        update.message.reply_text(TextBio.get_bio())

    if text.startswith('/tabir'): 
        tabir(update, int(text[6:]))

    elif text.__contains__('joke'): 
        update.message.reply_text(Joke.tell_joke())

    elif text.__contains__('quote'): 
        update.message.reply_text(Quote.get_Quote())
    
    if text == 'corona':
        update.message.reply_text(Corona.corona_iran())

    if text == 'me':
        string = ''
        user = update.effective_user.to_dict()
        for info in user:
            string += info + ': ' if info is not None else ''
            string += str(user[info]) + '\n' if user[info] is not None else 'Empty'
        if string == '':
            string = 'Nothing to show!'
        update.message.reply_text(string)
    
    if text == 'fal hafez': fal_hafez(update)

    if is_admin(update):
        text_admin(update, context)
    else:
        text_member(update)

def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    if update.effective_chat.type == 'supergroup' or update.effective_chat.type == 'group':
        if is_admin:
            gp_info = update.effective_chat.to_dict()
            string = ''
            for info in gp_info:
                string += str(info) + ': ' if info is not None else ''
                string += str(gp_info[info]) + '\n' if gp_info[info] is not None else 'Empty'
            if string == '':
                string = 'Nothing to show!'
            update.message.reply_text(string)
    else:
        sendTextMessage('Welcome', chat_id)

def buttons(update: Update, context: CallbackContext):
    query = update.callback_query
    if is_admin(update): 
        keyboard = [
            [InlineKeyboardButton("back", callback_data='backToSettings')],

        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        if query.data == 'delete':query.delete_message()
        if query.data == 'gpinfo':query.edit_message_text(update.effective_chat.to_dict(),
                                                             reply_markup=reply_markup)
        if query.data == 'support':query.edit_message_text('Support:'+
                                                            '\n@officialmehdiamiri'+
                                                            '\n@officialmehdiamiri_ch',
                                                             reply_markup=reply_markup)
        if query.data == 'backToSettings': show_settings(update, query)
        query.answer()
    else: query.answer('error')

def schedule_message(context: CallbackContext):
    chat_id = -1001283002376
    # now = datetime.now()
    # current_time = now.strftime("%H:%M:%S")
    job = context.job
    text = price = Bitfinex().get_current_price()
    #text = "it's %s and i still miss you :("%(current_time)
    context.bot.send_message(job.context,text = "1BTC = "+str(price)+'$' )
    context.job_queue.run_once(schedule_message, 10 ,chat_id, str(chat_id))

def stock_market(update: Update):
    price = Bitfinex().get_current_price()
    update.message.reply_text("1BTC = "+str(price)+'$')

def fal_hafez(update: Update):
    chat_id = update.effective_chat.id
    fal = FalHafez.random_fal()
    sendTextMessage('شعر:\n' + str(fal[1]), chat_id)
    sendTextMessage('فال:\n' + str(fal[2]), chat_id)

def tabir_khab(update: Update, keyword):
    keys = TabirKhab.search(keyword)
    text = ''
    for i in keys:
        text += '\n' + str(i[1]) + '\n'
        text += '/tabir'+str(i[0])
    if len(text) > 4096:
        for i in range(len(text) % 4096):
            step = i * 4096
            update.message.reply_text(text[step: step + 4096])
    else:
        try:
            update.message.reply_text(text)
        except:
            update.message.reply_text('error')

def tabir(update: Update, i):
    text = TabirKhab.re_content(i)
    text = text.replace('h4', 'b')
    text = text.replace('<p>', '\n')
    text = text.replace('</p>', '')
    try:
        update.message.reply_html(text)
    except:
        update.message.reply_text('error')
    
def main():
    dispatcher.add_handler(CommandHandler(('start'), start))
    dispatcher.add_handler(CallbackQueryHandler(buttons))
    dispatcher.add_handler(MessageHandler(Filters.text, text_handler))
    updater.start_polling()

if __name__ == '__main__':
    main()
