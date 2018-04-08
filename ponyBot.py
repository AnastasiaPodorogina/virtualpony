import telebot
from telebot import types
import JsonFromRequest as FUCK

TOKEN = ""
TXT_HELLO = "Привет! Я Пони - твой друг)\nСегодня я помогу тебе выбрать самые классные билеты, чтобы ты смог отправиться в путешествие ;)\n\n\nИз какого ты города?"
CHAT_ID = 187022130
tb = telebot.TeleBot(TOKEN)

user = tb.get_me()

answer_dict = {"origin": "", "destination": "", "d_date": "", "bort_feed": "", "hand_clad": "", "p_space": "",
               "entertain": "", "clean": "", "sells": "", "staff_work": ""}

count = 0


def deadline1(message, question, key):
    tb.reply_to(message, question, reply_markup=markup)
    answer_dict[key] = message.text
    print(answer_dict)


def deadline(message, question, key):
    tb.reply_to(message, question)
    answer_dict[key] = message.text
    print(answer_dict)


markup = types.ReplyKeyboardMarkup()
itembtna = types.KeyboardButton('10')
itembtnv = types.KeyboardButton('20')
itembtnc = types.KeyboardButton('30')
itembtnd = types.KeyboardButton('40')
itembtne = types.KeyboardButton('50')
itembtnaa = types.KeyboardButton('60')
itembtnvv = types.KeyboardButton('70')
itembtncc = types.KeyboardButton('80')
itembtndd = types.KeyboardButton('90')
itembtnee = types.KeyboardButton('100')
markup.row(itembtna, itembtnv, itembtnc, itembtnd, itembtne)
markup.row(itembtnaa, itembtnvv, itembtncc, itembtndd, itembtnee)


@tb.message_handler(commands=['start', 'help'])
def send_welcome(message):
    global count
    count = 0
    tb.reply_to(message, TXT_HELLO)
    count += 1


@tb.message_handler(func=lambda message: True)
def msg_hd(message):
    global count
    if count == 1:
        deadline(message, "Куда ты хочешь полететь?)", "origin")

    if count == 2:
        deadline(message, "Когда ты хочешь полететь в {}?)".format(message.text), "destination")

    if count == 3:
        deadline1(message, "На сколько вы любите вкусно поесть на борту?)", "d_date")

    if count == 4:
        deadline1(message, "Много ли вы планируете взять с собой в самолет?", "bort_feed")

    if count == 5:
        deadline1(message, "Насколько вы интроверт?", "hand_clad")

    if count == 6:
        deadline1(message, "Как вы относитесь к развлечениям на борту?", "p_space")

    if count == 7:
        deadline1(message, "На сколько вы брезгливый человек?", "entertain")

    if count == 8:
        deadline1(message, "Хотели бы вы что-нибудь купить во время полета?", "clean")

    if count == 9:
        deadline1(message, "На сколько вам важен сервис?", "sells")

    if count == 10:
        deadline1(message, "Спасибо за ответики ;)", "staff_work")
        tb.send_message(CHAT_ID, "Подождите, сейчас поняша подберет билетик...;)")
        max_tiket = FUCK.YOBANI_VROT(answer_dict)[0]
        for ticket in FUCK.YOBANI_VROT(answer_dict):
            if ticket.weight > max_tiket.weight:
                max_tiket = ticket

        msg = "Билет авиакомпании {}\nЦена:{}\nКоличество пересадок:{}\n".format(max_tiket.ticket_list()[1], max_tiket.ticket_list()[2], max_tiket.ticket_list()[3])
        tb.send_message(CHAT_ID, msg)
        tb.send_message(CHAT_ID, "Ваш билетик;)")

    count += 1


tb.polling(none_stop=False, interval=3, timeout=20)
