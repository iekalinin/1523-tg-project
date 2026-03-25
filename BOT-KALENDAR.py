import random
import sqlite3
import telebot
# from telebot import types
from telebot.types import BotCommand
from holidays import HOLIDAYS

# Проверка даты
def check_data(d: str) -> bool:
    try:
        a, b = map(int, d.split('.'))
        pr2 = False
        if 1 <= a <= 31 and 1 <= b <= 12:
            if a <= PROVERKA[b - 1][0]:
                pr2 = True
        if pr2:
            return True
        else:
            return False
    except ValueError:
        return False


token = '8544639239:AAGRdsxPMreMdaPRqB6_R9r83E36fYrjU1Y'
bot = telebot.TeleBot(token)
# В HOLIDAYS лежат праздники, сам кортеж находится в файле holidays.py
# PROVERKA: в ней лежат кол-во дней в месяцаx, чтобы не было ошибок, а также название месяца



PROVERKA = (
    (31, 'Января'),  # 1
    (29, 'Февраля'),  # 2
    (31, 'Марта'),  # 3
    (30, 'Апреля'),  # 4
    (31, "Мая"),  # 5
    (30, 'Июня'),  # 6
    (31, 'Июля'),  # 7
    (31, 'Августа'),  # 8
    (30, 'Сентебря'),  # 9
    (31, 'Октября'),  # 10
    (30, 'Ноября'),  # 11
    (31, 'Декабря')  # 12
)

# создание файла
con = sqlite3.connect('holidays.db', check_same_thread=False)
cur = con.cursor()

# создание таблицы
cur.execute('''
    CREATE TABLE IF NOT EXISTS holidays(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        days INTEGER,
        months INTEGER,
        names TEXT
    )
''')

# заполнение таблицы
for day, month, name in HOLIDAYS:
    cur.execute('''INSERT INTO holidays(days, months, names) VALUES(?, ?, ?)''', (day, month, name))

# установление команд в боте
commands = [
    BotCommand("info", "Информация о боте"),
    BotCommand("data", "Ввести свою дату"),
    BotCommand('random', 'Получить случайный праздник'),
    BotCommand('add', 'Добавить праздник'),
    BotCommand('congratulation', 'Сделать поздравление')
]
bot.set_my_commands(commands)


# Команда старт
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет, я бот который поможет тебе узнать когда какие праздники ✌️ ")

# Команда инфо
@bot.message_handler(commands=['info'])
def info(message):
    bot.send_message(message.chat.id, "Привет, я бот который поможет тебе узнать когда какие праздники ✌️ ")

# Поиск праздника по дате
@bot.message_handler(commands=['data'])
def data_z(message):
    msg = bot.send_message(message.chat.id, 'Введи дату в формате ДД.ММ')
    bot.register_next_step_handler(msg, get_hol)

# проверка и получение даты и вывод праздника
def get_hol(message):
    inp = message.text
    pr = check_data(inp)
    if not pr:
        msg = bot.send_message(message.chat.id, 'Дата некорректна❌. Введи новую дату в формате ДД.ММ')
        bot.register_next_step_handler(msg, get_hol)
    else:
        f, e = inp.split('.')
        cur.execute('''SELECT names FROM holidays WHERE days = ? AND months = ?''', (f, e))
        ans = cur.fetchall()
        for i in ans:
            bot.send_message(message.chat.id, f'В этот день отмечается {i[0]}🎉!')

# вывод случайного праздника
@bot.message_handler(commands=['random'])
def random_data(message):
    z = random.randint(1, 12)
    g = PROVERKA[z - 1][0]
    x = random.randint(1, g)
    cur.execute('''SELECT names FROM holidays WHERE days = ? AND months = ?''', (x, z))
    ans = cur.fetchall()
    bot.send_message(message.chat.id, f'{ans[0][0]}, Отмечается {x} {PROVERKA[z - 1][1]}🎉!')

# Ввод команда add и ее запуск
@bot.message_handler(commands=['add'])
def zapusk(message):
    msg = bot.send_message(message.chat.id, 'Введи дату через в формате ДД.ММ и названия праздника')
    bot.register_next_step_handler(msg, add)
# Добавление праздника
def add(message):
    #bot.send_message(message.chat.id, f'Введи дату через в формате ДД.ММ и праздник')
    inp = message.text
    l = inp.split()
    pr = check_data(l[0])
    print(l ,pr)
    if not pr or len(l) == 1:
        msg = bot.send_message(message.chat.id, 'Дата некорректна❌. Введи новую дату в формате ДД.ММ и название праздника')
        bot.register_next_step_handler(msg, add)
    else:
        a, b = l[0].split('.')
        c = ''
        for i in range(1, len(l)):
            c += l[i] + " "
        c = c[:len(c)-1]
        print(c)
        cur.execute('''INSERT INTO holidays(days, months, names) VALUES(?, ?, ?)''', (a, b, c))
        msg = bot.send_message(message.chat.id, 'Добавлен👍')

# запуск команда поздравление
@bot.message_handler(commands=['congratulation'])
def z_pozdr(message):
    msg = bot.send_message(message.chat.id, 'Введи дату через в формате ДД.ММ и имя, кого поздравить')
    bot.register_next_step_handler(msg, pozdr)
# вывод поздравления
def pozdr(message):
    inp = message.text
    l = list(inp.split())
    pr = check_data(l[0])
    if(not pr or len(l) == 1):
        msg = bot.send_message(message.chat.id, 'Неправильный ввод❌. Введи новую дату через в формате ДД.ММ и новое имя, кого поздравить')
        bot.register_next_step_handler(msg, pozdr)
    else:
        f, e = map(int, l[0].split('.'))
        print(f, e)
        c = ''
        for i in range(1, len(l)):
            c += l[i] + ' ';
        c = c[:len(c)-1]
        cur.execute('''SELECT names FROM holidays WHERE days = ? AND months = ?''', (f, e))
        ans = cur.fetchall()
        for i in ans:
            bot.send_message(message.chat.id, f'{c}! Сегодня {f} {PROVERKA[e - 1][1]} отмечается {i[0]}, Поздравляю тебя🎉🎉!')


bot.infinity_polling()