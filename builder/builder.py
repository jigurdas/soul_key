import os
import json
import subprocess
import shutil



with open("config.json", "r") as file:
    data = json.load(file)
def update_config_value(config_file, key, value):
    with open(config_file, 'r') as file:
        data = json.load(file)
        data[key] = value
    with open(config_file, 'w') as file:
        json.dump(data, file, indent=4)

def build_exe():
    # Налаштування для компіляції Python-програми в exe
    python_file = "main.py"  # Змінити на ім'я вашого основного скрипту Python
    exe_name = "main.exe"  # Вкажіть ім'я exe файлу

    if data == None:
        # Змінюємо значення в config.json перед зборкою
        config_file = "config.json"
        user_id = "user_id"  # Вкажіть ключ, який потрібно змінити
        new_value_user_id = input("Вкажіть ваш TG ID")  # Вкажіть нове значення для ключа
        bot_token = "bot_token"  # Вкажіть ключ, який потрібно змінити
        new_value_bot_token = input("Вкажіть токен вашого TG бота")  # Вкажіть нове значення для ключа
        ngrok_token = "ngrok_token"  # Вкажіть ключ, який потрібно змінити
        new_value_ngrok_token = input("Вкажіть токен вашого Ngrock")  # Вкажіть нове значення для ключа
        auto_start = "auto_start"  # Вкажіть ключ, який потрібно змінити
        new_value_auto_start = input("запускати скрипт автозагрузки (Y/N)")  # Вкажіть нове значення для ключа

        update_config_value(config_file, user_id, new_value_user_id, bot_token, new_value_bot_token, ngrok_token,
                            new_value_ngrok_token, auto_start, new_value_auto_start)

    # Компіляція Python-програми в exe за допомогою команди pyinstaller
    command = f'pyinstaller --onefile --add-data "config.json;." {python_file}'
    subprocess.run(command, shell=True)

    # Змінюємо робочу директорію на ту, де знаходиться main.exe
    os.chdir("dist")

    # Перейменовуємо exe файл вказаним ім'ям
    #os.rename(python_file.replace(".py", ".exe"), exe_name)

    # # Отримуємо абсолютний шлях до файлу config.json
    config_file = os.path.join(os.path.dirname(__file__), "config.json")
    #
    # # Копіюємо файл config.json до папки dist
    # shutil.copy(config_file, "config.json")

    print("Компіляція завершена!")

if __name__ == "__main__":
    build_exe()
